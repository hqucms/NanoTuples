import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var
from PhysicsTools.NanoTuples.pfcands_cff import addSVPFCands


def nanoTuples_customizeCommon(process, runOnMC):
    # add ParticleNetAK4
    from RecoBTag.ONNXRuntime.pfParticleNetAK4_cff import _pfParticleNetAK4JetTagsProbs
    for prob in _pfParticleNetAK4JetTagsProbs:
        name = 'ParticleNetAK4_' + prob.split(':')[1]
        setattr(process.jetTable.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=10))

    # add PFCands for SV tagging
    addSVPFCands(process)

    return process


def nanoTuples_customizeData(process):
    process = nanoTuples_customizeCommon(process, False)

    process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication
    process.add_(cms.Service("InitRootHandlers", EnableIMT=cms.untracked.bool(False)))
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
    process.add_(cms.Service("InitRootHandlers", EnableIMT=cms.untracked.bool(False)))
    return process
