#!/bin/bash
#
# Update requirements.txt files to synchronize with "poetry.lock".

if [ ! -f "./ci/requirements.txt" ]; then
    echo "Wrong directory."
    exit 1
fi

HEADER="# $(poetry --version) export at $(date)"

echo "$HEADER" > ./ci/requirements.txt
poetry export >> ./ci/requirements.txt

echo "$HEADER" > ./ci/requirements-dev.txt
poetry export --dev >> ./ci/requirements-dev.txt

exit 0
