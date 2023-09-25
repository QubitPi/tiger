import json
import os
from unittest import TestCase

from theresa.neo4j.json_parser import _convert_to_spec_link
from theresa.neo4j.json_parser import _convert_to_spec_node
from theresa.neo4j.json_parser import _extract_link
from theresa.neo4j.json_parser import _extract_nodes
from theresa.neo4j.json_parser import neo4json_2_spec


def _load_neo4j_exported_json():
    with open(os.path.join(os.path.dirname(__file__), 'neo4j-export.json'), encoding="utf-8-sig") as file:
        return json.loads(file.read())


def _load_first_tuple():
    return _load_neo4j_exported_json()[0]


def _load_second_tuple():
    return _load_neo4j_exported_json()[1]


def _expected_hacker_node():
    return {
        "id": "1",
        "fields": {
            "name": "Hacker",
            "description": "A person who eavesdrops communication",
            "id": "attacker",
            "label": "Undefined"
        }
    }


def _expected_bob_node():
    return {
        "id": "0",
        "fields": {
            "name": "Bob",
            "description": "A person who sends an email",
            "id": "sender",
            "label": "Person"
        }
    }


def _expected_alice_node():
    return {
        "id": "2",
        "fields": {
            "name": "Alice",
            "description": "A person who receives a message",
            "id": "receiver",
            "label": "Person"
        }
    }


def _expected_bob_hacker_link():
    return {
        "id": "0",
        "source": "0",
        "target": "1",
        "fields": {
            "label": "got interrupted by"
        }
    }


def _expected_hacker_alice_link():
    return {
        "id": "1",
        "source": "1",
        "target": "2",
        "fields": {
            "label": "sends 'fake' message to Alice"
        }
    }


class TestJsonParser(TestCase):

    def test__convert_to_spec_node(self):
        self.assertEqual(_expected_hacker_node(), _convert_to_spec_node(_load_first_tuple()["m"]))

    def test__extract_nodes(self):
        self.assertEqual([_expected_hacker_node(), _expected_bob_node()], _extract_nodes(_load_first_tuple()))

    def test__convert_to_spec_link(self):
        self.assertEqual(_expected_bob_hacker_link(), _convert_to_spec_link(_load_first_tuple()["r"]))

    def test__extract_link(self):
        self.assertEqual(_expected_bob_hacker_link(), _extract_link(_load_first_tuple()))

    def test_neo4json_2_spec(self):
        self.assertEqual(
            {
                "nodes": [_expected_hacker_node(), _expected_bob_node(), _expected_alice_node()],
                "links": [_expected_bob_hacker_link(), _expected_hacker_alice_link()]
            },
            neo4json_2_spec(_load_neo4j_exported_json())
        )
