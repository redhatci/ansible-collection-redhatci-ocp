#!/bin/bash

set -e
set -x

echo ">>> Quick gathering object info in the Namespace of test"
$OC_PATH get all -n storage-tester -o wide | grep rox
echo ""
echo ">>>>>>> RESULTS:"
TEST_TIME=$($OC_PATH get job/init-pv -n storage-tester --no-headers | awk '{print $4}')
echo "> Time of the test: $TEST_TIME"

FAILS=$($OC_PATH get job -n storage-tester --no-headers | grep rox | grep -vc "2/1 of 2")
echo "> Number of failures during this time: $FAILS"

TIME_NORMALIZED=$(echo $TEST_TIME | sed -E 's/h/hours /g' | sed -E 's/m/minutes /g')
SECOND=$(date -ud "19700101 $TIME_NORMALIZED" +%s)
NB_TRY=$(bc <<< "scale=0 ; $SECOND / 60")
PERCENT=$(bc <<< "scale=3 ; $FAILS / $NB_TRY * 100")
SUCCESS=$(expr $NB_TRY - $FAILS)
echo "> Estimated percentage of failure: $PERCENT"
DOWN=$(bc <<< "scale=1 ; $SECOND * $PERCENT / 100 / 60")
echo "> Estimated downtime in Minutes: $DOWN"
echo ""

echo "> Filling JUNIT report $1"
sed -i -E "s/(NB_TRY_ROX)/$NB_TRY/g" "$1"
sed -i -E "s/(NB_SUCCESS_ROX)/$SUCCESS/g" "$1"
sed -i -E "s/(DOWN_ROX)/$DOWN/g" "$1"
sed -i -E "s/(FAILS_ROX)/$FAILS/g" "$1"
sed -i -E "s/(PERCENT_ROX)/$PERCENT/g" "$1"
echo ""
