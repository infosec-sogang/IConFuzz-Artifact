#!/bin/bash

SCRIPTDIR=$(dirname $0)
OUTDIR=$(realpath $SCRIPTDIR/../output)
EXP_NAME="result-parameter"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <iterN>"
    exit
fi

if ls $OUTDIR/$EXP_NAME 1> /dev/null 2>&1; then
    echo "$OUTDIR/$EXP_NAME exists, please remove it."
    exit 1
fi

python $SCRIPTDIR/run_experiment.py B-IO IConFuzz 7200 $1 $OUTDIR $EXP_NAME "-a 5"
python $SCRIPTDIR/run_experiment.py B-IO IConFuzz 7200 $1 $OUTDIR $EXP_NAME "-a 10"
python $SCRIPTDIR/run_experiment.py B-IO IConFuzz 7200 $1 $OUTDIR $EXP_NAME "-a 20"
python $SCRIPTDIR/run_experiment.py B-IO IConFuzz 7200 $1 $OUTDIR $EXP_NAME "-a 40"

python $SCRIPTDIR/run_experiment.py B-ELSC IConFuzz 7200 $1 $OUTDIR $EXP_NAME "-a 5"
python $SCRIPTDIR/run_experiment.py B-ELSC IConFuzz 7200 $1 $OUTDIR $EXP_NAME "-a 10"
python $SCRIPTDIR/run_experiment.py B-ELSC IConFuzz 7200 $1 $OUTDIR $EXP_NAME "-a 20"
python $SCRIPTDIR/run_experiment.py B-ELSC IConFuzz 7200 $1 $OUTDIR $EXP_NAME "-a 40"
