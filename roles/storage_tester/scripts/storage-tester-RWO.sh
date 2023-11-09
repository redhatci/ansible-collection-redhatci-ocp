#!/usr/bin/env bash

set -e
set -x

echo ">>> Quick gathering object info in the Namespace of test"
$OC_PATH get all -n storage-tester -o wide

echo ">> Gathering logs from tester pod"
JSON=$(printf '{"spec":{"containers":[{"command":["tail","-f","/dev/null"],"image":"%s/rhel8/support-tools","name":"tmp-rwo-pod","volumeMounts":[{"mountPath":"/data-to-gather","name":"volume"}]}],"volumes":[{"name":"volume","persistentVolumeClaim":{"claimName":"storage-upgrade-tester-rwo"}}]}}' "$REGISTRY")
$OC_PATH run tmp-rwo-pod -n storage-tester --image=dummy --restart=Never --overrides="$JSON"
$OC_PATH wait -n storage-tester --for=condition=Ready pod/tmp-rwo-pod --timeout=180s
RESULT=$($OC_PATH rsh -n storage-tester tmp-rwo-pod cat /data-to-gather/test.txt)
$OC_PATH delete pod -n storage-tester tmp-rwo-pod
echo ""

echo ">> Gathering Content of the result file in the persistent Volume"
echo "$RESULT"


TEST_TIME=$($OC_PATH get job/init-pv -n storage-tester --no-headers | awk '{print $4}')
echo ""
echo ">>>>>>> RESULTS:"
echo "> Time of the test: $TEST_TIME"
TIME_NORMALIZED=$(echo "$TEST_TIME" | sed -E 's/h/hours /g' | sed -E 's/m/minutes /g')
SECOND=$(date -ud "19700101 $TIME_NORMALIZED" +%s)
NB_TRY=$(bc <<< "scale=0 ; $SECOND / 60")
NB_SUCCESS=$(echo "$RESULT" | wc -l)
FAILS=$(( NB_TRY - NB_SUCCESS ))
echo "> Number of estimated failures during this time: $FAILS"

PERCENT=$(bc <<< "scale=3 ; $FAILS/$NB_TRY*100")
echo "> Estimated percentage of failure: $PERCENT"
DOWN=$(bc <<< "scale=1 ; $SECOND * $PERCENT / 100 / 60")
echo "> Estimated downtime in Minutes: $DOWN"
echo ""

echo "> Filling JUNIT report $1"
DATE=$(date --rfc-3339=seconds)

sed -i -E "s/(DATE)/$DATE/g" "$1"
sed -i -E "s/(TEST_TIME)/$SECOND/g" "$1"
sed -i -E "s/(NB_TRY_RWO)/$NB_TRY/g" "$1"
sed -i -E "s/(NB_SUCCESS_RWO)/$NB_SUCCESS/g" "$1"
sed -i -E "s/(DOWN_RWO)/$DOWN/g" "$1"
sed -i -E "s/(FAILS_RWO)/$FAILS/g" "$1"
sed -i -E "s/(PERCENT_RWO)/$PERCENT/g" "$1"

echo ">>> Gathering YAML details object info in the Namespace of test"
$OC_PATH get all -n storage-tester -o yaml
echo ""
