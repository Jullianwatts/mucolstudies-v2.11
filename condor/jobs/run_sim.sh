#!/bin/bash

JOB_NUM=$1
INPUT_FILE=$2
OUTPUT_FILE=$3

SKIP_N=$((JOB_NUM * 100))

source /opt/setup_mucoll.sh

export LD_LIBRARY_PATH=/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/vdt-0.4.6-mfaghtw6c5v3hz4we6zsgal4zd3dodkg/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/root-6.36.04-knw3reqpsgef2g55677xcm5zbchab5lg/lib/root:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/k4marlinwrapper-00-12-anpkew3oi374uhaot3i2fnw3qvonfmzk/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/k4simdelphes-00-07-05-edatl3qf43pc2onj7kue267673pglcom/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/k4simgeant4-0.1.0pre16-lhrp5tdlsguuyesxkbreas3g22dvxrpz/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/k4gen-0.1pre14-ttv4snquoxisii6x5c7zshujyyoqpc4s/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/k4geo-00-23-dklehcszm7rspyzkfvnmnee4ergookmv/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/lcio-2.22.6-pm4avkqlnhxxrpypnu7rieazthmlcjyb/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/k4fwcore-main-lsd2rnhgcnesyrz7bjs2qqcyorwrj4k3/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/gaudi-40.0-ymmtt5oepr4k2jcqq6mn7mszlaljylpp/lib64:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/gaudi-40.0-ymmtt5oepr4k2jcqq6mn7mszlaljylpp/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/dd4hep-1.32.1-6xccwvvjhkgswcovflawvlg4qh7b2xlp/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/edm4hep-0.99.2-pgbagpruasjblipyza6xsc2auxvd63vt/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/podio-1.4.1-4csnxatk2ck5d4sbljidappxhzfnapkl/lib:/opt/spack/opt/spack/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/__spack_path_placeholder__/linux-x86_64/r-4.5.1-3ogyl5altmekznz7wmxepzwlyju7gzb6/rlib/R/lib:/.singularity.d/libs

COMPACT_FILE="$(pwd)/MAIA_v0_container/MAIA_v0.xml"
echo "Using compact file: ${COMPACT_FILE}"

sed -i "s|SIM.compactFile = .*|SIM.compactFile = \"${COMPACT_FILE}\"|" sim_steer_condor.py
echo "Job ${JOB_NUM}: skipping ${SKIP_N} events"
echo "Input:  ${INPUT_FILE}"
echo "Output: ${OUTPUT_FILE}"

ddsim \
  --inputFile ${INPUT_FILE} \
  --steeringFile sim_steer_condor.py \
  --outputFile ${OUTPUT_FILE} \
  --numberOfEvents 100 \
  --skipNEvents ${SKIP_N}
