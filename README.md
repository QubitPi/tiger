Theresa
=======

![Python Version Badge](https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white)

Entity Extraction
-----------------

[![AWS EC2 min size][AWS EC2 min size]](https://aws.amazon.com/ec2/instance-types/)

Create virtual environment and install dependencies:

```console
cd mlflow_models/HanLPner
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

Generate Model with

```console
python3 HanLPner.py
```

A model directory called "HanLPner" appears under `mlflow_models/models`. Then build Docker image

```console
mlflow models build-docker --name "entity-extraction"
```

and run container with

```console
cp parser.py ../../mlflow_models/models/HanLPner/
docker run --rm \
  --memory=4000m \
  -p 8080:8080 \
  -v /Users/jackjack/Desktop/github/theresa/mlflow_models/models/HanLPner:/opt/ml/model \
  -e PYTHONPATH="/opt/ml/model:$PYTHONPATH" \
  -e GUNICORN_CMD_ARGS="--timeout 60 -k gevent --workers=1" \
  "entity-extraction"
```

> [!TIP]
> If `docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))`
> error is seen, refer to https://forums.docker.com/t/docker-errors-dockerexception-error-while-fetching-server-api-version-connection-aborted-filenotfounderror-2-no-such-file-or-directory-error-in-python/135637/5

> [!WARNING]
> The number of gunicorn worker process MUST be **1** (`--workers=1`) to prevent multiple workers from downloading a
> HanLP pre-trained model to the same location, which results in runtime error in Docker container. In **native**
> environment, this error can be
> 
> ```bash
> OSError: [Errno 39] Directory not empty: '/root/.hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210304_135840'
> -> '/root/.hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159'
> ```

Example query (or [in Python](https://huggingface.co/spaces/QubitPi/named-entity-recognition/blob/main/app.py)):

```bash
curl -X POST -H "Content-Type:application/json" \
  --data '{"dataframe_split": {"columns":["text"], "data":[["我爱中国"], ["米哈游成立于2011年,致力于为用户提供美好的、超出预期的产品与内容。米哈游多年来秉持技术自主创新,坚持走原创精品之路,围绕原创IP打造了涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链。"]]}}' \
  http://127.0.0.1:8080/invocations
```

[Note the JSON schema of the `--data` value](https://stackoverflow.com/a/75104855)

Deployments
-----------

> [!CAUTION]
>
> [Screwdriver](./screwdriver.yaml) MUST NOT auto-register to Kong because container startup takes time in a scale of
> more than 10 minutes. **We must manually register service using**:
> 
> ```bash
> export THERESA_EC2_PRIVATE_IP=172.31.12.154
> export KONG_PUBLIC_DNS=ec2-52-9-19-226.us-west-1.compute.amazonaws.com
> export SERVICE_NAME=theresa-ner
> export ROUTE_NAME=theresa-ner
> 
> curl -i -s -k -X POST https://${KONG_PUBLIC_DNS}:8444/services \
>   --data name=${SERVICE_NAME} \
>   --data url="http://${THERESA_EC2_PRIVATE_IP}:8080/invocations"
> 
> curl -i -k -X POST https://${KONG_PUBLIC_DNS}:8444/services/${SERVICE_NAME}/routes \
>   --data "paths[]=/${ROUTE_NAME}" \
>   --data name=${ROUTE_NAME}
> ```
> 
> Then we can test routing with
> 
> ```bash
> curl -k -X POST -H "Content-Type:application/json" \
>   --data '{"dataframe_split": {"columns":["text"], "data":[["我爱中国"], ["米哈游成立于2011年,致力于为用户提供美好的、超出预期的产品与内容。米哈游多年  来秉持技术自主创新,坚持走原创精品之路,围绕原创IP打造了涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链。"]]}}' \
>   https://${KONG_PUBLIC_DNS}/${ROUTE_NAME}
> ```

ASR (Automatic Speech Recognition)
----------------------------------

- [asr-test.paion-data.dev](./test_models/asr)

ASR
---

Setup
-----

```console
python3 -m venv .venv
. .venv/bin/activate
pip3 install torch torchvision torchaudio
```

[AWS EC2 min size]: https://img.shields.io/badge/EC2-%E2%89%A5t2.large-FF9902?style=for-the-badge&logo=amazonec2&logoColor=white
