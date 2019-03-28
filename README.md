# NanoTuples (Custom NanoAOD ntuple producers with DeepAK8 and DeepAK15)

### Set up CMSSW

```bash
cmsrel CMSSW_10_2_11
cd CMSSW_10_2_11/src
cmsenv
```

### Apply changes on PhysicsTools/NanoAOD

```bash
# pull updates from official NanoAOD repo
git cms-merge-topic -u cms-nanoAOD:master-102X

# this one adds the trigger prescale
# git cms-merge-topic -u hqucms:custom-nano-94X-add-trigger-prescales
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

MC (2016, 94X, MiniAODv3):

```bash
cmsDriver.py test_nanoHRT_mc2016 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 94X_mcRun2_asymptotic_v3 --step NANO --nThreads 4 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIISummer16MiniAODv3/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/80000/FEC61D42-F5F5-E811-8435-001E67A4061D.root --fileout file:nano_mc2016.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_mc2016.log &

less +F test_mc2016.log
```

Data (2016, 94X, MiniAODv3):

```bash
cmsDriver.py test_nanoHRT_data2016 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 94X_dataRun2_v10 --step NANO --nThreads 4 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2016H/MET/MINIAOD/17Jul2018-v2/00000/0A0B71F7-75B8-E811-BAB7-0425C5DE7BE4.root --fileout file:nano_data2016.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_data2016.log &

less +F test_data2016.log
```


MC (2017, 94X, MiniAODv2):

```bash
cmsDriver.py test_nanoHRT_mc2017 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 94X_mc2017_realistic_v17 --step NANO --nThreads 4 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIIFall17MiniAODv2/ZprimeToTT_M3000_W30_TuneCP2_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/50000/20FF99D9-702A-E911-B801-0025904CFB86.root --fileout file:nano_mc2017.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_mc2017.log &

less +F test_mc2017.log
```

Data (2017, 94X, MiniAODv2):

```bash
cmsDriver.py test_nanoHRT_data2017 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 94X_dataRun2_v11 --step NANO --nThreads 4 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2017D/JetHT/MINIAOD/31Mar2018-v1/60000/1EEE02D3-E539-E811-9859-0025905A6066.root --fileout file:nano_data2017.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_data2017.log &

less +F test_data2017.log
```

### Production [FIXME]

MC (80X, MiniAODv2):

```bash
cmsDriver.py mc -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 94X_mcRun2_asymptotic_v2 --step NANO --nThreads 4 --era Run2_2016,run2_miniAOD_80XLegacy --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (2016 ReReco):

```bash
cmsDriver.py data -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 94X_dataRun2_v4 --step NANO --nThreads 4 --era Run2_2016,run2_miniAOD_80XLegacy --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData_METMuEGClean --filein file:step-1.root --fileout file:nano.root --no_exec
```

To add trigger prescales,

```bash
cmsDriver.py data -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 94X_dataRun2_v4 --step NANO --nThreads 4 --era Run2_2016,run2_miniAOD_80XLegacy --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData_METMuEGClean_saveTriggerPrescale --filein file:step-1.root --fileout file:nano.root --no_exec
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

MC (80X, For use with 2016 Legacy data):

```bash
cmsDriver.py mc -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 94X_mcRun2_asymptotic_v3 --step NANO --nThreads 4 --era Run2_2016,run2_miniAOD_80XLegacy --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec

# test file: /store/mc/RunIISummer16MiniAODv2/ttHToCC_M125_TuneCUETP8M2_13TeV_powheg_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/106F8E1B-23ED-E711-9F58-0025905B861C.root
```

MC (94X, MiniAODv3):

```bash
cmsDriver.py mc -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 94X_mcRun2_asymptotic_v3 --step NANO --nThreads 4 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec

# test file: /store/mc/RunIISummer16MiniAODv3/QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/120000/00FFD8FF-0DE4-E811-8C2C-1866DA89035E.root
```
