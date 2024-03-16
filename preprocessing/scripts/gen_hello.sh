#!/bin/bash
MSP=0 # min sampling period used when generating tracepoint outputs
LOG_DIR=logs # log output directory
APP_DIR=apps # app directory
JAVA=jdk/bin/java # custom java binary
JAVAC=jdk/bin/javac # custom javac binary
cd ..
mkdir "${LOG_DIR}"
chmod +x ./jdk/bin/*
cd "${APP_DIR}"
"../$JAVAC" HelloWorld.java
for I in $(seq 1 5)
do
    # log tracepoint data to file
    "../${JAVA}" "-Xtrace:print={j9jit.93-96}" "-Xjit:minSamplingPeriod=${MSP}" HelloWorld 2> "../${LOG_DIR}/hello_trace_msp${MSP}_${I}.log"
    cd ..
    # generate the json data based on the tracepoint outputs
    python log2json.py -i "${LOG_DIR}/hello_trace_msp${MSP}_${I}.log"
    cd ${APP_DIR}
done