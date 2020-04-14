#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "RecoBTag/FeatureTools/interface/TrackInfoBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"

#include <unordered_map>
#include <set>

class JetConstituentTableProducer : public edm::stream::EDProducer<> {
public:
  explicit JetConstituentTableProducer(const edm::ParameterSet &);
  ~JetConstituentTableProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  typedef edm::Ptr<pat::PackedCandidate> CandidatePtr;
  typedef CandidatePtr::key_type Key;
  typedef edm::View<pat::PackedCandidate> CandidateView;
  typedef reco::VertexCollection VertexCollection;

  void produce(edm::Event &, const edm::EventSetup &) override;

  template <typename T>
  T getval(const std::unordered_map<Key, T> &m, Key key, T fallback = 0) {
    auto it = m.find(key);
    return it == m.end() ? fallback : it->second;
  }

  const std::string name_;

  unsigned ncols_ = 0;
  std::vector<std::string> jet_names_;
  std::vector<bool> jet_ispuppi_;
  std::vector<StringCutObjectSelector<pat::Jet>> jet_cuts_;
  std::vector<edm::EDGetTokenT<edm::View<pat::Jet>>> jet_tokens_;

  edm::EDGetTokenT<VertexCollection> vtx_token_;
  edm::EDGetTokenT<CandidateView> pfcand_token_;

  edm::Handle<VertexCollection> vtxs_;
  edm::Handle<CandidateView> pfcands_;
  edm::ESHandle<TransientTrackBuilder> track_builder_;
};

//
// constructors and destructor
//
JetConstituentTableProducer::JetConstituentTableProducer(const edm::ParameterSet &iConfig)
    : name_(iConfig.getParameter<std::string>("name")),
      vtx_token_(consumes<VertexCollection>(iConfig.getParameter<edm::InputTag>("vertices"))),
      pfcand_token_(consumes<CandidateView>(iConfig.getParameter<edm::InputTag>("pf_candidates"))) {
  const auto &pset = iConfig.getParameterSet("jets");
  jet_names_ = pset.getParameterNames();
  ncols_ = jet_names_.size();
  for (const auto &jetname : jet_names_) {
    const auto &p = pset.getParameterSet(jetname);
    jet_ispuppi_.emplace_back(p.getParameter<bool>("isPuppi"));
    jet_cuts_.emplace_back(p.getParameter<std::string>("cut"), true);
    jet_tokens_.emplace_back(consumes<edm::View<pat::Jet>>(p.getParameter<edm::InputTag>("src")));
  }

  produces<nanoaod::FlatTable>(name_);
  produces<std::vector<CandidatePtr>>();
}

JetConstituentTableProducer::~JetConstituentTableProducer() {}

void JetConstituentTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {
  // elements in all these collections must have the same order!
  auto outCands = std::make_unique<std::vector<CandidatePtr>>();
  std::vector<std::vector<int>> jetIdx(ncols_);
  std::vector<std::vector<float>> btagEtaRel(ncols_), btagPtRatio(ncols_), btagPParRatio(ncols_), btagSip3dVal(ncols_),
      btagSip3dSig(ncols_), btagJetDistVal(ncols_);

  iEvent.getByToken(vtx_token_, vtxs_);
  if (!vtxs_->empty()) {
    iEvent.getByToken(pfcand_token_, pfcands_);
    iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", track_builder_);

    std::vector<Key> pfcand_idxs;

    // vmaps below: one for each jet collection
    std::vector<std::unordered_map<Key, int>> vmap_jetIdx(ncols_);
    std::vector<std::unordered_map<Key, float>> vmap_btagEtaRel(ncols_), vmap_btagPtRatio(ncols_),
        vmap_btagPParRatio(ncols_), vmap_btagSip3dVal(ncols_), vmap_btagSip3dSig(ncols_), vmap_btagJetDistVal(ncols_);

    for (unsigned ic = 0; ic < ncols_; ++ic) {
      auto &m_jetIdx = vmap_jetIdx[ic];
      auto &m_btagEtaRel = vmap_btagEtaRel[ic];
      auto &m_btagPtRatio = vmap_btagPtRatio[ic];
      auto &m_btagPParRatio = vmap_btagPParRatio[ic];
      auto &m_btagSip3dVal = vmap_btagSip3dVal[ic];
      auto &m_btagSip3dSig = vmap_btagSip3dSig[ic];
      auto &m_btagJetDistVal = vmap_btagJetDistVal[ic];

      edm::Handle<edm::View<pat::Jet>> jets;
      iEvent.getByToken(jet_tokens_[ic], jets);
      for (unsigned i_jet = 0; i_jet < jets->size(); ++i_jet) {
        const auto &jet = jets->at(i_jet);
        if (!jet_cuts_[ic](jet))
          continue;

        math::XYZVector jet_dir = jet.momentum().Unit();
        GlobalVector jet_ref_track_dir(jet.px(), jet.py(), jet.pz());

        std::vector<CandidatePtr> daughters;
        for (const auto &cand : jet.daughterPtrVector()) {
          const auto *packed_cand = dynamic_cast<const pat::PackedCandidate *>(&(*cand));
          assert(packed_cand != nullptr);
          // remove particles w/ extremely low puppi weights (needed for 2017 MiniAOD)
          if (jet_ispuppi_[ic] && packed_cand->puppiWeight() < 0.01)
            continue;
          // get the original reco/packed candidate not scaled by the puppi weight
          daughters.push_back(pfcands_->ptrAt(cand.key()));
        }

        if (ncols_ == 1) {
          // sort by original pt (to preserve old behavior, i.e., pt ordered, when only one jet collection is given)
          // not needed for ncols_>1 as then the pfcands will be ordered by their keys
          std::sort(daughters.begin(), daughters.end(), [](const auto &a, const auto &b) { return a->pt() > b->pt(); });
        }

        for (const auto &cand : daughters) {
          pfcand_idxs.push_back(cand.key());
          m_jetIdx[cand.key()] = i_jet;
          if (cand->hasTrackDetails()) {
            btagbtvdeep::TrackInfoBuilder trkinfo(track_builder_);
            trkinfo.buildTrackInfo(&(*cand), jet_dir, jet_ref_track_dir, vtxs_->at(0));
            m_btagEtaRel[cand.key()] = trkinfo.getTrackEtaRel();
            m_btagPtRatio[cand.key()] = trkinfo.getTrackPtRatio();
            m_btagPParRatio[cand.key()] = trkinfo.getTrackPParRatio();
            m_btagSip3dVal[cand.key()] = trkinfo.getTrackSip3dVal();
            m_btagSip3dSig[cand.key()] = trkinfo.getTrackSip3dSig();
            m_btagJetDistVal[cand.key()] = trkinfo.getTrackJetDistVal();
          } else {
            m_btagEtaRel[cand.key()] = 0;
            m_btagPtRatio[cand.key()] = 0;
            m_btagPParRatio[cand.key()] = 0;
            m_btagSip3dVal[cand.key()] = 0;
            m_btagSip3dSig[cand.key()] = 0;
            m_btagJetDistVal[cand.key()] = 0;
          }
        }
      }  // end jet loop
    }

    if (ncols_ > 1) {
      // remove duplicates
      std::set<Key> s(pfcand_idxs.begin(), pfcand_idxs.end());
      pfcand_idxs.clear();
      pfcand_idxs.insert(pfcand_idxs.end(), s.begin(), s.end());
    }

    for (const auto &key : pfcand_idxs) {
      outCands->push_back(pfcands_->ptrAt(key));
      // fill jetIdx and other variables
      for (unsigned ic = 0; ic < ncols_; ++ic) {
        // jetIdx: fill -1 if this pfcand does not appear in this jet collection
        jetIdx[ic].push_back(getval(vmap_jetIdx[ic], key, -1));
        // for other variables we fill 0
        btagEtaRel[ic].push_back(getval(vmap_btagEtaRel[ic], key));
        btagPtRatio[ic].push_back(getval(vmap_btagPtRatio[ic], key));
        btagPParRatio[ic].push_back(getval(vmap_btagPParRatio[ic], key));
        btagSip3dVal[ic].push_back(getval(vmap_btagSip3dVal[ic], key));
        btagSip3dSig[ic].push_back(getval(vmap_btagSip3dSig[ic], key));
        btagJetDistVal[ic].push_back(getval(vmap_btagJetDistVal[ic], key));
      }
    }
  }

  auto candTable = std::make_unique<nanoaod::FlatTable>(outCands->size(), name_, false);
  // We fill from here only stuff that cannot be created with the SimpleFlatTableProducer
  for (unsigned ic = 0; ic < ncols_; ++ic) {
    auto prefix = ncols_ > 1 ? jet_names_[ic] + "_" : "";
    auto doc = ncols_ > 1 ? "(" + jet_names_[ic] + ")" : "";
    candTable->addColumn<int>(
        prefix + "jetIdx", jetIdx[ic], "Index of the parent jet" + doc, nanoaod::FlatTable::IntColumn);
    candTable->addColumn<float>(
        prefix + "btagEtaRel", btagEtaRel[ic], "btagEtaRel" + doc, nanoaod::FlatTable::FloatColumn, 10);
    candTable->addColumn<float>(
        prefix + "btagPtRatio", btagPtRatio[ic], "btagPtRatio" + doc, nanoaod::FlatTable::FloatColumn, 10);
    candTable->addColumn<float>(
        prefix + "btagPParRatio", btagPParRatio[ic], "btagPParRatio" + doc, nanoaod::FlatTable::FloatColumn, 10);
    candTable->addColumn<float>(
        prefix + "btagSip3dVal", btagSip3dVal[ic], "btagSip3dVal" + doc, nanoaod::FlatTable::FloatColumn, 10);
    candTable->addColumn<float>(
        prefix + "btagSip3dSig", btagSip3dSig[ic], "btagSip3dSig" + doc, nanoaod::FlatTable::FloatColumn, 10);
    candTable->addColumn<float>(
        prefix + "btagJetDistVal", btagJetDistVal[ic], "btagJetDistVal" + doc, nanoaod::FlatTable::FloatColumn, 10);
  }

  iEvent.put(std::move(candTable), name_);
  iEvent.put(std::move(outCands));
}

void JetConstituentTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<std::string>("name", "JetPFCands");
  edm::ParameterSetDescription jets;
  jets.setAllowAnything();
  desc.add<edm::ParameterSetDescription>("jets", jets);
  desc.add<edm::InputTag>("vertices", edm::InputTag("offlineSlimmedPrimaryVertices"));
  desc.add<edm::InputTag>("pf_candidates", edm::InputTag("packedPFCandidates"));
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(JetConstituentTableProducer);
