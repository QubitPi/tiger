from flask import Flask

import spacy
from flask import request

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/")
def hello_world():
    doc = nlp(request.args.get('sentence'))

    entity_map = {}
    for ent in doc.ents:
        # https://spacy.io/usage/linguistic-features#named-entities
        entity_map[ent.text] = ent.label_

    return entity_map
