#!/bin/bash

# Arg1 : Time limit
# Arg2 : Source file
# Arg3 : Bytecode file
# Arg4 : ABI file
# Arg5 : Main contract name
# Arg6, Arg7, Arg8 : Optional argument to pass

mkdir -p /home/test/output
cd /home/test/tools/IConFuzz/ && \
dotnet /home/test/tools/IConFuzz/build/IConFuzz.dll fuzz \
  --useothersoracle -s 0.4.25 -t $1 -p $2 -m $5 -v 1 $6 $7 $8 -o /home/test/output \
  > /home/test/output/log.txt 2>&1