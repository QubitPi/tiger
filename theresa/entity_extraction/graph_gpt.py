import ast
import json
import requests
from translate import Translator

TRANSLATOR = Translator(to_lang="Chinese")

PROMPT_TEMPLATE = """
Given a prompt, extrapolate as many relationships as possible from it and provide a list of updates.

If an update is a relationship, provide [ENTITY 1, RELATIONSHIP, ENTITY 2]. The relationship is directed, so the order matters.

If an update is related to deleting an entity, provide ["DELETE", ENTITY].

Example:
prompt: Alice is Bob's roommate. Make her node green.
updates:
[["Alice", "roommate", "Bob"]]

prompt: PROMPT_CONTENTS
updates:
"""

def entity_extraction(sentences: list[str]):
    knowledge_graph_desc = " ".join(sentences)
    prompt = PROMPT_TEMPLATE.replace('PROMPT_CONTENTS', knowledge_graph_desc)

    url = 'https://api.openai.com/v1/completions'

    payload = {
        "model": "text-davinci-003",
        "temperature": 0.3,
        "max_tokens": 800,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "prompt": prompt
    }

    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer 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"
        },
        data=json.dumps(payload)
    )



    rdf_pairs = ast.literal_eval(json.loads(response.text)["choices"][0]["text"])

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

    return translate(
        {
            "nodes": nodes,
            "links": links
        },
        knowledge_graph_desc
    )


def translate(knowledge_graph_spec, knowledge_graph_desc):
    for node in knowledge_graph_spec["nodes"]:
        if node["fields"]["label"] not in knowledge_graph_desc:
            node["fields"]["label"] = TRANSLATOR.translate(node["fields"]["label"])
    for link in knowledge_graph_spec["links"]:
        if link["fields"]["label"] not in knowledge_graph_desc:
            link["fields"]["label"] = TRANSLATOR.translate(link["fields"]["label"])
    return knowledge_graph_spec


if __name__ == '__main__':
    pass
