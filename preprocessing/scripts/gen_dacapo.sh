#!/bin/bash
DACAPO_JAR=dacapo-23.11-chopin.jar
LOG_DIR=logs
APP_DIR=apps
JAVA=jdk/bin/java
TRACEFORMAT=jdk/bin/traceformat
TARGET=$1
REPS=$2
cd ..
mkdir ${LOG_DIR}
chmod +x jdk/bin/*
rm "${LOG_DIR}/${TARGET}_time.log"
cd ${APP_DIR}

for I in $(seq 1 5)
do 
    { echo "==============================================="; } &>> "../${LOG_DIR}/${TARGET}_time.log"
    { echo "../${LOG_DIR}/${TARGET}_trace_${I}.trc"; } &>> "../${LOG_DIR}/${TARGET}_time.log"
    # log tracepoint data to file (also logs output + time to ${TARGET}_time.log)
    { time "../${JAVA}" "-Xtrace:none,maximal=j9jit.93-95,buffers=30k,output=../${LOG_DIR}/${TARGET}_trace_${I}.trc" -jar $DACAPO_JAR ${TARGET}; } &>> "../${LOG_DIR}/${TARGET}_time.log"
    # convert binary tracepoint output to text
    "../${TRACEFORMAT}" "../${LOG_DIR}/${TARGET}_trace_${I}.trc"
    cd ..
    # generate the json data based on the tracepoint outputs
    python log2json.py -i "./${LOG_DIR}/${TARGET}_trace_${I}.trc.fmt"
    cd ${APP_DIR}
done
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print={j9jit.93-95}" "-Xjit:minSamplingPeriod=2" -jar $DACAPO_JAR ${1} 2> ${1}_trace_{}.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print={j9jit.13-14}" -jar $DACAPO_JAR ${1} 2> ${1}_sample.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print={j9jit.15-16}" -jar $DACAPO_JAR ${1} 2> ${1}_trace.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java -jar $DACAPO_JAR ${1} 
