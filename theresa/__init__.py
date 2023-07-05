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
        对一个节点进行展开操作并返回与之相关的新节点和关系
        ---
        parameters:
          - name: node
            description: |
              一个节点对象，举例如下
              对象必须包含 "id" 和 "fields" 两个属性
              "id" 是这个节点的在一张图谱中的唯一标识
              "fields" 是这个节点上的属性（即前端 NodeModel 中 "propertiesList" 里的 key-value pairs），"fields" 可以包含任何属性
            in: query
            required: true
            type: object
            schema:
              type: object
              properties:
                id:
                  type: string
                  required: true
                fields:
                  type: object
                  required: true
              example:
                id: "TypeScript"
                fields:
                  name: "TypeScript"
                  anyOtherFields1: "foo"
                  anyOtherFields2: "bar"
        responses:
          200:
            description: 一张独立的知识图谱
          400 ~ 499:
            description: 前端请求参数不合法，请确保 "node" 传参和上面的举例一致
          500+:
            description: 后端服务异常，请通知 Jack 查看
        """
        return jsonify(node_expand(json.loads(request.args.get('node'))))

    return app
