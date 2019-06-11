# NanoTuples (Custom NanoAOD ntuple producers with DeepAK8 and DeepAK15)

### Set up CMSSW

```bash
cmsrel CMSSW_10_2_15
cd CMSSW_10_2_15/src
cmsenv
```

### Apply changes on PhysicsTools/NanoAOD

```bash
# pull updates from official NanoAOD repo
# git cms-merge-topic -u cms-nanoAOD:master-102X

# no longer needed in CMSSW_10_2_15
# git clone https://github.com/cms-nanoAOD/PhysicsTools-NanoAOD.git $CMSSW_BASE/external/$SCRAM_ARCH/data/PhysicsTools/NanoAOD/data

# this one adds the trigger prescale
# git cms-merge-topic -u hqucms:custom-nano-94X-add-trigger-prescales
```

### Get customized NanoAOD producers

```bash
git clone ssh://git@gitlab.cern.ch:7999/hqu/NanoTuples.git PhysicsTools/NanoTuples -b 102X
```

### Compile

```bash
scram b -j16
```

### Test

MC (2016, 94X, MiniAODv3):

```bash
cmsDriver.py test_nanoTuples_mc2016 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_mcRun2_asymptotic_v7 --step NANO --nThreads 4 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIISummer16MiniAODv3/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/80000/FEC61D42-F5F5-E811-8435-001E67A4061D.root --fileout file:nano_mc2016.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_mc2016.log &

less +F test_mc2016.log
```

Data (2016, 94X, MiniAODv3):

```bash
cmsDriver.py test_nanoTuples_data2016 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v11 --step NANO --nThreads 4 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2016H/MET/MINIAOD/17Jul2018-v2/00000/0A0B71F7-75B8-E811-BAB7-0425C5DE7BE4.root --fileout file:nano_data2016.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_data2016.log &

less +F test_data2016.log
```


MC (2017, 94X, MiniAODv2):

```bash
cmsDriver.py test_nanoTuples_mc2017 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_mc2017_realistic_v7 --step NANO --nThreads 4 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIIFall17MiniAODv2/ZprimeToTT_M3000_W30_TuneCP2_13TeV-madgraphMLM-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/50000/20FF99D9-702A-E911-B801-0025904CFB86.root --fileout file:nano_mc2017.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_mc2017.log &

less +F test_mc2017.log
```

Data (2017, 94X, MiniAODv2):

```bash
cmsDriver.py test_nanoTuples_data2017 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v11 --step NANO --nThreads 4 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2017D/JetHT/MINIAOD/31Mar2018-v1/60000/1EEE02D3-E539-E811-9859-0025905A6066.root --fileout file:nano_data2017.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_data2017.log &

less +F test_data2017.log
```


MC (2018, 102X):

```bash
cmsDriver.py test_nanoTuples_mc2018 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_upgrade2018_realistic_v19 --step NANO --nThreads 4 --era Run2_2018,run2_nanoAOD_102Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIIAutumn18MiniAOD/ZprimeToTT_M3000_W30_TuneCP2_PSweights_13TeV-madgraphMLM-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/90000/1CFAC15C-895C-CD44-BC86-58EE90CBF456.root --fileout file:nano_mc2018.root --customise_commands "process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))" >& test_mc2018.log &

less +F test_mc2018.log
```


### Production

**Step 0**: switch to the crab production directory and set up grid proxy, CRAB environment, etc.

```bash
cd $CMSSW_BASE/src/PhysicsTools/NanoTuples/crab
# set up grid proxy
voms-proxy-init -rfc -voms cms --valid 168:00
# set up CRAB env (must be done after cmsenv)
source /cvmfs/cms.cern.ch/crab3/crab.sh
```

**Step 1**: generate the python config file with `cmsDriver.py` with the following commands:


MC (2016, 94X, MiniAODv3):

```bash
cmsDriver.py mc2016 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_mcRun2_asymptotic_v7 --step NANO --nThreads 4 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (2016, 94X, MiniAODv3):

```bash
cmsDriver.py data2016 -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v11 --step NANO --nThreads 4 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```


MC (2017, 94X, MiniAODv2):

```bash
cmsDriver.py mc2017 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_mc2017_realistic_v7 --step NANO --nThreads 4 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (2017, 94X, MiniAODv2):

```bash
cmsDriver.py data2017 -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v11 --step NANO --nThreads 4 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```

MC (2018, 102X):

```bash
cmsDriver.py mc2018 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_upgrade2018_realistic_v19 --step NANO --nThreads 4 --era Run2_2018,run2_nanoAOD_102Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (2018ABC, 102X):

```bash
cmsDriver.py data2018abc -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v11 --step NANO --nThreads 4 --era Run2_2018,run2_nanoAOD_102Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (2018D, 102X):

```bash
cmsDriver.py data2018d -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_Prompt_v14 --step NANO --nThreads 4 --era Run2_2018,run2_nanoAOD_102Xv1 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```


**Step 2**: use the `crab.py` script to submit the CRAB jobs:

For MC:

`python crab.py -p mc_NANO.py -o /store/user/$USER/outputdir -t NanoTuples-[version] -i mc_[ABC].txt --num-cores 4 -s EventAwareLumiBased -n 100000 --work-area crab_projects_mc_[ABC] --dryrun`

For data:

`python crab.py -p data_NANO.py -o /store/user/$USER/outputdir -t NanoTuples-[version] -i data.txt --num-cores 4 -s EventAwareLumiBased -n 100000 --work-area crab_projects_data --dryrun`


A JSON file can be applied for data samples with the `-j` options.

Golden JSON, 2016:

```
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
```

Golden JSON, 2017:

```
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt
```

Golden JSON, 2018:

```
https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt
```

These command will perform a "dryrun" to print out the CRAB configuration files. Please check everything is correct (e.g., the output path, version number, requested number of cores, etc.) before submitting the actual jobs. To actually submit the jobs to CRAB, just remove the `--dryrun` option at the end.

**Step 3**: check job status

The status of the CRAB jobs can be checked with:

```bash
./crab.py --status --work-area crab_projects_[ABC]
```

Note that this will also resubmit failed jobs automatically.

The crab dashboard can also be used to get a quick overview of the job status:
`https://dashb-cms-job.cern.ch/dashboard/templates/task-analysis`

More options of this `crab.py` script can be found with:

```bash
./crab.py -h
```

