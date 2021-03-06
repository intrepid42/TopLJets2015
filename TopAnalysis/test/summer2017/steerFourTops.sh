#!/bin/bash

WHAT=$1; 
if [ "$#" -ne 1 ]; then 
    echo "steerFourTops.sh <SEL/MERGE/PLOT/WWW>";
    echo "        SEL          - launches selection jobs to the batch, output will contain summary trees and control plots"; 
    echo "        MERGE        - merge output"
    echo "        PLOT         - make plots"
    echo "        WWW          - move plots to web-based are"
    exit 1; 
fi

export LSB_JOB_REPORT_MAIL=N
queue=2nd
githash=b312177
lumi=35922
lumiUnc=0.025
whoami=`whoami`
myletter=${whoami:0:1}
eosdir=/store/cmst3/group/top/ReReco2016/${githash}
outdir=test/summer2017/FourTops
wwwdir=~/www/FourTops


RED='\e[31m'
NC='\e[0m'
case $WHAT in

    SEL )
        queue=local
	python scripts/runLocalAnalysis.py -i ${eosdir} \
            --only test/summer2017/4tops_samples.json --exactonly \
            -q ${queue} -o ${outdir} --njobs 8 \
            --era era2016 -m FourTopsAnalyzer::RunFourTopsAnalyzer --ch 0 --runSysts;
	;;

    MERGE )
	./scripts/mergeOutputs.py ${outdir};
	;;
    PLOT )
	commonOpts="-i ${outdir} --puNormSF puwgtctr -j test/summer2017/4tops_samples.json -l ${lumi}  --saveLog --mcUnc ${lumiUnc} --noStack"
	python scripts/plotter.py ${commonOpts}; 
	;;
    WWW )
	mkdir -p ${wwwdir}/sel
	cp ${outdir}/plots/*.{png,pdf} ${wwwdir}/sel
	cp test/index.php ${wwwdir}/sel
	;;
    DATACARD )

        #addBinByBin specifies if the threshold for which bin-by-bin uncertainties should be added
        #            30% relative stat unc is usually fine as threshold
        #rebin       helps to reduce stat fluctuations
        #specs       specifies the analysis line in python/xsecSystSpecs.py which defines which systematics
        #            should be assigned to each process

        python scripts/createDataCard.py \
            -i  /afs/cern.ch/user/p/psilva/public/forTop/plotter.root \
            --systInput /afs/cern.ch/user/p/psilva/public/forTop/syst_plotter.root \
            -o test/summer2017/datacard_4tops \
            --specs FourTops \
            --signal tbarttbart \
            -d bdt \
            -c "" \
            --rebin 10 \
            --addBinByBin 0.3            
         ;;
esac
