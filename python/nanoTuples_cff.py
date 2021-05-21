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


def nanoTuples_customizeCommon(process, runOnMC, addAK15=True, addAK8=False, addPFcands=False):
    pfcand_params = {'srcs': [], 'isPuppiJets':[], 'jetTables':[]}
    if addAK15:
        setupAK15(process, runOnMC=runOnMC)
        pfcand_params['srcs'].append('ak15WithUserData')
        pfcand_params['isPuppiJets'].append(True)
        pfcand_params['jetTables'].append('ak15Table')
    if addAK8:
        addParticleNetAK8(process, runParticleNet=False, runParticleNetMD=True)
        pfcand_params['srcs'].append('updatedJetsAK8WithUserData')
        pfcand_params['isPuppiJets'].append(True)
        pfcand_params['jetTables'].append('fatJetTable')
    if addPFcands:
        addPFCands(process, outTableName='PFCands', **pfcand_params)

    # nanoTuples_customizeVectexTable(process)
    # nanoTuples_customizeFatJetTable(process, runOnMC=runOnMC)

    return process


def nanoTuples_customizeData(process):
    process = nanoTuples_customizeCommon(process, False)

    process.NANOAODoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication
    process.add_(cms.Service("InitRootHandlers", EnableIMT=cms.untracked.bool(False)))
    return process


def nanoTuples_customizeMC(process):
    process = nanoTuples_customizeCommon(process, True)

    process.NANOAODSIMoutput.fakeNameForCrab = cms.untracked.bool(True)  # hack for crab publication
    process.add_(cms.Service("InitRootHandlers", EnableIMT=cms.untracked.bool(False)))
    return process
