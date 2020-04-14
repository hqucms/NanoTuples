import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *


def addPFCands(process, jetCollections={'ak15':'ak15WithUserData'}, tableName='AK15PuppiPFCands', path=None):

    jets = {}
    for jetname in jetCollections:
        src = jetCollections[jetname]
        if not isinstance(src, cms.InputTag):
            src = cms.InputTag(src)
        jets[jetname] = cms.PSet(
            src=src,
            isPuppi=cms.bool('chs' not in jetname.lower()),
            cut=cms.string(''),
            )

    process.jetConstituentsTable = cms.EDProducer("JetConstituentTableProducer",
                                                  jets=cms.PSet(**jets),
                                                  name=cms.string(tableName),
                                                  )

    process.jetConstituentsExtTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
                                                     src=cms.InputTag("jetConstituentsTable"),
                                                     cut=cms.string(""),  # we should not apply any further cut
                                                     name=process.jetConstituentsTable.name,
                                                     doc=cms.string("pfcands from jets"),
                                                     singleton=cms.bool(False),
                                                     extension=cms.bool(True),  # set to ``True``: this is the extension table of jetConstituentsTable
                                                     variables=cms.PSet(CandVars,
                                                                        puppiWeight=Var("puppiWeight()", float, doc="Puppi weight", precision=10),
                                                                        vtxChi2=Var("?hasTrackDetails()?vertexChi2():-1", float, doc="vertex chi2", precision=10),
                                                                        trkChi2=Var("?hasTrackDetails()?pseudoTrack().normalizedChi2():-1", float, doc="normalized trk chi2", precision=10),
                                                                        dz=Var("dz()", float, doc="pf dz", precision=10),
                                                                        dzErr=Var("?hasTrackDetails()?dzError():-1", float, doc="pf dz err", precision=10),
                                                                        d0=Var("dxy()", float, doc="pf d0", precision=10),
                                                                        d0Err=Var("?hasTrackDetails()?dxyError():-1", float, doc="pf d0 err", precision=10),
                                                                        pvAssocQuality=Var("pvAssociationQuality()", int, doc="primary vertex association quality"),
                                                                        lostInnerHits=Var("lostInnerHits()", int, doc="lost inner hits"),
                                                                        trkQuality=Var("?hasTrackDetails()?pseudoTrack().qualityMask():0", int, doc="track quality mask"),
                                                                        )
                                                     )

    process.pfcandTask = cms.Task(
        process.jetConstituentsTable,
        process.jetConstituentsExtTable,
        )

    if path is None:
        process.schedule.associate(process.pfcandTask)
    else:
        getattr(process, path).associate(process.pfcandTask)
