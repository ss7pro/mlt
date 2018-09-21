
#!/bin/bash

inter=2

physical_cores=`lscpu | grep "Core(s) per socket" | cut -d':' -f2 | sed "s/ //g"`
num_sockets=`lscpu | grep "Socket(s)" | cut -d':' -f2 | sed "s/ //g"`
num_cores=$(( $physical_cores * $num_sockets ))

python main.py --num_inter_threads=${inter} --num_threads=$num_cores --no_horovod --data_path=${1} --output_path=${2}
