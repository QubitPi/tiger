from flask_cors import CORS
import json
from flasgger import Swagger
from flask import Flask, request, jsonify
from theresa.entity_extraction.rapid_api import entity_extraction
from theresa.entity_extraction.rapid_api import transform_to_knowledge_graph_spec
from theresa.expand.google_knowledge_graph_api import node_expand


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

    @app.route("/expand")
    def expand():
        """
        给定一个节点的名称（label），对这个节点进行展开操作并返回与之相关的新节点和关系
        ---
        parameters:
          - name: node
            in: query
            type: object
            properties:
              id:
                type: string
              fields:
                type: object
            required: true
        responses:
          200:
            description: 一张独立的知识图谱
        """
        return jsonify(node_expand(json.loads(request.args.get('node'))))

    return app
