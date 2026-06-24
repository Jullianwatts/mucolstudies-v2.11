#!/bin/bash

JOB_NUM=$1
INPUT_FILE=$2
OUTPUT_FILE=$3
TYPE_EVENT=$4

source /opt/setup_mucoll.sh

export LD_LIBRARY_PATH="$(pwd)/LCContent_lib:$(pwd)/DDMarlinPandora_lib:${LD_LIBRARY_PATH}"
export MARLIN_DLL="$(pwd)/DDMarlinPandora_lib/libDDMarlinPandora.so:${MARLIN_DLL}"
export MARLIN_DLL=$(python3 -c "import os; print(os.environ.get('MARLIN_DLL', '').replace(':/DDMarlinPandora_lib/libDDMarlinPandora.so:', ':'))")

mkdir -p SteeringMacros
mv PandoraSettings SteeringMacros/

echo "Job ${JOB_NUM}: running reco"
echo "Input:  ${INPUT_FILE}"
echo "Output: ${OUTPUT_FILE}"
echo "TypeEvent: ${TYPE_EVENT}"
echo "Code dir: $(pwd)"

k4run steer_reco.py \
    --inputFile ${INPUT_FILE} \
    --outputFile ${OUTPUT_FILE} \
    --TypeEvent ${TYPE_EVENT} \
    --InFileName ${JOB_NUM} \
    --code $(pwd)
