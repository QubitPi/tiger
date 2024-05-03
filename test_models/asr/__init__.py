import logging

from flasgger import Swagger
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import os

from gradio_client import Client


def __inference_by_whisper_space():
    """
    Inferencing using https://huggingface.co/spaces/openai/whisper.

    supports wider variety of audio file types, including .wav, and .mp3

    :return: The transcribed audio text in string
    """
    f = request.files['audio']
    f.save(f.filename)

    client = Client("https://openai-whisper.hf.space/")
    result = client.predict(f.filename, "transcribe", api_name="/predict")

    os.remove(f.filename)

    return result


def __inference_by_speech_recognition():
    """
    Inferencing using https://github.com/Uberi/speech_recognition

    Supports inferencing beyond whisper, but audio file type is more restricted - support .wav but not .mp3

    :return: The transcribed audio text in string
    """
    import speech_recognition as sr

    f = request.files['audio']
    f.save(f.filename)

    r = sr.Recognizer()

    with sr.AudioFile(f.filename) as source:
        audio = r.record(source)

    os.remove(f.filename)

    return r.recognize_whisper(audio_data=audio, language="zh")


def create_app():
    app = Flask(__name__)

    CORS(app)

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)

    app.config['SWAGGER'] = {
        'title': 'Whisper ASR API',
        'openapi': '3.0.2'
    }
    Swagger(app)

    @app.route("/healthcheck")
    def hello():
        return "Success", 200

    @app.route("/model1", methods=["POST"])
    def model1():
        return __inference_by_whisper_space()

    @app.route("/model2", methods=["POST"])
    def model2():
        return __inference_by_speech_recognition()

    return app
