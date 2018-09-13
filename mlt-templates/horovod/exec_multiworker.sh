#!/bin/bash

# Execute training on each node, pulling local thread counts for the train script
cd /src/app

export physical_cores=`lscpu | grep "Core(s) per socket" | cut -d':' -f2 | sed "s/ //g"` # Total number of physical cores per socket

export num_threads=$(( ${1} * $physical_cores )) # Total number of physical cores on this machine

python main.py --num_inter_threads=${2} --num_threads=$num_threads --data_path=${3} --output_path=${4}

