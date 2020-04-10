import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var
from PhysicsTools.NanoTuples.ak15_cff import setupAK15


def nanoTuples_customizeVectexTable(process):
    process.vertexTable.dlenMin = -1
    process.vertexTable.dlenSigMin = -1
    process.svCandidateTable.variables.ntracks = Var("numberOfDaughters()", int, doc="number of tracks")
    return process


def nanoTuples_customizeFatJetTable(process, runOnMC, addDeepAK8Probs=False):
    if addDeepAK8Probs:
        # add DeepAK8 raw scores: nominal
        from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import _pfDeepBoostedJetTagsProbs
        for prob in _pfDeepBoostedJetTagsProbs:
            name = prob.split(':')[1]
            setattr(process.fatJetTable.variables, 'deepTag_' + name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

        # add DeepAK8 raw scores: mass decorrelated
        from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import _pfMassDecorrelatedDeepBoostedJetTagsProbs
        for prob in _pfMassDecorrelatedDeepBoostedJetTagsProbs:
            name = prob.split(':')[1]
            setattr(process.fatJetTable.variables, 'deepTagMD_' + name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    if runOnMC:
        process.finalGenParticles.select.append('keep+ (abs(pdgId) == 6 || abs(pdgId) == 23 || abs(pdgId) == 24 || abs(pdgId) == 25)')

    return process


def _fix_tau_global_tag(process):
    global_tag_map = {
        '102X_mcRun2_asymptotic_v':'110X_mcRun2_asymptotic_v7',
        '102X_mc2017_realistic_v':'110X_mc2017_realistic_v4',
        '102X_upgrade2018_realistic_v':'110X_upgrade2018_realistic_v9',
        '102X_dataRun2_v':'111X_dataRun2_v2',
        '102X_dataRun2_Prompt_v':'111X_dataRun2_v2',
        }
    for k in global_tag_map:
        if k in process.GlobalTag.globaltag.value():
            tau_tag = global_tag_map[k]
            break
    process.loadRecoTauTagMVAsFromPrepDB.globaltag = tau_tag
    process.prefer('GlobalTag')
    return process


def nanoTuples_customizeCommon(process, runOnMC):
    setupAK15(process, runOnMC=runOnMC)
    nanoTuples_customizeVectexTable(process)
    nanoTuples_customizeFatJetTable(process, runOnMC=runOnMC)
    _fix_tau_global_tag(process)

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
