import cv2
import math
import numpy
from flask import Flask, request, jsonify
from theresa.image.similarity import compare_two

import spacy
from flasgger import Swagger


def create_app():
    app = Flask(__name__)
    swagger = Swagger(app)
    nlp = spacy.load("en_core_web_sm")

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
        doc = nlp(request.args.get('sentence'))

        entity_map = {}
        for ent in doc.ents:
            # https://spacy.io/usage/linguistic-features#named-entities
            entity_map[ent.text] = ent.label_

        return entity_map

    @app.route('/image/similarity', methods=['POST'])
    def similarity():
        if request.method == 'POST':

            files = request.files.getlist("file")

            img = cv2.imdecode(numpy.frombuffer(files[0].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
            base_img = cv2.imdecode(numpy.frombuffer(files[1].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

            raw_results = compare_two(img, base_img)

            # filter out items with NaN and infinity values
            results = {k: str(v) for k, v in raw_results.items() if not (math.isinf(v) or math.isnan(v))}

            app.logger.warning("raw_results=%s", raw_results)
            app.logger.warning("result=%s", results)

            return jsonify(results)

    return app
