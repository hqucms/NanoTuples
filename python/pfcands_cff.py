import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var, ExtVar, CandVars


def addSVPFCands(process, outTableName='PFCands', path=None):

    process.svConstituentsTable = cms.EDProducer(
        "SVPFCandidateTableProducer",
        name=cms.string(outTableName)
    )

    process.svConstituentsExtTable = cms.EDProducer(
        "SimpleCandidateFlatTableProducer",
        src=cms.InputTag("svConstituentsTable", "constituents"),
        cut=cms.string(""),  # we should not apply any further cut
        name=cms.string(outTableName),
        doc=cms.string("pfcands near SVs"),
        singleton=cms.bool(False),
        # set to ``True``: this is the extension table of svConstituentsTable
        extension=cms.bool(True),
        variables=cms.PSet(
            CandVars,
            puppiWeight=Var("puppiWeight()", float, doc="Puppi weight", precision=10),
            # vtxChi2=Var("?hasTrackDetails()?vertexChi2():-1", float, doc="vertex chi2", precision=10),
            trkChi2=Var("?hasTrackDetails()?pseudoTrack().normalizedChi2():-1",
                        float, doc="normalized trk chi2", precision=10),
            dz=Var("dz()", float, doc="pf dz", precision=10),
            dzErr=Var("?hasTrackDetails()?dzError():-1", float, doc="pf dz err", precision=10),
            d0=Var("dxy()", float, doc="pf d0", precision=10),
            d0Err=Var("?hasTrackDetails()?dxyError():-1", float, doc="pf d0 err", precision=10),
            pvAssocQuality=Var("pvAssociationQuality()", int, doc="primary vertex association quality"),
            lostInnerHits=Var("lostInnerHits()", int, doc="lost inner hits"),
            trkQuality=Var("?hasTrackDetails()?pseudoTrack().qualityMask():0", int, doc="track quality mask"),
            nValidHits=Var("?hasTrackDetails()?pseudoTrack().hitPattern().numberOfValidHits():0",
                           int, doc="lost inner hits"),
            nValidPixelHits=Var("?hasTrackDetails()?pseudoTrack().hitPattern().numberOfValidPixelHits():0",
                                int, doc="lost inner hits"),
        )
    )

    process.pfcandTask = cms.Task(
        process.svConstituentsTable,
        process.svConstituentsExtTable,
    )

    # customize SV table
    process.vertexTable.dlenMin = -1
    process.vertexTable.dlenSigMin = -1
    process.svCandidateTable.variables.ntracks = Var("numberOfDaughters()", int, doc="number of tracks")
    externalVariables = getattr(process.svCandidateTable, 'externalVariables', cms.PSet())
    externalVariables.nPFCand = ExtVar(
        cms.InputTag("svConstituentsTable", 'npfcands'),
        int, doc="number of selected PFCands stored in the %s table" % outTableName)
    process.svCandidateTable.externalVariables = externalVariables

    if path is None:
        process.schedule.associate(process.pfcandTask)
    else:
        getattr(process, path).associate(process.pfcandTask)
