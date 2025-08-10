#!/bin/bash


# Arg1 : Time limit
# Arg2 : Source file
# Arg3 : Bytecode file
# Arg4 : ABI file
# Arg5 : Main contract name
# Arg6 : Optional argument to pass

TOOLDIR=/home/test/tools/rlf/go/src/rlf
WORKDIR=/home/test/rlf-workspace
OUTDIR=/home/test/output

source /home/test/tools/rlf/venv/bin/activate

# Set up workdir
mkdir -p $WORKDIR
mkdir -p $WORKDIR/output
touch $WORKDIR/output/log.txt
# Preprocess
python3 /home/test/tools/rlf/preprocess/rlf_preprocess.py --source $2 --name $5 --proj $WORKDIR/proj --rlf $TOOLDIR
# Run rlf
cd $TOOLDIR
timeout $1s python3 -m rlf --proj $WORKDIR/proj --output_path $WORKDIR/output \
  --contract $5 --fuzzer reinforcement --limit 2000 --limit_time $1 --detect_bugs all > \
  $WORKDIR/output/stdout.txt 2>&1

mkdir -p $OUTDIR
# Move raw tc
mkdir -p $OUTDIR/raw_tc
mkdir -p $OUTDIR/raw_misc
cp $WORKDIR/output/tc_* $OUTDIR/raw_tc/
cp $WORKDIR/proj/build/contracts/*.json $OUTDIR/raw_misc/

# Move logs
mv $WORKDIR/output/log.txt $OUTDIR/log.txt
mv $WORKDIR/output/stdout.txt $OUTDIR/stdout.txt

# Move output
mv $WORKDIR/output $OUTDIR/testcase

deactivate