import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *


def addPFCands(process, srcs=[], isPuppiJets=[], jetTables=[], cuts=None, outTableName='PFCands', path=None):
    if len(srcs) == 0:
        return

    if cuts is None:
        cuts = [None for _ in jetTables]
    jetTables = [getattr(process, tbl_name) for tbl_name in jetTables]
    jets = {}
    for src, jet_table, is_puppi, cut in zip(srcs, jetTables, isPuppiJets, cuts):
        jetname = jet_table.name.value()
        jets[jetname] = cms.PSet(
            src=cms.InputTag(src),
            isPuppi=cms.bool(is_puppi),
            cut=jet_table.cut if cut is None else cms.string(cut),
            )

    process.jetConstituentsTable = cms.EDProducer("JetConstituentTableProducer",
                                                  jets=cms.PSet(**jets),
                                                  name=cms.string(outTableName),
                                                  check_indices=cms.bool(False),  # turn on for debugging
                                                  )

    process.jetConstituentsExtTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
                                                     src=cms.InputTag("jetConstituentsTable", "constituents"),
                                                     cut=cms.string(""),  # we should not apply any further cut
                                                     name=cms.string(outTableName),
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

    # add nPFCands to the jet tables
    for jet_table in jetTables:
        jetname = jet_table.name.value()
        externalVariables = getattr(jet_table, 'externalVariables', cms.PSet())
        externalVariables.nPFCand = ExtVar(cms.InputTag("jetConstituentsTable", jetname + 'Npfcand'), int, doc="number of selected PFCands stored in the %s table" % outTableName)
        jet_table.externalVariables = externalVariables

    if path is None:
        process.schedule.associate(process.pfcandTask)
    else:
        getattr(process, path).associate(process.pfcandTask)
