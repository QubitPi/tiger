#!/bin/bash
set -x

touch /home/ubuntu/aws-base-tf-init.log
export AWS_BASE_TF_INIT_LOG=/home/ubuntu/aws-base-tf-init.log
echo "aws-base-tf-init started executing..."       >>$AWS_BASE_TF_INIT_LOG 2>&1

sudo nginx -t                                      >>$AWS_BASE_TF_INIT_LOG 2>&1
sudo nginx -s reload                               >>$AWS_BASE_TF_INIT_LOG 2>&1
echo "nginx init done..."                          >>$AWS_BASE_TF_INIT_LOG 2>&1

cd /home/ubuntu/theresa
alias python3=python3.10
python3 -m venv .venv                              >>$AWS_BASE_TF_INIT_LOG 2>&1
. .venv/bin/activate                               >>$AWS_BASE_TF_INIT_LOG 2>&1
echo "python init done..."                         >>$AWS_BASE_TF_INIT_LOG 2>&1
export APP_CONFIG_FILE=/home/ubuntu/settings.cfg   >>$AWS_BASE_TF_INIT_LOG 2>&1
python3 -m pip install .                           >>$AWS_BASE_TF_INIT_LOG 2>&1
gunicorn \
  -w 1 \
  -b 0.0.0.0 \
  --log-file /home/ubuntu/theresa/theresa.log \
  --log-level DEBUG \
  'theresa:create_app()'

echo "aws-base-tf-init finished executing"         >>$AWS_BASE_TF_INIT_LOG 2>&1
