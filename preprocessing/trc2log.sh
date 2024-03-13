#!/bin/bash
# convinience script for converting .trc file to text format
# NOTE: we need to use custom jdk for this part (due to custom tracepoints)
./jdk/bin/traceformat $1