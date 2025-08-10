#!/bin/bash

SCRIPTDIR=$(dirname $0)
OUTDIR=$(realpath $SCRIPTDIR/../output)
EXP_NAME="result-ELSC-compare"

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <iterN>"
    exit
fi

if ls $OUTDIR/$EXP_NAME 1> /dev/null 2>&1; then
    echo "$OUTDIR/$EXP_NAME exists, please remove it."
    exit 1
fi

# Run IConFuzz, smartian, SmarTest, and rlf.
python $SCRIPTDIR/run_experiment.py B-ELSC IConFuzz 3600 $1 $OUTDIR $EXP_NAME
python $SCRIPTDIR/run_experiment.py B-ELSC smartian 3600 $1 $OUTDIR $EXP_NAME
python $SCRIPTDIR/run_experiment.py B-ELSC SmarTest 3600 $1 $OUTDIR $EXP_NAME
python $SCRIPTDIR/run_experiment.py B-ELSC rlf 3600 $1 $OUTDIR $EXP_NAME