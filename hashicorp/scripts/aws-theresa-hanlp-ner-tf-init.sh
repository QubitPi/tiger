#!/bin/bash
set -x
set -e

touch /home/ubuntu/aws-base-tf-init.log
export AWS_BASE_TF_INIT_LOG=/home/ubuntu/aws-base-tf-init.log
echo "aws-base-tf-init started executing..."       >>$AWS_BASE_TF_INIT_LOG 2>&1

touch /home/ubuntu/theresa/mlflow_models/models/HanLPner/__init__.py
mv /home/ubuntu/theresa/mlflow_models/HanLPner/parser.py /home/ubuntu/theresa/mlflow_models/models/HanLPner
sudo docker run --detach --rm \
  --memory=4000m \
  -p 5001:8080 \
  -e PYTHONPATH="/opt/ml/model:$PYTHONPATH" \
  -v /home/ubuntu/theresa/mlflow_models/models/HanLPner:/opt/ml/model \
  -e GUNICORN_CMD_ARGS="--timeout 600 -k gevent --workers=1" \
  "entity-extraction"                              >>$AWS_BASE_TF_INIT_LOG 2>&1
echo "HanLP container started"                     >>$AWS_BASE_TF_INIT_LOG 2>&1

echo "aws-base-tf-init finished executing"         >>$AWS_BASE_TF_INIT_LOG 2>&1
