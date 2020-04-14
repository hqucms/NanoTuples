import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Modifier_run2_jme_2016_cff import run2_jme_2016
from Configuration.Eras.Modifier_run2_jme_2017_cff import run2_jme_2017

from PhysicsTools.NanoAOD.common_cff import *

# ---------------------------------------------------------
def addParticleNetAK8(process, runParticleNet=False, runParticleNetMD=True):
    if not runParticleNet and not runParticleNetMD:
        return process

    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    from RecoBTag.MXNet.pfParticleNet_cff import _pfParticleNetJetTagsProbs as pfParticleNetJetTagsProbs
    from RecoBTag.MXNet.pfParticleNet_cff import _pfMassDecorrelatedParticleNetJetTagsProbs as pfMassDecorrelatedParticleNetJetTagsProbs

    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    bTagDiscriminators = []
    if runParticleNet:
        bTagDiscriminators += pfParticleNetJetTagsProbs
    if runParticleNetMD:
        bTagDiscriminators += pfMassDecorrelatedParticleNetJetTagsProbs

    updateJetCollection(
        process,
        jetSource=cms.InputTag('selectedUpdatedPatJetsAK8WithDeepInfo'),
        rParam=0.8,
        jetCorrections=('AK8PFPuppi', cms.vstring(JETCorrLevels), 'None'),
        btagDiscriminators=bTagDiscriminators,
        postfix='AK8WithParticleNet',
    )
    process.jetCorrFactorsAK8.src = "selectedUpdatedPatJetsAK8WithParticleNet"
    process.updatedJetsAK8.jetSource = "selectedUpdatedPatJetsAK8WithParticleNet"

    from RecoBTag.ONNXRuntime.pfDeepBoostedJetTags_cfi import pfDeepBoostedJetTags as _pfDeepBoostedJetTags
    if runParticleNet:
        process.pfParticleNetJetTagsAK8WithParticleNet = _pfDeepBoostedJetTags.clone(
            src=process.pfParticleNetJetTagsAK8WithParticleNet.src,
            flav_names=process.pfParticleNetJetTagsAK8WithParticleNet.flav_names,
            preprocessParams=process.pfParticleNetJetTagsAK8WithParticleNet.preprocessParams,
            model_path='PhysicsTools/NanoTuples/data/ParticleNet/ak8/ParticleNet.onnx',
            )
    if runParticleNetMD:
        process.pfMassDecorrelatedParticleNetJetTagsAK8WithParticleNet = _pfDeepBoostedJetTags.clone(
            src=process.pfMassDecorrelatedParticleNetJetTagsAK8WithParticleNet.src,
            flav_names=process.pfMassDecorrelatedParticleNetJetTagsAK8WithParticleNet.flav_names,
            preprocessParams=process.pfMassDecorrelatedParticleNetJetTagsAK8WithParticleNet.preprocessParams,
            model_path='PhysicsTools/NanoTuples/data/ParticleNet-MD/ak8/ParticleNetMD.onnx',
            )

    # add nominal taggers
    if runParticleNet:
        for prob in pfParticleNetJetTagsProbs:
            name = 'ParticleNet_' + prob.split(':')[1]
            setattr(process.fatJetTable.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    # add mass-decorelated taggers
    if runParticleNetMD:
        for prob in pfMassDecorrelatedParticleNetJetTagsProbs:
            name = 'ParticleNetMD_' + prob.split(':')[1]
            setattr(process.fatJetTable.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    return process



# ---------------------------------------------------------
def setupCustomizedAK8(process, runOnMC=False, path=None):
    # recluster Puppi jets
    bTagDiscriminators = [
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfBoostedDoubleSecondaryVertexAK8BJetTags',
    ]
    subjetBTagDiscriminators = [
        'pfCombinedInclusiveSecondaryVertexV2BJetTags',
        'pfDeepCSVJetTags:probb',
        'pfDeepCSVJetTags:probbb',
    ]
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']

    from PhysicsTools.NanoTuples.jetToolbox_cff import jetToolbox
    jetToolbox(process, 'ak8', 'dummySeqAK8', 'noOutput',
               PUMethod='Puppi', JETCorrPayload='AK8PFPuppi', JETCorrLevels=JETCorrLevels,
               Cut='pt > 170.0 && abs(rapidity()) < 2.4',
               runOnMC=runOnMC,
               addNsub=True, maxTau=3,
               addSoftDrop=True, addSoftDropSubjets=True, subJETCorrPayload='AK4PFPuppi', subJETCorrLevels=JETCorrLevels,
               bTagDiscriminators=bTagDiscriminators, subjetBTagDiscriminators=subjetBTagDiscriminators)

    if runOnMC:
        process.ak8GenJetsNoNu.jetPtMin = 100
        process.ak8GenJetsNoNuSoftDrop.jetPtMin = 100

    from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
    from RecoBTag.ONNXRuntime.pfDeepBoostedJet_cff import _pfDeepBoostedJetTagsProbs,_pfMassDecorrelatedDeepBoostedJetTagsProbs
    from RecoBTag.MXNet.pfParticleNet_cff import _pfParticleNetJetTagsProbs, _pfMassDecorrelatedParticleNetJetTagsProbs
    updateJetCollection(
        process,
        jetSource=cms.InputTag('packedPatJetsAK8PFPuppiSoftDrop'),
        rParam=0.8,
        jetCorrections=('AK8PFPuppi', cms.vstring(JETCorrLevels), 'None'),
        btagDiscriminators=bTagDiscriminators + _pfDeepBoostedJetTagsProbs + _pfMassDecorrelatedDeepBoostedJetTagsProbs + _pfParticleNetJetTagsProbs + _pfMassDecorrelatedParticleNetJetTagsProbs,
        postfix='AK8WithPuppiDaughters',
    )

    # src
    srcJets = cms.InputTag('selectedUpdatedPatJetsAK8WithPuppiDaughters')

    # jetID
    process.looseJetIdCustomAK8 = cms.EDProducer("PatJetIDValueMapProducer",
              filterParams=cms.PSet(
                version = cms.string('WINTER16'),
                quality = cms.string('LOOSE'),
              ),
              src=srcJets
    )

    process.tightJetIdCustomAK8 = cms.EDProducer("PatJetIDValueMapProducer",
              filterParams=cms.PSet(
                version=cms.string('SUMMER18PUPPI'),
                quality = cms.string('TIGHT'),
              ),
              src=srcJets
    )

    process.tightJetIdLepVetoCustomAK8 = cms.EDProducer("PatJetIDValueMapProducer",
              filterParams=cms.PSet(
                version = cms.string('SUMMER18PUPPI'),
                quality = cms.string('TIGHTLEPVETO'),
              ),
              src=srcJets
    )

    run2_jme_2016.toModify(process.tightJetIdCustomAK8.filterParams, version="WINTER16")
    run2_jme_2016.toModify(process.tightJetIdLepVetoCustomAK8.filterParams, version="WINTER16")
    run2_jme_2017.toModify(process.tightJetIdCustomAK8.filterParams, version="WINTER17PUPPI")
    run2_jme_2017.toModify(process.tightJetIdLepVetoCustomAK8.filterParams, version="WINTER17PUPPI")

    process.customAK8WithUserData = cms.EDProducer("PATJetUserDataEmbedder",
        src=srcJets,
        userFloats=cms.PSet(),
        userInts=cms.PSet(
           tightId=cms.InputTag("tightJetIdCustomAK8"),
           tightIdLepVeto=cms.InputTag("tightJetIdLepVetoCustomAK8"),
        ),
    )
    
    run2_jme_2016.toModify(process.customAK8WithUserData.userInts,
        looseId=cms.InputTag("looseJetIdCustomAK8"),
        tightIdLepVeto=None,
    )

    process.customAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src=cms.InputTag("customAK8WithUserData"),
        name=cms.string("CustomAK8Puppi"),
        cut=cms.string(""),
        doc=cms.string("reclustered ak8 puppi jets"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            jetId=Var("userInt('tightId')*2+4*userInt('tightIdLepVeto')", int, doc="Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"),
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            nPFConstituents=Var("numberOfDaughters()", int, doc="Number of PF candidate constituents"),
            tau1=Var("userFloat('NjettinessAK8Puppi:tau1')", float, doc="Nsubjettiness (1 axis)", precision=10),
            tau2=Var("userFloat('NjettinessAK8Puppi:tau2')", float, doc="Nsubjettiness (2 axis)", precision=10),
            tau3=Var("userFloat('NjettinessAK8Puppi:tau3')", float, doc="Nsubjettiness (3 axis)", precision=10),
            msoftdrop=Var("groomedMass()", float, doc="Corrected soft drop mass with PUPPI", precision=10),
            btagCSVV2=Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')", float, doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)", precision=10),
            btagHbb=Var("bDiscriminator('pfBoostedDoubleSecondaryVertexAK8BJetTags')", float, doc="Higgs to BB tagger discriminator", precision=10),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
            subJetIdx1=Var("?nSubjetCollections()>0 && subjets().size()>0?subjets()[0].key():-1", int,
                 doc="index of first subjet"),
            subJetIdx2=Var("?nSubjetCollections()>0 && subjets().size()>1?subjets()[1].key():-1", int,
                 doc="index of second subjet"),
        )
    )
    run2_jme_2016.toModify(process.customAK8Table.variables, jetId=Var("userInt('tightId')*2+userInt('looseId')", int, doc="Jet ID flags bit1 is loose, bit2 is tight"))
    process.customAK8Table.variables.pt.precision = 10

    # add DeepAK8 scores: nominal
    for prob in _pfDeepBoostedJetTagsProbs:
        name = 'DeepAK8_' + prob.split(':')[1]
        setattr(process.customAK8Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    # add DeepAK8 scores: mass decorrelated
    for prob in _pfMassDecorrelatedDeepBoostedJetTagsProbs:
        name = 'DeepAK8MD_' + prob.split(':')[1]
        setattr(process.customAK8Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    # add ParticleNet nominal taggers
    for prob in _pfParticleNetJetTagsProbs:
        name = 'ParticleNet_' + prob.split(':')[1]
        setattr(process.customAK8Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    # add ParticleNet mass-decorelated taggers
    for prob in _pfMassDecorrelatedParticleNetJetTagsProbs:
        name = 'ParticleNetMD_' + prob.split(':')[1]
        setattr(process.customAK8Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    process.customAK8SubJetTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
        src=cms.InputTag("selectedPatJetsAK8PFPuppiSoftDropPacked", "SubJets"),
        cut=cms.string(""),
        name=cms.string("CustomAK8PuppiSubJet"),
        doc=cms.string("reculstered ak8 puppi subjets"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            btagDeepB=Var("bDiscriminator('pfDeepCSVJetTags:probb')+bDiscriminator('pfDeepCSVJetTags:probbb')", float, doc="DeepCSV b+bb tag discriminator", precision=10),
            btagCSVV2=Var("bDiscriminator('pfCombinedInclusiveSecondaryVertexV2BJetTags')", float, doc=" pfCombinedInclusiveSecondaryVertexV2 b-tag discriminator (aka CSVV2)", precision=10),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
        )
    )
    process.customAK8SubJetTable.variables.pt.precision = 10

    process.customizedAK8Task = cms.Task(
        process.tightJetIdCustomAK8,
        process.tightJetIdLepVetoCustomAK8,
        process.customAK8WithUserData,
        process.customAK8Table,
        process.customAK8SubJetTable
        )

    if runOnMC:
        process.customGenJetAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
            src=cms.InputTag("ak8GenJetsNoNu"),
            cut=cms.string("pt > 100."),
            name=cms.string("CustomGenJetAK8"),
            doc=cms.string("AK8 GenJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.customGenJetAK8Table.variables.pt.precision = 10

        process.customGenSubJetAK8Table = cms.EDProducer("SimpleCandidateFlatTableProducer",
            src=cms.InputTag("ak8GenJetsNoNuSoftDrop", "SubJets"),
            cut=cms.string(""),
            name=cms.string("CustomGenSubJetAK8"),
            doc=cms.string("AK8 Gen-SubJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.customGenSubJetAK8Table.variables.pt.precision = 10

        process.customizedAK8Task.add(process.customGenJetAK8Table)
        process.customizedAK8Task.add(process.customGenSubJetAK8Table)

    _customizedAK8Task_80X = process.customizedAK8Task.copy()
    _customizedAK8Task_80X.replace(process.tightJetIdLepVetoCustomAK8, process.looseJetIdCustomAK8)
    run2_jme_2016.toReplaceWith(process.customizedAK8Task, _customizedAK8Task_80X)

    if path is None:
        process.schedule.associate(process.customizedAK8Task)
    else:
        getattr(process, path).associate(process.customizedAK8Task)
