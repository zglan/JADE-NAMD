#!/bin/bash

rm *.log
rm fort*

bsub -q simul -n 1 -o mndo.log -e mndo.err -i mndo.inp /home/simul/zhuang/program/myfirstmndo/mndo99


