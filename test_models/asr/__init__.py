import logging
import time
from functools import wraps

from flasgger import Swagger
from flask import Flask
from flask import request
from flask_cors import CORS

import os

def __inference_by_whisper_space(audio_path):
    """
    Inferencing using https://huggingface.co/spaces/openai/whisper.

    supports wider variety of audio file types, including .wav, and .mp3

    :param audio_path:  The local audio file path to transcribe

    :return: The transcribed audio text in string
    """
    from gradio_client import Client

    client = Client("https://openai-whisper.hf.space/")
    return client.predict(audio_path, "transcribe", api_name="/predict")

def __inference_by_speech_recognition(audio_path):
    """
    Inferencing using https://github.com/Uberi/speech_recognition

    Supports inferencing beyond whisper, but audio file type is more restricted - support .wav but not .mp3

    :param audio_path:  The local audio file path to transcribe

    :return: The transcribed audio text in string
    """
    import speech_recognition as sr

    r = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)

    return r.recognize_whisper(audio_data=audio, language="zh")


def random_filename(original_filename: str):
    return str(hash((original_filename, time.time())))

def with_uploaded_file(f):
    """
    Extracts uploaded file from HTTP request, saves the file to a random path, executes route logic, and always cleans
    up the file.

    See https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/ for more details

    :param f:  The route logic function
    :return:  The decorated route logic function with common file logics
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        uploaded_file = request.files['audio']
        file_path = random_filename(uploaded_file.filename)
        uploaded_file.save(file_path)
        kwargs["audio_path"] = file_path

        try:
            return f(*args, **kwargs)
        finally:
            os.remove(file_path)

    return decorated_function


def create_app():
    app = Flask(__name__)

    CORS(app)

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)

    app.config['SWAGGER'] = {
        'title': '派昂科技自动语音识别测试 API',
        'openapi': '3.0.2'
    }
    Swagger(app)

    @app.route("/healthcheck")
    def hello():
        return "Success", 200

    @app.route("/model1", methods=["POST"])
    @with_uploaded_file
    def model1(**kwargs):
        """
        使用 1 号基础模型将一段音频转译成文字格式。
        ---
        requestBody:
          content:
            multipart/form-data:
              schema:
                type: object
                properties:
                  audio:
                    type: string
                    format: binary
        responses:
          200:
            description: Success
        """
        return __inference_by_whisper_space(kwargs["audio_path"])

    @app.route("/model2", methods=["POST"])
    @with_uploaded_file
    def model2(**kwargs):
        """
        使用 2 号基础模型将一段音频转译成文字格式。
        ---
        requestBody:
          content:
            multipart/form-data:
              schema:
                type: object
                properties:
                  audio:
                    type: string
                    format: binary
        responses:
          200:
            description: Success
        """
        return __inference_by_speech_recognition(kwargs["audio_path"])

    return app
