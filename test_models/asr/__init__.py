import logging

from flasgger import Swagger
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

import os

from gradio_client import Client

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

    @app.route("/asr", methods=["POST"])
    def asr():
        f = request.files['audio']
        f.save(f.filename)

        client = Client("https://openai-whisper.hf.space/")
        result = client.predict(f.filename, "transcribe", api_name="/predict")

        os.remove(f.filename)

        return jsonify(result)

    return app
