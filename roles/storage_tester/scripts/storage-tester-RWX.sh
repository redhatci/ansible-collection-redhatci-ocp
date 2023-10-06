#!/bin/bash

set -e
set -x

echo ">>> Quick gathering object info in the Namespace of test"
$OC_PATH get all -n storage-tester -o wide

echo ">> Gathering info from mounted volume"
JSON="{\"spec\":{\"containers\":[{\"command\":[\"tail\",\"-f\",\"/dev/null\"],\"image\":\"$REGISTRY/rhel8/support-tools\",\"name\":\"tmp-pod\",\"volumeMounts\":[{\"mountPath\":\"/data-to-gather\",\"name\":\"volume\"}]}],\"volumes\":[{\"name\":\"volume\",\"persistentVolumeClaim\":{\"claimName\":\"storage-upgrade-tester-rwx\"}}]}}"
$OC_PATH run tmp-pod -n storage-tester --image=dummy --restart=Never --overrides=$JSON
$OC_PATH wait -n storage-tester --for=condition=Ready pod/tmp-pod --timeout=240s
# each writer will write a different file name
# so the number of files in the volume is the number of successful jobs (divided by 2)
NB_FILES=$($OC_PATH rsh -n storage-tester tmp-pod ls -1 /data-to-gather | wc -l)
$OC_PATH delete pod -n storage-tester tmp-pod

TEST_TIME=$($OC_PATH get job/init-pv -n storage-tester --no-headers | awk '{print $4}')
echo ""
echo ">>>>>>> RESULTS:"
echo "> Time of the test: $TEST_TIME"
TIME_NORMALIZED=$(echo $TEST_TIME | sed -E 's/h/hours /g' | sed -E 's/m/minutes /g')
SECOND=$(date -ud "19700101 $TIME_NORMALIZED" +%s)
NB_TRY=$(bc <<< "scale=0 ; $SECOND / 60")
FAILS=$(expr $NB_TRY '*' 2 - $NB_FILES)
echo "> Number of estimated failures during this time: $FAILS"

PERCENT=$(bc <<< "scale=3 ; $FAILS/$NB_TRY/2*100")
echo "> Estimated percentage of failure: $PERCENT"
DOWN=$(bc <<< "scale=1 ; $SECOND * $PERCENT / 100 / 60")
echo "> Estimated downtime in Minutes: $DOWN"
echo ""

echo "> Filling JUNIT report $1"
sed -i -E "s/(NB_TRY_RWX)/$NB_TRY/g" "$1"
sed -i -E "s/(NB_SUCCESS_RWX)/$NB_FILES/g" "$1"
sed -i -E "s/(FAILS_RWX)/$FAILS/g" "$1"
sed -i -E "s/(DOWN_RWX)/$DOWN/g" "$1"
sed -i -E "s/(PERCENT_RWX)/$PERCENT/g" "$1"
echo ""