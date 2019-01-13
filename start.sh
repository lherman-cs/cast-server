#!/bin/sh

cd `dirname $0`
ENV_DIR=venv

# Update vscreen
git pull origin master

# Check venv
if ! [ -d ${ENV_DIR} ]; then
    echo "venv doesn't exist. creating one..."
    python -m venv ${ENV_DIR}
    ${ENV_DIR}/bin/pip install -r requirements.txt
fi

echo ""
echo "vscreen is ready"
${ENV_DIR}/bin/python main.py