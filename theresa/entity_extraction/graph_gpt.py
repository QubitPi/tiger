import ast
import json
import requests
from requests import Response
from flask import current_app # https://stackoverflow.com/a/32017603

PROMPT_TEMPLATE = """
Given a prompt, extrapolate as many relationships as possible from it and provide a list of updates.

If an update is a relationship, provide [ENTITY 1, RELATIONSHIP, ENTITY 2] and translate it into Chinese. The relationship is directed, so the order matters.

Example:
prompt: Alice is Bob's roommate. Make her node green.
updates:
[["Alice", "roommate", "Bob"]]

prompt: PROMPT_CONTENTS
updates:
"""


def _convert_to_knowledge_graph_spec(response):
    """
    Given the completion API (https://platform.openai.com/docs/api-reference/completions) response, this method
    extracts the response data and converts the data to Knowledge Graph Spec format.

    :param response:  A regular python 'response' object whose response data can be retrieved via
    'json.loads(response.text)'

    :return: a Knowledge Graph Spec parsed out of the response
    """
    rdf_pairs = ast.literal_eval(json.loads(response.text)["choices"][0]["text"].partition("Chinese translation:\n")[2]) # https://stackoverflow.com/a/1926757

    nodes = []
    links = []

    for rdf_pair in rdf_pairs:
        if len(rdf_pair) == 2:
            nodes.append({
                "id": rdf_pair[0],
                "fields": {
                    "label": rdf_pair[0],
                    "type": "entity"
                }
            }),
            nodes.append({
                "id": rdf_pair[1],
                "fields": {
                    "label": rdf_pair[1],
                    "type": "entity"
                }
            })
        else:
            nodes.append({
                "id": rdf_pair[0],
                "fields": {
                    "label": rdf_pair[0],
                    "type": "entity"
                }
            }),
            nodes.append({
                "id": rdf_pair[2],
                "fields": {
                    "label": rdf_pair[2],
                    "type": "entity"
                }
            })
            links.append({
                "source": rdf_pair[0],
                "target": rdf_pair[2],
                "fields": {
                    "label": rdf_pair[1]
                }
            })

    return {
        "nodes": nodes,
        "links": links
    }


def _entity_extraction_via_graph_gpt(prompt: str) -> Response:
    """
    Queries the Completion API (https://platform.openai.com/docs/api-reference/completions) to perform the entity
    extraction.

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
    return PROMPT_TEMPLATE.replace('PROMPT_CONTENTS', knowledge_graph_desc)


def entity_extraction(sentences: list[str]):
    knowledge_graph_desc = " ".join(sentences)
    prompt = _transform_desc_to_prompt(knowledge_graph_desc)
    response = _entity_extraction_via_graph_gpt(prompt)
    knowledge_graph_spec = _convert_to_knowledge_graph_spec(response)
    return knowledge_graph_spec

if __name__ == '__main__':
    pass
