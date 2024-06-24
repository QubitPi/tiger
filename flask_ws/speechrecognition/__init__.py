import logging
import time
from functools import wraps

from flasgger import Swagger
from flask import Flask
from flask import request
from flask_cors import CORS
from flask import Request

import os

# https://stackoverflow.com/a/77964479
# This is actually not needed, but in case gunicorn can't take a large file, this becomes handy
class CustomRequest(Request):
    def __init__(self, *args, **kwargs):
        super(CustomRequest, self).__init__(*args, **kwargs)
        self.max_form_parts = 999999

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
    app.request_class = CustomRequest

    CORS(app)

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)

    app.config['SWAGGER'] = {
        'title': 'Theresa Speech Recognition Flask',
        'openapi': '3.0.2'
    }
    Swagger(app)

    @app.route("/healthcheck")
    def hello():
        return "Success", 200

    @app.route("/whisperHuggingFaceSpace", methods=["POST"])
    @with_uploaded_file
    def inference_by_whisper_huggingface_space(**kwargs):
        """
        Inferencing using https://huggingface.co/spaces/openai/whisper.

        supports wider variety of audio file types, including .wav, and .mp3
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
        from gradio_client import Client

        client = Client("https://openai-whisper.hf.space/")
        return client.predict(kwargs["audio_path"], "transcribe", api_name="/predict")

    @app.route("/speechrecognitionLibrary", methods=["POST"])
    @with_uploaded_file
    def inference_by_speechrecognition_library(**kwargs):
        """
        Inferencing using https://github.com/Uberi/speech_recognition

        Supports inferencing beyond whisper, but audio file type is more restricted - support .wav but not .mp3
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
        import speech_recognition as sr

        r = sr.Recognizer()

        with sr.AudioFile(kwargs["audio_path"]) as source:
            audio = r.record(source)

        return r.recognize_whisper(audio_data=audio, language="zh")

    return app
