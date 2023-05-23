from flask import Flask

import spacy
from flask import request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
nlp = spacy.load("en_core_web_sm")

@app.route("/")
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
