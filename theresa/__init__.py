from flask_cors import CORS
from flasgger import Swagger
from flask import Flask, request, jsonify
from theresa.entity_extraction.rapid_api import entity_extraction
from theresa.entity_extraction.rapid_api import transform_to_knowledge_graph_spec


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_envvar("APP_CONFIG_FILE")

    swagger = Swagger(app)

    @app.route("/sanityCheck")
    def hello():
        return "Success"

    @app.route("/entityExtraction")
    def named_entity_extraction():
        """
        This endpoint returns the Named Entity Recognition result of a sentence
        ---
        parameters:
          - name: sentence
            in: query
            type: string
            required: true
        responses:
          200:
            description: A mapping from sentence word to its label
        """
        rapid_api_result = entity_extraction([request.args.get('sentence')])
        return jsonify(transform_to_knowledge_graph_spec(rapid_api_result))

    return app
