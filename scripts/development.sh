#!/bin/bash

exit_code=0

cd "$( dirname "${BASH_SOURCE[0]}" )"
cd '..'

echo "
********************************************************************************
*** Running Development for SpeechProcessor
********************************************************************************"

MAX_THREADS=3 INPUT_FILE='example_input.json' SPEECH_ENV='development' SUBS_LOCATION='file' python3 -v .
((exit_code+=$?))

exit $exit_code
