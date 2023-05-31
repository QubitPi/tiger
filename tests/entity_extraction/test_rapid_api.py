import os
import json
from theresa.entity_extraction.rapid_api import transform_to_knowledge_graph_spec


def test_transform_to_knowledge_graph_spec():
    with open(os.path.join(os.path.dirname(__file__), "test-rapid-api.input.json")) as input:
        with open(os.path.join(os.path.dirname(__file__), "test-rapid-api.output.json")) as expected:
            assert transform_to_knowledge_graph_spec(json.loads(input.read())) == json.loads(expected.read())
