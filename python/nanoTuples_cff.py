import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import Var
from PhysicsTools.NanoTuples.ak15_cff import setupAK15
from PhysicsTools.NanoTuples.ak8_cff import addParticleNetAK8
from PhysicsTools.NanoTuples.pfcands_cff import addPFCands


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


def nanoTuples_customizeMetTable(process):
    process.metTable.variables.smearPt = Var("shiftedPt('NoShift','Type1Smear')", float, doc="JER smeared type-1 met pt", precision=-1)
    process.metTable.variables.smearPhi = Var("shiftedPhi('NoShift','Type1Smear')", float, doc="JER smeared type-1 met phi", precision=12)
    process.metTable.variables.smearMetJetEnUpDeltaX = Var("shiftedPx('JetEnUp','Type1Smear')-shiftedPx('NoShift','Type1Smear')", float, doc="Delta (smearMETx_mod-smearMETx) JES Up", precision=10)
    process.metTable.variables.smearMetJetEnUpDeltaY = Var("shiftedPy('JetEnUp','Type1Smear')-shiftedPy('NoShift','Type1Smear')", float, doc="Delta (smearMETy_mod-smearMETy) JES Up", precision=10)
    process.metTable.variables.smearMetJetResUpDeltaX = Var("shiftedPx('JetResUp','Type1Smear')-shiftedPx('NoShift','Type1Smear')", float, doc="Delta (smearMETx_mod-smearMETx) JER Up", precision=10)
    process.metTable.variables.smearMetJetResUpDeltaY = Var("shiftedPy('JetResUp','Type1Smear')-shiftedPy('NoShift','Type1Smear')", float, doc="Delta (smearMETy_mod-smearMETy) JER Up", precision=10)
    process.metTable.variables.smearMetUnclustEnUpDeltaX = Var("shiftedPx('UnclusteredEnUp','Type1Smear')-shiftedPx('NoShift','Type1Smear')", float, doc="Delta (smearMETx_mod-smearMETx) UnclusteredEn Up", precision=10)
    process.metTable.variables.smearMetUnclustEnUpDeltaY = Var("shiftedPy('UnclusteredEnUp','Type1Smear')-shiftedPy('NoShift','Type1Smear')", float, doc="Delta (smearMETy_mod-smearMETy) UnclusteredEn Up", precision=10)
    # use the same for metFixEE2017
    process.metFixEE2017Table.variables = process.metTable.variables.clone()
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
    addParticleNetAK8(process, runParticleNet=False, runParticleNetMD=True)
    addPFCands(process,
               srcs=('ak15WithUserData', 'updatedJetsAK8WithUserData'),
               isPuppiJets=(True, True),
               jetTables=('ak15Table', 'fatJetTable'),
               outTableName='PFCands',
               )

    nanoTuples_customizeVectexTable(process)
    nanoTuples_customizeMetTable(process)
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
