import ast
import json
import requests
from requests import Response
from flask import current_app # https://stackoverflow.com/a/32017603

PROMPT_TEMPLATE = """
Given a prompt, extrapolate as many relationships as possible from it and provide a list of updates.

If an update is a relationship, provide [ENTITY 1, RELATIONSHIP, ENTITY 2] in its original language. The relationship is directed, so the order matters.

Example:
prompt: Alice is Bob's roommate. Make her node green.
updates:
[["Alice", "roommate", "Bob"]]

prompt: {}
updates:
"""


def _construct_knowledge_graph_spec_node(extrapolated_entity: str):
    return {
        "id": extrapolated_entity,
        "fields": {
            "label": extrapolated_entity,
            "type": "entity"
        }
    }


def _construct_knowledge_graph_spec_link(source: str, target: str, extrapolated_relationship: str):
    return {
        "source": source,
        "target": target,
        "fields": {
            "label": extrapolated_relationship
        }
    }


def _remove_duplicates(nodes: list) -> list:
    """
    De-duplicates nodes by node.id and returns a new list of unique nodes.

    :param nodes:  The node list with potential duplicaets

    :return: a list of nodes with unique id's
    """
    return list({node["id"]: node for node in nodes}.values())


def _convert_to_knowledge_graph_spec(response):
    """
    Given the completion API (https://platform.openai.com/docs/api-reference/completions) response, this method
    extracts the response data and converts the data to Knowledge Graph Spec format.

    :param response:  A regular python 'response' object whose response data can be retrieved via
    'json.loads(response.text)'

    :return: a Knowledge Graph Spec parsed out of the response
    """
    rdf_pairs = ast.literal_eval(json.loads(response.text)["choices"][0]["text"])

    nodes = []
    links = []

    for rdf_pair in rdf_pairs:
        if len(rdf_pair) == 2:
            nodes.append(_construct_knowledge_graph_spec_node(rdf_pair[0]))
            nodes.append(_construct_knowledge_graph_spec_node(rdf_pair[1]))
        else:
            nodes.append(_construct_knowledge_graph_spec_node(rdf_pair[0]))
            nodes.append(_construct_knowledge_graph_spec_node(rdf_pair[2]))
            links.append(_construct_knowledge_graph_spec_link(rdf_pair[0], rdf_pair[2], rdf_pair[1]))

    nodes = _remove_duplicates(nodes)

    return {
        "nodes": nodes,
        "links": links
    }


def _entity_extraction_via_completion_api(prompt: str) -> Response:
    """
    Queries the Completion API (https://platform.openai.com/docs/api-reference/completions) to perform the entity
    extraction.

    A single API request can only process up to 4,096 tokens between your prompt and completion.

    Although openai library (https://github.com/openai/openai-quickstart-python/blob/master/app.py) is there, let's
    keep Theresa SIMPLE by eliminating dependencies as much as possible
    (https://ramsrigoutham.medium.com/why-choose-python-requests-over-python-client-for-libraries-3454c92670ae). For
    this reason, we do simple CURL

    :param prompt:  The API notion's of prompt

    :return: a regular python 'response' whose response data can be retrieved via 'json.loads(response.text)'
    """
    url = "https://api.openai.com/v1/completions"

    payload = {
        "model": "text-davinci-003",
        "temperature": 0.3,
        "max_tokens": 800,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "prompt": prompt
    }

    return requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + current_app.config['OPEN_AI_API_KEY']
        },
        data=json.dumps(payload)
    )


def _transform_desc_to_prompt(knowledge_graph_desc: str) -> str:
    """
    Embeds a specified knowledge graph description into a completion prompt

    :param knowledge_graph_desc:  A natural language text corpus

    :return: PROMPT_TEMPLATE instantiated by the provided specified knowledge graph
    """
    return PROMPT_TEMPLATE.format(knowledge_graph_desc)


def entity_extraction(text: str):
    prompt = _transform_desc_to_prompt(text)
    response = _entity_extraction_via_completion_api(prompt)
    return _convert_to_knowledge_graph_spec(response)


if __name__ == '__main__':
    pass
