#!/bin/bash

conda_env=${3}

inter=2

physical_cores=`lscpu | grep "Core(s) per socket" | cut -d':' -f2 | sed "s/ //g"`
num_sockets=`lscpu | grep "Socket(s)" | cut -d':' -f2 | sed "s/ //g"`
num_cores=$(( $physical_cores * $num_sockets ))

if [ -n "${conda_env}" ]
 then
     echo -e "\nActivating ${conda_env}\n"
     source ~/.bashrc
     conda activate ${conda_env}
fi

python main.py --num_inter_threads=${inter} --num_threads=$num_cores --no_horovod --data_path=${1} --output_path=${2}

if [ -n "${conda_env}" ]
 then
     echo -e "\nDeactivating ${conda_env}\n"
     conda deactivate
fi