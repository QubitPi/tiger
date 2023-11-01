Theresa <sup>![Python Version Badge](https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white)</sup>
=======

MLflow
------

### Entity Extraction

Create virtual environment and install dependencies:

```bash
cd mlflow_models/HanLPner
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

Generate Model with

```bash
python3 HanLPner.py
```

A model directory called "HanLPner" appears under `mlflow_models/models`. Then build Docker image and run container with

> If `docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))`
> error is seen, refer to https://forums.docker.com/t/docker-errors-dockerexception-error-while-fetching-server-api-version-connection-aborted-filenotfounderror-2-no-such-file-or-directory-error-in-python/135637/5

```bash
cd ../../mlflow_models/models/HanLPner
mlflow models build-docker --name "entity-extraction"

source ~/.bashrc # load $NER_MODEL_PATH
docker run --rm \
  --memory=4000m \
  -p 5001:8080 \
  -v /abs/path/to/theresa/mlflow_models/models/HanLPner:/opt/ml/model \
  -e PYTHONPATH="/opt/ml/model:$PYTHONPATH" \
  -e GUNICORN_CMD_ARGS="--timeout 60 -k gevent --workers=1" \
  "entity-extraction"
```

> ⚠️⚠️⚠️
> 
> The number of gunicorn worker process MUST be **1** (`--workers=1`) to prevent multiple workers from downloading a
> HanLP pre-trained model to the same location, which results in runtime error in Docker container. In **native**
> environment, this error can be
> 
> ```bash
> OSError: [Errno 39] Directory not empty: '/root/.hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210304_135840'
> -> '/root/.hanlp/mtl/close_tok_pos_ner_srl_dep_sdp_con_electra_small_20210111_124159'
> ```
> 
> ⚠️⚠️⚠️

Example query (or [in Python](https://huggingface.co/spaces/QubitPi/named-entity-recognition/blob/main/app.py)):

```bash
curl -X POST -H "Content-Type:application/json" \
  --data '{"dataframe_split": {"columns":["text"], "data":[["我爱中国"], ["米哈游成立于2011年,致力于为用户提供美好的、超出预期的产品与内容。米哈游多年来秉持技术自主创新,坚持走原创精品之路,围绕原创IP打造了涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链。"]]}}' \
  http://127.0.0.1:5001/invocations
```

[Note the JSON schema of the `--data` value](https://stackoverflow.com/a/75104855)

### Topological Sort

Generate Model with

```bash
cd mlflow_models/Planner
python3 Planner.py
```

```bash
curl -X POST -H "Content-Type:application/json" \
  --data '{"dataframe_split": {"columns":["text"], "data":[["{\"D\": [\"B\", \"C\"], \"C\": [\"A\"], \"B\": [\"A\"]}"]]}}' \
  http://localhost:5002/invocations
```
