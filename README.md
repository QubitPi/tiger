Theresa
=======

![Python Version Badge](https://img.shields.io/badge/Python-3.10-brightgreen?style=flat-square&logo=python&logoColor=white)

ASR (Automatic Speech Recognition)
----------------------------------

- [whisper](./mlflow_models/whisper)
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

### Fine-Tuning Whisper For Chinese ASR with 🤗 Transformers

#### Loading WhisperFeatureExtractor

Speech is represented by a 1-dimensional array that varies with time. The value of the array at any given time step is
the signal's amplitude at that point. From the amplitude information alone, we can reconstruct the frequency spectrum of
the audio and recover all acoustic features.

Since speech is continuous, it contains an infinite number of amplitude values. This poses problems for computer devices
which expect finite arrays. Thus, training should discretize speech signal by sampling values from our signal at fixed
time steps. The interval with which we sample our audio is known as the *sampling rate* and is usually measured in
samples/sec or Hertz (Hz). Sampling with a higher sampling rate results in a better approximation of the continuous
speech signal, but also requires storing more values per second.

It is crucial that we **match the sampling rate of our audio inputs to the sampling rate expected by our model**, as
audio signals with different sampling rates have very different distributions. Audio samples should only ever be
processed with the correct sampling rate. Failing to do so can lead to unexpected results! For instance, taking an audio
sample with a sampling rate of 16kHz and listening to it with a sampling rate of 8kHz will make the audio sound as
though it's in half-speed. In the same way, passing audio with the wrong sampling rate can falter an ASR model that
expects one sampling rate and receives another. The Whisper feature extractor expects audio inputs with a sampling rate
of 16kHz, so we need to match our inputs to this value. We don't want to inadvertently train an ASR system on
slow-motion speech!

The Whisper feature extractor performs 2 operations.

1. It first pads/truncates a batch of audio samples such that all samples have an input length of 30s. Samples shorter
   than 30s are padded to 30s by appending zeros to the end of the sequence (zeros in an audio signal corresponding to
   no signal or silence). Samples longer than 30s are truncated to 30s. Since all elements in the batch are
   padded/truncated to a maximum length in the input space, we don't require an attention mask when forwarding the audio
   inputs to the Whisper model. Whisper is unique in this regard - with most audio models, we can expect to provide an
   attention mask that details where sequences have been padded, and thus where they should be ignored in the
   self-attention mechanism. Whisper is trained to operate without an attention mask and infer directly from the speech
   signals where to ignore the inputs.
2. The second operation that the Whisper feature extractor performs is converting the padded audio arrays to log-Mel
   spectrograms. These spectrograms are a visual representation of the frequencies of a signal, rather like a Fourier
   transform. An example spectrogram is shown below. Along the ***y***-axis are the Mel channels, which correspond to
   particular frequency bins. Along the ***x***-axis is time. The colour of each pixel corresponds to the log-intensity
   of that frequency bin at a given time. The log-Mel spectrogram is the form of input expected by the Whisper model.


Entity Extraction
-----------------

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

```bash
cd ../../mlflow_models/models/HanLPner
mlflow models build-docker --name "entity-extraction"

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
> [Screwdriver](./screwdriver.yaml) MUST NOT auto-register to Kong because container startup takes time in a scale of
> more than 10 minutes. **We must manually register service using**:
> 
> ```bash
> export THERESA_EC2_PRIVATE_IP=172.31.10.191
> export KONG_PUBLIC_DNS=ec2-54-177-15-48.us-west-1.compute.amazonaws.com
> export SERVICE_NAME=theresa
> export ROUTE_NAME=analyze
> 
> curl -i -s -k -X POST https://${KONG_PUBLIC_DNS}:8444/services \
>   --data name=${SERVICE_NAME} \
>   --data url="http://${THERESA_EC2_PRIVATE_IP}:8080/invocations"
> 
> curl -i -k -X POST https://${KONG_PUBLIC_DNS}:8444/services/${SERVICE_NAME}/routes \
>   --data 'paths[]=/${ROUTE_NAME}' \
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
