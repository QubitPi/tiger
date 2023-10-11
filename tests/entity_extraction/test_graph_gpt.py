from unittest import TestCase
from types import SimpleNamespace
import json
from theresa.entity_extraction.graph_gpt import _construct_knowledge_graph_spec_link
from theresa.entity_extraction.graph_gpt import _construct_knowledge_graph_spec_node
from theresa.entity_extraction.graph_gpt import _convert_to_knowledge_graph_spec
from theresa.entity_extraction.graph_gpt import _transform_desc_to_prompt

class TestGraphGPT(TestCase):

    def test_making_knowledge_graph_node_from_extrapolated_result(self):
        self.assertEqual(
            {
                "id": "Earth",
                "fields": {
                    "label": "Earth",
                    "type": "entity"
                }
            },
            _construct_knowledge_graph_spec_node("Earth")
        )

    def test_making_knowledge_graph_link_from_extrapolated_result(self):
        self.assertEqual(
            {
                "source": "China",
                "target": "strong country",
                "fields": {
                    "label": "is a"
                }
            },
            _construct_knowledge_graph_spec_link("China", "strong country", "is a")
        )

    def test_convert_to_knowledge_graph_spec(self):
        response = {
            "text": json.dumps(
                {
                    "id": "fjrh-34fve4354gedsfzsdDFrgthbqere",
                    "object": "text_completion",
                    "created": 2673477357,
                    "model": "text-davinci-003",
                    "choices": [
                        {
                            "text": "[[\"Bob\", \"roommate\", \"Tom\"]]",
                            "index": 0,
                            "logprobs": None,
                            "finish_reason": "stop"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 106,
                        "completion_tokens": 13,
                        "total_tokens": 119
                    }
                }

            )
        }
        self.assertEqual(
            {
                "nodes": [
                    {'fields': {'label': 'Bob', 'type': 'entity'}, 'id': 'Bob'},
                    {'fields': {'label': 'Tom', 'type': 'entity'}, 'id': 'Tom'}
                ],
                "links": [
                    {'fields': {'label': 'roommate'}, 'source': 'Bob', 'target': 'Tom'}
                ]
            },
            _convert_to_knowledge_graph_spec(SimpleNamespace(**response))
        )

    def test_convert_to_knowledge_graph_spec_in_case_of_duplicate_nodes(self):
        response = {
            "text": json.dumps(
                {
                    "id": "fjrh-34fve4354gedsfzsdDFrgthbqere",
                    "object": "text_completion",
                    "created": 2673477357,
                    "model": "text-davinci-003",
                    "choices": [
                        {
                            "text": "[[\"Bob\", \"roommate\", \"Tom\"], [\"Any\", \"is sister of\", \"Bob\"]]",
                            "index": 0,
                            "logprobs": None,
                            "finish_reason": "stop"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 106,
                        "completion_tokens": 13,
                        "total_tokens": 119
                    }
                }

            )
        }
        self.assertEqual(
            [
                {'fields': {'label': 'Bob', 'type': 'entity'}, 'id': 'Bob'},
                {'fields': {'label': 'Tom', 'type': 'entity'}, 'id': 'Tom'},
                {'fields': {'label': 'Any', 'type': 'entity'}, 'id': 'Any'}
            ],
            _convert_to_knowledge_graph_spec(SimpleNamespace(**response))["nodes"]
        )

    def test_transform_desc_to_prompt(self):
        expected = """
Given a prompt, extrapolate as many relationships as possible from it and provide a list of updates.

If an update is a relationship, provide [ENTITY 1, RELATIONSHIP, ENTITY 2] in its original language. The relationship is directed, so the order matters.

Example:
prompt: Alice is Bob's roommate. Make her node green.
updates:
[["Alice", "roommate", "Bob"]]

prompt: Bob's roommate is Tom
updates:
"""
        self.assertEqual(expected, _transform_desc_to_prompt("Bob's roommate is Tom"))
