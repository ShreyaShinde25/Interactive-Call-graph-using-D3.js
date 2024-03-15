#!/bin/bash
DACAPO_JAR=./dacapo-23.11-chopin.jar
JAVA=../jdk/bin/java
for I in 1 2 3 4 5
do 
    { echo "${1}_trace93-96_${I}.trc"; } &>> ${1}_time.log
    { time $JAVA -jar $DACAPO_JAR ${1}; } &>> ${1}_time.log
done
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print={j9jit.93-95}" "-Xjit:minSamplingPeriod=2" -jar $DACAPO_JAR ${1} 2> ${1}_trace_{}.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print={j9jit.13-14}" -jar $DACAPO_JAR ${1} 2> ${1}_sample.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java "-Xtrace:print={j9jit.15-16}" -jar $DACAPO_JAR ${1} 2> ${1}_trace.log
# ./jdk11/build/linux-x86_64-normal-server-release/images/jdk/bin/java -jar $DACAPO_JAR ${1} 
