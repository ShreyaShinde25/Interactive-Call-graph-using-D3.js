#!/bin/bash
PREFIX=${1}
OUT_DIR=out
cd ..
python pairwise_diff.py --prefix "${PREFIX}" --dir ${OUT_DIR}