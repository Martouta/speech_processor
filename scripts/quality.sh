#!/bin/bash

exit_code=0

cd "$( dirname "${BASH_SOURCE[0]}" )"

echo "
********************************************************************************
*** Running code quality checkers for SpeechProcessor
********************************************************************************"

echo "
********************** Running PyLint on App **********************
"
pylint ../app --rcfile=../app/.pylintrc

((exit_code+=$?))

exit $exit_code
