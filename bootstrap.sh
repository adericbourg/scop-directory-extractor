#!/usr/bin/env bash

VIRTUALENV_DIR=".venv"

if [[ ! -d ${VIRTUALENV_DIR} ]]; then
    echo "Creating virtualenv"
    virtualenv -p python3 ${VIRTUALENV_DIR}
fi

source ${VIRTUALENV_DIR}/bin/activate

if [[ -f "requirements.txt" ]]; then
    echo "Installing dependencies"
    pip install --upgrade -r requirements.txt
fi
if [[ -f "test-requirements.txt" ]]; then
    echo "Installing test dependencies"
    pip install --upgrade -r test-requirements.txt
fi

