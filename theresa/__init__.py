from flask_cors import CORS
from flasgger import Swagger
from flask import Flask, request, jsonify

from theresa.entity_extraction.hanlp_ner import entity_extraction
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
        Converts an exported knowledge graph from Neo4J Browser in JSON to a Knowledge Graph Spec
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
        Performs entity extraction on a text corpus
        ---
        requestBody:
          description: |
            The text being analyzed. It supports both Chinese and English. For example:

            ```json
            {
                "text": [
                    "React is a free and open-source front-end JavaScript library",
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
        Expand a node
        ---
        requestBody:
          description: |
            A node in JSON format, which must contain `id` and `fields` attributes. The `fields` itself is a JSON
            object

            - "id" is the unique identifier in a knowledge graph
            - "fields" is the properties of this node

            Example:

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
