#!/bin/bash
set -x
set -e

touch /home/ubuntu/aws-base-tf-init.log
export AWS_BASE_TF_INIT_LOG=/home/ubuntu/aws-base-tf-init.log
echo "aws-base-tf-init started executing..."       >>$AWS_BASE_TF_INIT_LOG 2>&1

sudo docker run --detach --rm \
  --memory=4000m \
  -p 5001:8080 \
  -v /home/ubuntu/theresa/mlflow_models/models/HanLPner:/opt/ml/model \
  -e GUNICORN_CMD_ARGS="--timeout 600 -k gevent --workers=1" \
  "entity-extraction"                              >>$AWS_BASE_TF_INIT_LOG 2>&1
echo "HanLP container started"                     >>$AWS_BASE_TF_INIT_LOG 2>&1

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
  -w 4 \
  -b 0.0.0.0 \
  --timeout 600 \
  --log-file /home/ubuntu/theresa/theresa.log \
  --log-level DEBUG \
  'theresa:create_app()'

echo "aws-base-tf-init finished executing"         >>$AWS_BASE_TF_INIT_LOG 2>&1
