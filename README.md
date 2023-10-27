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
  -v $NER_MODEL_PATH:/opt/ml/model \
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

Example query:

```bash
curl -X POST -H "Content-Type:application/json" \
  --data '{"dataframe_split": {"columns":["text"], "data":[["我爱中国"], ["米哈游成立于2011年,致力于为用户提供美好的、超出预期的产品与内容。米哈游多年来秉持技术自主创新,坚持走原创精品之路,围绕原创IP打造了涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链。"]]}}' \
  http://127.0.0.1:5001/invocations
```

[Note the JSON schema of the `--data` value](https://stackoverflow.com/a/75104855)

Or in Python

```python
def _get_hanlp_results(texts: list[str]):
    import requests
    import json

    results = []

    url = "http://127.0.0.1:5001/invocations"

    for text in texts:
        payload = json.dumps({
            "dataframe_split": {
                "columns": ["text"],
                "data": [[text]]
            }
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        results.extend(response.json()["predictions"][0]["0"])

    return [results]
```

### World Model

The world model originated from
[Ha and Schmidhuber, 2018b; Matsuo et al., 2022](https://qubitpi.github.io/worldmodels.github.io/). Basically, human
develop a mental model of the world based on what we are able to perceive with our limited senses. The decisions and
actions we make are based on this internal model. The image of the world around us, which we carry in our head, is just
a _model_. Nobody in his head imagines all the world, government or country. We have only selected **concepts, and
relationships** between them, and uses those to represent the real system.

:::tip What is a World Model?

With respect to [llm-reasoners](https://github.com/QubitPi/llm-reasoners), a **world model** is a _repurposed LLM_,
which builds a reasoning graph. In this graph, a node is called a **state** and a link is called an **action**. _The LLM
generates the link_

:::

### Language Model as World Model

In general, a world model predicts the next state of the reasoning after applying an action to the current state.
[RAP](https://github.com/QubitPi/RAP) enables us to instantiate the general concepts of state and action in different
ways depending on the specific reasoning problems at hand. 

With the definition of state and action, the reasoning process can thus be described as a
[Markov decision process (MDP)](./MDP.pdf): given the current state $s_{t,t=0,1,...,T}$ , e.g., the initial state $s_0$,
the LLM (as a **reasoning agent**) generates an action space by sampling from its generative distribution
$a_t ∼ p(a|s_t,c)$, where $c$ is a proper prompt (e.g., in-context demonstrations). Once an action is chosen, the world
model then predicts the next state $s_{t+1}$ of the reasoning. Specifically, we repurpose the same LLM to obtain a state
transition distribution $p(s_{t+1}|s_t, a_t, c')$, where c' is another prompt to guide the LLM to generate a state.

Continuing the process results in a reasoning trace, which consists of a sequence of interleaved states and actions
$(s_0, a_0, s_1, . . . , a_{T-1}, s_T)$. Note that the full reasoning trace is simulated by the LLM itself (as a
reasoning agent with an internal world model) without interacting with the external real environment. This resembles
humans contemplating a possible plan in their minds. The capability of simulating future states, by introducing the
world model, allows us to incorporate principled planning algorithms to efficiently explore the vast reasoning space

