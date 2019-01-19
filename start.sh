#!/bin/sh

cd `dirname $0`
ENV_DIR=venv

# Check venv
if ! [ -d ${ENV_DIR} ]; then
    echo "venv doesn't exist. creating one..."
    python -m venv ${ENV_DIR}
fi

# Update vscreen
git pull origin master && ${ENV_DIR}/bin/pip install -r requirements.txt

echo ""
echo "vscreen is ready"
${ENV_DIR}/bin/python main.py > out.log 2> err.log