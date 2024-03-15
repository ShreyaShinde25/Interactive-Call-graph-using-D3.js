#!/bin/bash
JAVA=../jdk/bin/java
JAVAC=../jdk/bin/javac
LOG_DIR=../logs
MSP=$1
$JAVAC HelloWorld.java
mkdir ${LOG_DIR}
for I in 1 2 3 4 5
do 
    $JAVA "-Xtrace:print={j9jit.93-96}" "-Xjit:minSamplingPeriod=${MSP}" HelloWorld 2> "${LOG_DIR}/hello_trace_msp${MSP}_${I}.log"
done
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:none,maximal=j9jit.15-16,output=hello5.trc" "-Xjit:minSamplingPeriod=5" HelloWorld 2> hello_trace5.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:none,maximal=j9jit.15-16,output=hello3.trc" "-Xjit:minSamplingPeriod=3" HelloWorld 2> hello_trace3.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:none,maximal=j9jit.15-16,output=hello2.trc" "-Xjit:minSamplingPeriod=2" HelloWorld 2> hello_trace2.log

# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print={j9jit.39-41}" "-Xjit:minSamplingPeriod=0" HelloWorld 2> 3941.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print={j9jit.15-16}" "-Xjit:minSamplingPeriod=0" HelloWorld 2> 1516.log

# $JAVA "-Xtrace:print={j9jit.93-95}" "-Xjit:minSamplingPeriod=0" HelloWorld 2> hello_trace.log

# $JAVA "-Xtrace:print={j9jit.93-95,mt},trigger=method{*.*,jstacktrace},stackdepth=2" HelloWorld 2> hello_trace1.log
# $JAVA "-Xtrace:print=mt,trigger=method{*.*,jstacktrace},stackdepth=2"  HelloWorld 2> hello_trace2.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print=j9jit.93-95,trigger=tpnid{j9jit.93,jstacktrace},stackdepth=2" HelloWorld 2> hello_trace.log
