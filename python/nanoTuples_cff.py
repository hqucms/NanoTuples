import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var
from PhysicsTools.NanoTuples.ak8_cff import setupCustomizedAK8
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
    setupCustomizedAK8(process, runOnMC=runOnMC)
    setupAK15(process, runOnMC=runOnMC)
    nanoTuples_customizeVectexTable(process)

    return process


def nanoTuples_customizeData(process):
    process = nanoTuples_customizeCommon(process, False)

    process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication
    return process


def nanoTuples_customizeData_saveTriggerPrescale(process):
    process = nanoTuples_customizeData(process)
    process.NANOAODoutput.outputCommands = cms.untracked.vstring(
        'drop *',
        "keep nanoaodFlatTable_*Table_*_*",  # event data
        "keep edmTriggerResults_*_*_*",  # event data
        "keep patPackedTriggerPrescales_patTrigger__PAT",  # add trigger prescale
        "keep nanoaodMergeableCounterTable_*Table_*_*",  # accumulated per/run or per/lumi data
        "keep nanoaodUniqueString_nanoMetadata_*_*",  # basic metadata
        )
    return process


def nanoTuples_customizeMC(process):
    process = nanoTuples_customizeCommon(process, True)

    process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication
    return process
