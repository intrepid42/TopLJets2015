#!/bin/bash

WHAT=$1; 
if [ "$#" -ne 1 ]; then 
    echo "steerTTZAnalyzer.sh <SEL/MERGE/PLOT/WWW>";
    echo "        FULLSEL      - launches selection jobs to the batch, output will contain summary trees and control plots"; 
    echo "        SEL          - launches a test selection job locally for the signal only"
    echo "        MERGE        - merge output"
    echo "        PLOT         - make plots"
    echo "        WWW          - move plots to web-based are"
    exit 1; 
fi
githash=b312177
lumi=35922
lumiUnc=0.025
whoami=`whoami`
myletter=${whoami:0:1}
eosdir=/store/cmst3/group/top/ReReco2016/${githash}
outdir=${CMSSW_BASE}/src/TopLJets2015/TopAnalysis/test/summer2017/TTZAnalyzer
wwwdir=~/www/TTZAnalyzer


RED='\e[31m'
NC='\e[0m'
case $WHAT in

    SEL )
        #to run locally use "--njobs 8 -q local"
        #to run on the batck use "-q condor"
        #input=/store/cmst3/group/top/ReReco2016/b312177/MC13TeV_WZTo3LNu/MergedMiniEvents_0.root
        #output=test_ttz.root
        input=${eosdir}
        output=${outdir}
	python scripts/runLocalAnalysis.py -i ${input}\
            --only test/summer2017/ttz_samples.json --exactonly \
            --njobs 1 -q local \
            -o ${output} \
            --era era2016 -m TTZAnalyzer::RunTTZAnalyzer --ch 0 --runSysts;
	;;
    FULLSEL )
	python scripts/runLocalAnalysis.py -i ${eosdir} \
            --only test/summer2017/ttz_fullsamples.json --exactonly \
            -q workday \
            -o ${outdir} \
            --era era2016 -m TTZAnalyzer::RunTTZAnalyzer --ch 0 --runSysts;
	;;
    MERGE )
	./scripts/mergeOutputs.py ${outdir};
	;;
    PLOT )
	commonOpts="-i ${outdir} --puNormSF puwgtctr -j test/summer2017/ttz_samples.json -l ${lumi}  --saveLog --mcUnc ${lumiUnc} --noStack"
	python scripts/plotter.py ${commonOpts}; 
	;;
    FULLPLOT )
	commonOpts="-i ${outdir} --puNormSF puwgtctr -j test/summer2017/ttz_fullsamples.json -l ${lumi}  --saveLog --mcUnc ${lumiUnc}"
	python scripts/plotter.py ${commonOpts}; 
	;;
    WWW )
	mkdir -p ${wwwdir}/sel
	cp ${outdir}/plots/*.{png,pdf} ${wwwdir}/sel
	cp test/index.php ${wwwdir}/sel
	;;
esac
