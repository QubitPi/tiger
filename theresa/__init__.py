from flask_cors import CORS
from flasgger import Swagger
from flask import Flask, request, jsonify

from theresa.entity_extraction.graph_gpt import entity_extraction
from theresa.expand.google_knowledge_graph_api import node_expand
from theresa.neo4j import json_parser


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_envvar("APP_CONFIG_FILE")

    app.config['SWAGGER'] = {
        'title': 'Theresa API',
        'openapi': '3.0.2'
    }
    Swagger(app)

    @app.route("/healthcheck")
    def hello():
        return "Success", 200

    @app.route("/neo4Json2Spec", methods = ["POST"])
    def neo4json_2_spec():
        """
        将 Neo4J Browser 的 JSON 图谱导出文件转换成一张 Nexus Graph 格式的知识图谱
        ---
        requestBody:
          description: A json
          required: true
          content:
            application/json:
              schema:
                type: object
                example:
                  [
                    {
                      "r":{
                        "elementType":"relationship",
                        "identity":2,
                        "start":0,
                        "end":1,
                        "type":"got interrupted by",
                        "properties":{

                        },
                        "elementId":"2",
                        "startNodeElementId":"0",
                        "endNodeElementId":"1"
                      },
                      "m":{
                        "elementType":"node",
                        "identity":1,
                        "labels":[
                          "Undefined"
                        ],
                        "properties":{
                          "name":"Hacker",
                          "description":"A person who eavesdrops communication",
                          "id":"attacker"
                        },
                        "elementId":"1"
                      },
                      "n":{
                        "elementType":"node",
                        "identity":0,
                        "labels":[
                          "Person"
                        ],
                        "properties":{
                          "name":"Bob",
                          "description":"A person who sends an email",
                          "label":"Person",
                          "id":"sender"
                        },
                        "elementId":"0"
                      }
                    },
                    {
                      "r":{
                        "elementType":"relationship",
                        "identity":3,
                        "start":1,
                        "end":2,
                        "type":"sends 'fake' message to alice",
                        "properties":{

                        },
                        "elementId":"3",
                        "startNodeElementId":"1",
                        "endNodeElementId":"2"
                      },
                      "m":{
                        "elementType":"node",
                        "identity":2,
                        "labels":[
                          "Person"
                        ],
                        "properties":{
                          "name":"Alice",
                          "description":"A person who receives a message",
                          "label":"Person",
                          "id":"receiver"
                        },
                        "elementId":"2"
                      },
                      "n":{
                        "elementType":"node",
                        "identity":1,
                        "labels":[
                          "Undefined"
                        ],
                        "properties":{
                          "name":"Hacker",
                          "description":"A person who eavesdrops communication",
                          "id":"attacker"
                        },
                        "elementId":"1"
                      }
                    }
                  ]
        responses:
          200:
            description: Success
        """
        return jsonify(json_parser.neo4json_2_spec(request.get_json()))

    @app.route("/entityExtraction", methods = ["POST"])
    def named_entity_extraction():
        """
        对一段文字进行知识抽取分析
        ---
        requestBody:
          description: |
            被分析的文字，支持中英文，可以是一个句子，也可以是一段话，内容格式和长度不限，用一个 JSON 表示，key = "text"，
            被分析的文字是 key 对应的值，例如：

            ```json
            {
                "text": "React is a free and open-source front-end JavaScript library"
            }
            ```
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  text:
                    type: string
                    required: true
                example:
                  text: "React is a free and open-source front-end JavaScript library"
        responses:
          200:
            description: Success
        """
        return jsonify(entity_extraction(request.get_json()["text"]))

    @app.route("/expand", methods = ["POST"])
    def expand():
        """
        对一个节点进行展开操作并返回与之相关的新节点和关系
        ---
        requestBody:
          description: |
            一个节点 JSON，JSON 必须包含 `id` 和 `fields` 两个属性

            - "id" 是这个节点的在一张图谱中的唯一标识
            - "fields" 是这个节点上的属性（即前端 NodeModel 中 "propertiesList" 里的 key-value pairs），
              "fields" 可以包含任何属性

            例如：

            ```json
            {
                "node": {
                    "fields": {
                      "anyOtherFields1": "foo",
                      "anyOtherFields2": "bar",
                      "name": "TypeScript"
                    },
                    "id": "TypeScript"
                }
            }
            ```

          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  node:
                    type: object
                    required: true
                    properties:
                      id:
                        type: string
                        required: true
                      fields:
                        type: object
                        required: true
                example:
                  node:
                    id: "TypeScript"
                    fields:
                      name: "TypeScript"
        responses:
          200:
            description: Success
        """
        return jsonify(node_expand(request.get_json()["node"]))

    return app
