# NanoTuples (SV)

Custom NanoAOD ntuple producers with additional jet taggers and PF candidates.

<!-- TOC -->

- [NanoTuples (SV)](#nanotuples-sv)
    - [Version](#version)
    - [Setup](#setup)
        - [Set up CMSSW (Official NanoAODv9)](#set-up-cmssw-official-nanoaodv9)
        - [Set up CMSSW (Official NanoAODv9 + New ParticleNet with Tau)](#set-up-cmssw-official-nanoaodv9--new-particlenet-with-tau)
        - [Get customized NanoAOD producers](#get-customized-nanoaod-producers)
        - [Compile](#compile)
        - [Test](#test)
    - [Production](#production)

<!-- /TOC -->

---

## Version

The current version is based on [NanoAODv9](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv9).

Customizations:

- ParticleNetAK4 for AK4 jets
- PF candidates near soft SVs

---

## Setup
<!-- 
### Set up CMSSW (Official NanoAODv9)

```bash
cmsrel CMSSW_10_6_26
cd CMSSW_10_6_26/src
cmsenv
```
 -->
### Set up CMSSW (Official NanoAODv9 + New ParticleNet with Tau)

```bash
cmsrel CMSSW_10_6_30
cd CMSSW_10_6_30/src
cmsenv

git cms-merge-topic -u gouskos:pnet_ak8_new_collection
```

### Get customized NanoAOD producers

```bash
git clone https://github.com/hqucms/NanoTuples.git PhysicsTools/NanoTuples -b production/sv_tagging
```

### Compile

```bash
scram b -j16
```

### Test
<!-- 
MC (2016, 94X, MiniAODv3):

```bash
cmsDriver.py test_nanoTuples_mc2016 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_mcRun2_asymptotic_v8 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIISummer16MiniAODv3/TTToSemilepton_TuneCUETP8M2_ttHtranche3_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/80000/FEC61D42-F5F5-E811-8435-001E67A4061D.root --fileout file:nano_mc2016.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_mc2016.log &

less +F test_mc2016.log
```

Data (2016, 94X, MiniAODv3):

```bash
cmsDriver.py test_nanoTuples_data2016 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v13 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2016H/MET/MINIAOD/17Jul2018-v2/00000/0A0B71F7-75B8-E811-BAB7-0425C5DE7BE4.root --fileout file:nano_data2016.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_data2016.log &

less +F test_data2016.log
```

MC (2017, 94X, MiniAODv2):

```bash
cmsDriver.py test_nanoTuples_mc2017 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_mc2017_realistic_v8 --step NANO --nThreads 1 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIIFall17MiniAODv2/DY1JetsToLL_M-50_LHEZpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/60000/F492A0D0-3F56-E811-9387-FA163EB32A35.root --fileout file:nano_mc2017.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_mc2017.log &

less +F test_mc2017.log
```

Data (2017, 94X, MiniAODv2):

```bash
cmsDriver.py test_nanoTuples_data2017 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v13 --step NANO --nThreads 1 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2017F/SingleElectron/MINIAOD/31Mar2018-v1/90002/EC099452-C938-E811-9922-0CC47A7C354C.root --fileout file:nano_data2017.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_data2017.log &

less +F test_data2017.log
```
 -->
MC (UL18):

```bash
cmsDriver.py test_nanoTuples_mc2018 -n 1000 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein /store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/004EF875-ACBB-FE45-B86B-EAF83448CE62.root --fileout file:nano_mc2018.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_mc2018.log &

less +F test_mc2018.log
```

Data (UL18):

```bash
cmsDriver.py test_nanoTuples_data2018 -n 1000 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 106X_dataRun2_v35 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein /store/data/Run2018C/SingleMuon/MINIAOD/UL2018_MiniAODv2_GT36-v2/2530000/003EFE78-9748-DC43-BB97-14236C25C5FA.root --fileout file:nano_data2018.root --customise_commands "process.options.wantSummary = cms.untracked.bool(True)" >& test_data2018.log &

less +F test_data2018.log
```

---

## Production

**Step 0**: switch to the crab production directory and set up grid proxy, CRAB environment, etc.

```bash
cd $CMSSW_BASE/src/PhysicsTools/NanoTuples/crab
# set up grid proxy
voms-proxy-init -rfc -voms cms --valid 168:00
# set up CRAB env (must be done after cmsenv)
source /cvmfs/cms.cern.ch/common/crab-setup.sh
```

**Step 1**: generate the python config file with `cmsDriver.py` with the following commands:
<!-- 
MC (2016, 94X, MiniAODv3):

```bash
cmsDriver.py mc2016 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_mcRun2_asymptotic_v8 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (2016, 94X, MiniAODv3):

```bash
cmsDriver.py data2016 -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v13 --step NANO --nThreads 1 --era Run2_2016,run2_nanoAOD_94X2016 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```

MC (2017, 94X, MiniAODv2):

```bash
cmsDriver.py mc2017 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 102X_mc2017_realistic_v8 --step NANO --nThreads 1 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (2017, 94X, MiniAODv2):

```bash
cmsDriver.py data2017 -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 102X_dataRun2_v13 --step NANO --nThreads 1 --era Run2_2017,run2_nanoAOD_94XMiniAODv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```
 -->
MC (UL18):

```bash
cmsDriver.py mc2018 -n -1 --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_upgrade2018_realistic_v16_L1v1 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeMC --filein file:step-1.root --fileout file:nano.root --no_exec
```

Data (UL18):

```bash
cmsDriver.py data2018abc -n -1 --data --eventcontent NANOAOD --datatier NANOAOD --conditions 106X_dataRun2_v35 --step NANO --nThreads 1 --era Run2_2018,run2_nanoAOD_106Xv2 --customise PhysicsTools/NanoTuples/nanoTuples_cff.nanoTuples_customizeData --filein file:step-1.root --fileout file:nano.root --no_exec
```

**Step 2**: use the `crab.py` script to submit the CRAB jobs:

For MC:

`python crab.py -e cmsRun.sh -p mc_NANO.py --site T2_CH_CERN -o /store/user/$USER/outputdir -t NanoTuples-[version] -i mc.txt --num-cores 1 --send-external -s FileBased -n 2 --work-area crab_projects_mc --dryrun`

For data:

`python crab.py -e cmsRun.sh -p data_NANO.py --site T2_CH_CERN -o /store/user/$USER/outputdir -t NanoTuples-[version] -i data.txt --num-cores 1 --send-external -s EventAwareLumiBased -n 100000 -j [json_file] --work-area crab_projects_data --dryrun`

A JSON file can be applied for data samples with the `-j` options.

Golden JSON, UL16:

```
https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions16/13TeV/Legacy_2016/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt
```

Golden JSON, UL17:

```
https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt
```

Golden JSON, UL18:

```
https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt
```

These command will perform a "dryrun" to print out the CRAB configuration files. Please check everything is correct (e.g., the output path, version number, requested number of cores, etc.) before submitting the actual jobs. To actually submit the jobs to CRAB, just remove the `--dryrun` option at the end.

**Step 3**: check job status

The status of the CRAB jobs can be checked with:

```bash
./crab.py --status --work-area crab_projects_*  --options "maxjobruntime=2500 maxmemory=2500" && ./crab.py --summary
```

Note that this will also **resubmit** failed jobs automatically.

The crab dashboard can also be used to get a quick overview of the job status:

- [https://monit-grafana.cern.ch/d/cmsTMGlobal/cms-tasks-monitoring-globalview?orgId=11](https://monit-grafana.cern.ch/d/cmsTMGlobal/cms-tasks-monitoring-globalview?orgId=11)

More options of this `crab.py` script can be found with:

```bash
./crab.py -h
```
