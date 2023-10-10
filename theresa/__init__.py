import logging

from flasgger import Swagger
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from theresa.entity_extraction.hanlp_ner import entity_extraction


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_envvar("APP_CONFIG_FILE")

    gunicorn_error_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.DEBUG)
    # app.logger.debug('this will show in the log')

    app.config['SWAGGER'] = {
        'title': 'Theresa API',
        'openapi': '3.0.2'
    }
    Swagger(app)

    @app.route("/healthcheck")
    def hello():
        return "Success", 200

    @app.route("/entityExtraction", methods=["POST"])
    def named_entity_extraction():
        """
        Performs entity extraction on a text corpus
        ---
        requestBody:
          description: |
            The text being analyzed. It supports both Chinese and English. For example:

            ```json
            {
                "text": [
                    "米哈游成立于2011年,致力于为用户提供美好的、超出预期的产品与内容。米哈游多年来秉持技术自主创新,坚持走原创精品之路,围绕原创IP打造了涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链。"
                ]
            }
            ```
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  text:
                    type: array
                    required: true
                example:
                  text: ["米哈游成立于2011年,致力于为用户提供美好的、超出预期的产品与内容。米哈游多年来秉持技术自主创新,坚持走原创精品之路,围绕原创IP打造了涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链。"]
        responses:
          200:
            description: Success
        """
        return jsonify(entity_extraction(request.get_json()["text"]))

    return app
