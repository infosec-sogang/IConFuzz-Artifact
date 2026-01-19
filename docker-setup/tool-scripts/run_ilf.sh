#!/bin/bash


# Arg1 : Time limit
# Arg2 : Source file
# Arg3 : Bytecode file
# Arg4 : ABI file
# Arg5 : Main contract name
# Arg6 : Optional argument to pass

TOOLDIR=/home/test/tools/ilf/go/src/ilf
WORKDIR=/home/test/ilf-workspace
OUTDIR=/home/test/output

source /home/test/tools/ilf/venv/bin/activate

# Set up workdir
mkdir -p $WORKDIR
mkdir -p $WORKDIR/output
touch $WORKDIR/output/log.txt
# Preprocess
python3 $TOOLDIR/preprocess/ilf_preprocess.py --source $2 --name $5 --proj $WORKDIR/proj --ilf $TOOLDIR
# Run ilf
cd $TOOLDIR
timeout $1s python3 -m ilf --log_to_file $WORKDIR/log --proj $WORKDIR/proj \
  --contract $5 --fuzzer imitation --model ./model --limit 1 $6 > \
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