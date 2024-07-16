Speech Recognition REST API via Python Flask Webservice (No Model)
==================================================================

![Error loading frontend-dev-design.png](../../img/flask-speechrecognition.png)

Two "models" are offered in this API

1. [openai/whisper](https://huggingface.co/spaces/openai/whisper)

   - This is an un-fine tuned official model
   - [QubitPi backup](https://huggingface.co/spaces/QubitPi/whisper)

2. [SpeechRecognition Python Library (Whisper recognizer)](https://github.com/QubitPi/speech_recognition)

Development
-----------

- Swagger can only be accessed by me

### Setup

```console
cd flask_ws/speechrecognition
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
```

### Start Prod Server

```console
touch theresa.log
gunicorn \
  -w 4 \
  -b 0.0.0.0 \
  --timeout 600 \
  --limit-request-line 0 \
  --log-file theresa.log \
  --log-level DEBUG \
  'asr:create_app()'
```

### Example Request - Transcribing Audio

> [!TIP]
>
> - This curl was generated from Postman. It's very helpful to
> [make it work on Postman](https://galaxyofai.com/how-to-send-audio-files-to-flask-api-using-postman/) and have it
> generate curl for us
> - [Test audio download](https://www.kaggle.com/datasets/pavanelisetty/sample-audio-files-for-speech-recognition)

```console
curl --location 'localhost:8000/whisperHuggingFaceSpace' --form 'audio=@"/abs/path/to/test.wav"'
```

```console
curl --location 'localhost:8000/speechrecognitionLibrary' --form 'audio=@"/abs/path/to/test.wav"'
```

Deployment (Manual)
-------------------

> [!WARNING]
> 
> - The accumulating logs will eventually fill up disk space on EC2!
> - This Flask service already uses [`CustomRequest`](./__init__.py) to handle large audio file upload, 
> - if this Flask service is, however, behind a proxy like Nginx, we must put a `custom.conf` under
>   __/etc/nginx/conf.d/custom.conf__ in order to
> 
>   1. [Allow longer transcription time](https://stackoverflow.com/a/54605177)
>   2. Allow big upload audio file
>
>   ```
>   # All custom configs are in this file
>   # https://stackoverflow.com/a/54605177
>   # https://docs.nginx.com/nginx/admin-guide/basic-functionality/managing-configuration-files/
>   
>   client_max_body_size 100000M;
>   
>   proxy_connect_timeout 6000;
>   proxy_send_timeout 6000;
>   proxy_read_timeout 6000;
>   send_timeout 6000;
>   ```

[Set AWS credentials first](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-build)
(paion-data-ami-and-ec2-manager). This is already done in `~/.bashrc`. Simply make sure `source ~/.bashrc` is done

```console
cd flask_ws/hashicorp/images/speechrecognition
packer init .
packer validate .
packer build .

cd ../../instances/speechrecognition/
terraform init
terraform validate
terraform apply -auto-approve
```

> [!TIP]
>
> [Test audio download](https://www.kaggle.com/datasets/pavanelisetty/sample-audio-files-for-speech-recognition)

### Nginx (If SSL is needed)

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;

    server_name _;

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    root /var/www/html;

    index index.html index.htm index.nginx-debian.html;
    server_name asr-test.paion-data.dev;

    location / {
        proxy_pass http://localhost:8000;
    }

    location /apidocs {
        proxy_pass http://localhost:8000/apidocs;
        allow 13.57.13.209;
        allow 54.153.21.51;
        deny all;
    }

    listen [::]:443 ssl ipv6only=on;
    listen 443 ssl;
    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;
}
server {
    if ($host = asr-test.paion-data.dev) {
        return 301 https://$host$request_uri;
    }

    listen 80 ;
    listen [::]:80 ;
    server_name asr-test.paion-data.dev;
    return 404;
}
```
