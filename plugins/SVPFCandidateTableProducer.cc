#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidateFwd.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"

#include "RecoBTag/FeatureTools/interface/TrackInfoBuilder.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"

#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "DataFormats/Common/interface/ValueMap.h"

class SVPFCandidateTableProducer : public edm::stream::EDProducer<> {
public:
  explicit SVPFCandidateTableProducer(const edm::ParameterSet &);
  ~SVPFCandidateTableProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
  typedef edm::Ptr<pat::PackedCandidate> CandidatePtr;
  typedef edm::View<pat::PackedCandidate> CandidateView;
  typedef reco::VertexCollection VertexCollection;

  void produce(edm::Event &, const edm::EventSetup &) override;

  std::vector<CandidatePtr> getPFCands(const reco::VertexCompositePtrCandidate &sv);

  const std::string name_;

  edm::EDGetTokenT<reco::VertexCompositePtrCandidateView> sv_token_;
  edm::EDGetTokenT<edm::View<pat::Jet>> jet_token_;
  edm::EDGetTokenT<VertexCollection> vtx_token_;
  edm::EDGetTokenT<CandidateView> pfcand_token_;

  edm::Handle<reco::VertexCompositePtrCandidateView> svs_;
  edm::Handle<edm::View<pat::Jet>> jets_;
  edm::Handle<VertexCollection> vtxs_;
  edm::Handle<CandidateView> pfcands_;

  std::vector<const pat::Jet *> selected_jets_;

  edm::ESHandle<TransientTrackBuilder> track_builder_;
};

