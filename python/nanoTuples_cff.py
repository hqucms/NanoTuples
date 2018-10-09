import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var
# from PhysicsTools.NanoTuples.ca15_cff import setupCA15
from PhysicsTools.NanoTuples.ak15_cff import setupAK15


def nanoTuples_customizeVectexTable(process):
    process.vertexTable = cms.EDProducer("CustomVertexTableProducer",
        pvSrc=cms.InputTag("offlineSlimmedPrimaryVertices"),
        goodPvCut=cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2"),
        svSrc=cms.InputTag("slimmedSecondaryVertices"),
        svCut=cms.string(""),
        dlenMin=cms.double(0),
        dlenSigMin=cms.double(0),
        pvName=cms.string("PV"),
        svName=cms.string("SV"),
        svDoc=cms.string("secondary vertices from IVF algorithm"),
    )
    process.svCandidateTable.variables.ntracks = Var("numberOfDaughters()", int, doc="number of tracks")
    return process


def nanoTuples_customizeCommon(process, runOnMC):
#     setupCA15(process, runOnMC=runOnMC)
    setupAK15(process, runOnMC=runOnMC)
    nanoTuples_customizeVectexTable(process)

    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
    runMetCorAndUncFromMiniAOD(process, isData=not runOnMC)

    process.jetTables.remove(process.saJetTable)
    process.jetTables.remove(process.fatJetTable)
    process.jetTables.remove(process.subJetTable)

    return process


def nanoTuples_customizeData(process):
    process = nanoTuples_customizeCommon(process, False)

#     process.NANOAODoutput.saveProvenance = cms.untracked.bool(False)
    process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication

    return process


def nanoTuples_customizeMC(process):
    process = nanoTuples_customizeCommon(process, True)

#     process.nanoSequenceMC.remove(process.particleLevelSequence)
#     process.nanoSequenceMC.remove(process.tauMC)
#     process.nanoSequenceMC.remove(process.ttbarCatMCProducers)
#     process.nanoSequenceMC.remove(process.particleLevelTables)
#     process.nanoSequenceMC.remove(process.ttbarCategoryTable)

#     process.NANOAODSIMoutput.saveProvenance = cms.untracked.bool(False)
    process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication

    return process
