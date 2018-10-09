# NanoHRT

### Set up CMSSW

```bash
cmsrel CMSSW_9_4_10
cd CMSSW_9_4_10/src
cmsenv
```

### Hack NanoAOD framework (when running over 94X MiniAODv3)

```bash
# git cms-addpkg PhysicsTools/NanoAOD

# comment out L183 of PhysicsTools/NanoAOD/python/nano_cff.py
# run2_nanoAOD_94X2016.toModify(process, nanoAOD_addDeepFlavourTagFor94X2016) 
```

### Set up DeepAK15

```bash
# MXNet
scram setup /cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_3_0_pre4/config/toolbox/slc6_amd64_gcc700/tools/selected/mxnet-predict.xml
# get DeepAK8 PR
###git cms-merge-topic -u hqucms:deep-boosted-jets-rebase-94X
# this one contains also the updated EGM corrections for electron/photons
git cms-merge-topic -u hqucms:deep-boosted-jets-94X-custom-nano
git cms-addpkg RecoBTag/Combined
mkdir RecoBTag/Combined/data
cp -r /cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/data-RecoBTag-Combined/V01-00-14/RecoBTag/Combined/data/DeepBoostedJet RecoBTag/Combined/data/ 
```

### Get customized NanoAOD producers

```bash
git clone ssh://git@gitlab.cern.ch:7999/hqu/NanoTuples.git PhysicsTools/NanoTuples
```

### Compile

```bash
scram b -j16
```

### Test

```bash
cd PhysicsTools/NanoHRT/test
cmsRun nanoHRT_cfg.py
```

### Production

MC (80X, MiniAODv2):

```bash
cmsDriver.py mc -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 94X_mcRun2_asymptotic_v2 --step NANO --nThreads 4 --era Run2_2016,run2_miniAOD_80XLegacy --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec

# test file: /store/mc/RunIISummer16MiniAODv2/ttHToCC_M125_TuneCUETP8M2_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/106F8E1B-23ED-E711-9F58-0025905B861C.root
```

Data (2016 ReReco):

```bash
cmsDriver.py data -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 94X_dataRun2_v4 --step NANO --nThreads 4 --era Run2_2016,run2_miniAOD_80XLegacy --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec

# test file: /store/data/Run2016H/MET/MINIAOD/03Feb2017_ver3-v1/80000/2A9DE5C7-ADEA-E611-9F9C-008CFA111290.root
```


JSON:

```
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
```

Data (2016 Legacy):

```bash
cmsDriver.py data -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 94X_dataRun2_v10 --step NANO --nThreads 4 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec

# test file: /store/data/Run2016H/MET/MINIAOD/17Jul2018-v2/00000/0A0B71F7-75B8-E811-BAB7-0425C5DE7BE4.root
```

MC (For use with 2016 Legacy data):

```bash
cmsDriver.py mc -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 94X_mcRun2_asymptotic_v3 --step NANO --nThreads 4 --era Run2_2016,run2_miniAOD_80XLegacy --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec

# test file: /store/mc/RunIISummer16MiniAODv2/ttHToCC_M125_TuneCUETP8M2_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/106F8E1B-23ED-E711-9F58-0025905B861C.root
```


