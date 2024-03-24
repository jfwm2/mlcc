#!/usr/bin/env bash

VENV_NAME=mlcc
VENV_DIR="venv-${VENV_NAME}"

if [ -n "$ZSH_VERSION" ]; then
   SCRIPT_DIR="${(%):-%N}"
elif [ -n "$BASH_VERSION" ]; then
   SCRIPT_DIR="${BASH_SOURCE[0]}"
else
   echo "Unsupported shell."
   exit 1
fi

BASEDIR=$(dirname -- "${SCRIPT_DIR}")
if [ ! -f "${BASEDIR}/${VENV_DIR}/bin/python3" ]; then
  rm -Rf ${BASEDIR}/${VENV_DIR}
  python3 -m venv "${BASEDIR}/${VENV_DIR}" --copies --prompt ${VENV_NAME}
fi
source ${BASEDIR}/${VENV_DIR}/bin/activate
pip install -r requirements.txt
pip install -r tests-requirements.txt
python3 "${BASEDIR}/setup.py" develop
