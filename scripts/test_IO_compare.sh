#!/bin/bash

SCRIPTDIR=$(dirname $0)
OUTDIR=$(realpath $SCRIPTDIR/../output)
EXP_NAME="result-IO-compare"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <iterN>"
    exit
fi

if ls $OUTDIR/$EXP_NAME 1> /dev/null 2>&1; then
    echo "$OUTDIR/$EXP_NAME exists, please remove it."
    exit 1
fi

# Run IConFuzz, smartian, and SmarTest.
python $SCRIPTDIR/run_experiment.py B-IO IConFuzz 3600 $1 $OUTDIR $EXP_NAME
python $SCRIPTDIR/run_experiment.py B-IO smartian 3600 $1 $OUTDIR $EXP_NAME
python $SCRIPTDIR/run_experiment.py B-IO SmarTest 3600 $1 $OUTDIR $EXP_NAME
