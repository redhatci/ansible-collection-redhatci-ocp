#!/bin/bash -eu
#
# Copyright (C) 2025 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Description: A shell script that collects example-cnf results

# TRex params
echo "*** TREX PARAMETERS ***"
echo
echo "Job duration (s): $TREX_DURATION"
echo "Packet rate: $TREX_PACKET_RATE"
echo "Packet size (B): $TREX_PACKET_SIZE"
echo
echo

# Retrieve pod names
TESTPMD_POD=$($OC_BINARY get pods -n "$APP_NAMESPACE" --selector='example-cnf-type=cnf-app' -o custom-columns=POD:.metadata.name --no-headers)
TREXCONFIG_POD=$($OC_BINARY get pods -n "$APP_NAMESPACE" --selector='example-cnf-type=pkt-gen' -o custom-columns=POD:.metadata.name --no-headers)
TREXAPP_POD=$($OC_BINARY get pods -n "$APP_NAMESPACE" --selector='example-cnf-type=pkt-gen-app' -o custom-columns=POD:.metadata.name --no-headers)

echo "*** EXAMPLE-CNF RESULTS ***"
echo

# Retrieve TestPMD results
echo "--- Last statistics reported by TestPMD ---"
echo
$OC_BINARY logs -n "$APP_NAMESPACE" "$TESTPMD_POD" | tail -n22
echo
echo

# Retrieve TRex results
## For these logs, we need some intermediate steps
echo "--- Last statistics reported by TestPMD ---"
echo

echo "> Server"
echo
INTERMEDIATE_FILE_NAME=trexconfig_logs.txt
$OC_BINARY logs -n "$APP_NAMESPACE" "$TREXCONFIG_POD" | tail -n60 > "$INTERMEDIATE_FILE_NAME"
TREXCONFIG_LOG_LINES=($(cat -n "$INTERMEDIATE_FILE_NAME" | grep "Per port" | awk '{print $1}'))
START_LINE=${TREXCONFIG_LOG_LINES[0]}
END_LINE=${TREXCONFIG_LOG_LINES[1]}
## This is the only command that prints something
tail -n+"$START_LINE" $INTERMEDIATE_FILE_NAME | head -n $((END_LINE-START_LINE-1))
rm $INTERMEDIATE_FILE_NAME
echo
echo

echo "> App"
echo
INTERMEDIATE_FILE_NAME=trexapp_logs.txt
$OC_BINARY logs -n "$APP_NAMESPACE" "$TREXAPP_POD" | tail -n60 > "$INTERMEDIATE_FILE_NAME"
START_LINE=$(cat -n "$INTERMEDIATE_FILE_NAME" | grep "Packets lost from 0 to 1" | awk '{print $1}')
## This is the only command that prints something
tail -n+"$START_LINE" $INTERMEDIATE_FILE_NAME
rm $INTERMEDIATE_FILE_NAME

echo
echo
echo "End of script"
