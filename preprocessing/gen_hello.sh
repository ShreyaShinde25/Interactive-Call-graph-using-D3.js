#!/bin/bash
MSP=1
LOG_DIR=./logs
cd ./sample_apps
# this script runs the program and generates the tracepoint outputs
./hello.sh ${MSP}
cd ..
for I in $(seq 1 5)
do
    # this script generates the json data based on the tracepoint outputs
    python log2json.py -i ${LOG_DIR}/hello_trace_msp${MSP}_${I}.log
done