//
// constructors and destructor
//
SVPFCandidateTableProducer::SVPFCandidateTableProducer(const edm::ParameterSet &iConfig)
    : name_(iConfig.getParameter<std::string>("name")),
      sv_token_(
          consumes<reco::VertexCompositePtrCandidateView>(iConfig.getParameter<edm::InputTag>("secondary_vertices"))),
      jet_token_(consumes<edm::View<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jets"))),
      vtx_token_(consumes<VertexCollection>(iConfig.getParameter<edm::InputTag>("vertices"))),
      pfcand_token_(consumes<CandidateView>(iConfig.getParameter<edm::InputTag>("pf_candidates"))) {
  produces<nanoaod::FlatTable>(name_);
  produces<std::vector<CandidatePtr>>("constituents");
  produces<edm::ValueMap<int>>("npfcands");
}

SVPFCandidateTableProducer::~SVPFCandidateTableProducer() {}

void SVPFCandidateTableProducer::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {
  // elements in all these collections must have the same order!
  auto outCands = std::make_unique<std::vector<CandidatePtr>>();
  std::vector<float> btagEtaRel, btagPtRatio, btagPParRatio, btagSip3dVal, btagSip3dSig, btagJetDistVal;

  iEvent.getByToken(sv_token_, svs_);
  std::vector<int> nPFCands(svs_->size(), 0);

  iEvent.getByToken(vtx_token_, vtxs_);
  if (!vtxs_->empty()) {
    iEvent.getByToken(jet_token_, jets_);
    for (unsigned j = 0; j < jets_->size(); ++j) {
      const auto &jet = jets_->at(j);
      if (jet.correctedP4(0).pt() > 40 && std::abs(jet.eta() < 2.5)) {
        selected_jets_.push_back(&jet);
      }
    }

    iEvent.getByToken(pfcand_token_, pfcands_);
    iSetup.get<TransientTrackRecord>().get("TransientTrackBuilder", track_builder_);

    for (unsigned i_sv = 0; i_sv < svs_->size(); ++i_sv) {
      const auto &sv = svs_->at(i_sv);

      auto daughters = getPFCands(sv);
      nPFCands[i_sv] = daughters.size();
      for (const auto &cand : daughters) {
        outCands->push_back(cand);
        if (cand->hasTrackDetails()) {
          math::XYZVector jet_dir = sv.momentum().Unit();
          GlobalVector jet_ref_track_dir(sv.px(), sv.py(), sv.pz());
          btagbtvdeep::TrackInfoBuilder trkinfo(track_builder_);
          trkinfo.buildTrackInfo(&(*cand), jet_dir, jet_ref_track_dir, vtxs_->at(0));
          btagEtaRel.push_back(trkinfo.getTrackEtaRel());
          btagPtRatio.push_back(trkinfo.getTrackPtRatio());
          btagPParRatio.push_back(trkinfo.getTrackPParRatio());
          btagSip3dVal.push_back(trkinfo.getTrackSip3dVal());
          btagSip3dSig.push_back(trkinfo.getTrackSip3dSig());
          btagJetDistVal.push_back(trkinfo.getTrackJetDistVal());
        } else {
          btagEtaRel.push_back(0);
          btagPtRatio.push_back(0);
          btagPParRatio.push_back(0);
          btagSip3dVal.push_back(0);
          btagSip3dSig.push_back(0);
          btagJetDistVal.push_back(0);
        }
      }
    }  // end sv loop
  }

  auto candTable = std::make_unique<nanoaod::FlatTable>(outCands->size(), name_, false);
  // We fill from here only stuff that cannot be created with the SimpleFlatTableProducer
  candTable->addColumn<float>("btagEtaRel", btagEtaRel, "btagEtaRel", nanoaod::FlatTable::FloatColumn, 10);
  candTable->addColumn<float>("btagPtRatio", btagPtRatio, "btagPtRatio", nanoaod::FlatTable::FloatColumn, 10);
  candTable->addColumn<float>("btagPParRatio", btagPParRatio, "btagPParRatio", nanoaod::FlatTable::FloatColumn, 10);
  candTable->addColumn<float>("btagSip3dVal", btagSip3dVal, "btagSip3dVal", nanoaod::FlatTable::FloatColumn, 10);
  candTable->addColumn<float>("btagSip3dSig", btagSip3dSig, "btagSip3dSig", nanoaod::FlatTable::FloatColumn, 10);
  candTable->addColumn<float>("btagJetDistVal", btagJetDistVal, "btagJetDistVal", nanoaod::FlatTable::FloatColumn, 10);

  iEvent.put(std::move(candTable), name_);
  iEvent.put(std::move(outCands), "constituents");
  auto npfMap = std::make_unique<edm::ValueMap<int>>();
  edm::ValueMap<int>::Filler filler(*npfMap);
  filler.insert(svs_, nPFCands.begin(), nPFCands.end());
  filler.fill();
  iEvent.put(std::move(npfMap), "npfcands");
}

std::vector<SVPFCandidateTableProducer::CandidatePtr> SVPFCandidateTableProducer::getPFCands(
    const reco::VertexCompositePtrCandidate &sv) {
  std::vector<CandidatePtr> daughters;
  // 1) check if the SV is inside any selected jets; if yes, store no PFCands
  for (const auto *jet : selected_jets_) {
    if (reco::deltaR(sv, *jet) < 0.4) {
      return daughters;
    }
  }
  // 2) loop over all pfcands and selected those satisfying deltaR(sv, pf) < 0.4
  for (unsigned i = 0; i < pfcands_->size(); ++i) {
    const auto &cand = pfcands_->ptrAt(i);
    if (reco::deltaR(sv, *cand) < 0.4) {
      daughters.push_back(cand);
    }
  }
  // sort pfcands by pt
  std::sort(daughters.begin(), daughters.end(), [](const auto &a, const auto &b) { return a->pt() > b->pt(); });
  return daughters;
}

void SVPFCandidateTableProducer::fillDescriptions(edm::ConfigurationDescriptions &descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<std::string>("name", "PFCands");
  desc.add<edm::InputTag>("secondary_vertices", edm::InputTag("slimmedSecondaryVertices"));
  desc.add<edm::InputTag>("jets", edm::InputTag("slimmedJets"));
  desc.add<edm::InputTag>("vertices", edm::InputTag("offlineSlimmedPrimaryVertices"));
  desc.add<edm::InputTag>("pf_candidates", edm::InputTag("packedPFCandidates"));
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(SVPFCandidateTableProducer);
