#!/bin/bash
set -x
set -e

touch /home/ubuntu/asr/theresa.log
export THERESA_LOG=/home/ubuntu/asr/theresa.log
echo "Flask server starting..."  >>$THERESA_LOG 2>&1

cd /home/ubuntu
alias python3=python3.10
python3 -m venv .venv            >>$THERESA_LOG 2>&1
. .venv/bin/activate             >>$THERESA_LOG 2>&1
echo "Python 3.10 init done..."  >>$THERESA_LOG 2>&1

gunicorn \
  -w 4 \
  -b 0.0.0.0 \
  --timeout 600 \
  --limit-request-line 0 \
  --log-file asr/theresa.log \
  --log-level DEBUG \
  'asr:create_app()'
