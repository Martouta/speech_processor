#!/bin/bash

exit_code=0

cd "$( dirname "${BASH_SOURCE[0]}" )"
cd '..'

echo "
********************************************************************************
*** Running Test for SpeechProcessor
********************************************************************************"

SPEECH_ENV=test python3 -m pytest tests --tb=native --show-capture=all --verbosity=1 -rP -k tiktok
((exit_code+=$?))

exit $exit_code
