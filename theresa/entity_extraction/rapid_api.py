import requests
from requests import Response
from flask import current_app # https://stackoverflow.com/a/32017603


def transform_to_knowledge_graph_spec(data):
    """
    Transform the return value of "entity_extraction()" into standard knowledge graph JSON structure
    (https://qubitpi.github.io/knowledge-graph-spec/draft/#sec-Data-Structure)

    The data to be transformed must have the following structure (extra JSON fields are OK but they won't be used)::

    [
        {
            "entities":[
                {
                    "text":"trip",
                    "category":"Event"
                },
                {
                    "text":"Seattle",
                    "category":"Location"
                },
                ...
            ]
        },
        {
            "entities":[
                {
                    "text":"China",
                    "category":"Country"
                },
                ...
            ]
        },
        ...
    ]

    i.e. it's a list of entities grouped by a sentence


    :param data:  The return value of "entity_extraction()"

    :return: a JSON object
    """
    nodes = []

    for sentence_result in data:
        entities = sentence_result["entities"]
        for entity in entities:
            nodes.append({
                "id": entity["text"],
                "fields": {
                    "label": entity["text"],
                    "type": entity["category"]
                }
            })

    return {
        "nodes": nodes
    }


def entity_extraction(sentences: list[str], language: str = "zh"):
    """
    Batch-extracts entities from a list of sentences

    :param sentences:  A list of strings
    :param language:  The language code defined in https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes. Defaults to
    "zh" (Chinese)

    :return: a list of JSON objects, each of which follows this example structure::

        {
            "id":"1",
            "entities":[
                {
                    "text":"trip",
                    "category":"Event",
                    "offset":18,
                    "length":4,
                    "confidenceScore":0.74
                },
                {
                    "text":"Seattle",
                    "category":"Location",
                    "subcategory":"GPE",
                    "offset":26,
                    "length":7,
                    "confidenceScore":1
                }
            ],
            "warnings":[

            ]
        }
    """
    id_counter: int = 0
    microsoft_max_payload_size = 5
    payload: dict[str, list] = { "documents": [ ] }

    results: list[dict] = []

    for sentence in sentences:
        if (id_counter + 1) % microsoft_max_payload_size != 0:
            payload["documents"].append(
                {
                    "id": id_counter,
                    "language": language,
                    "text": sentence
                }
            )
        else:
            results = results + new_results(fire_request(payload))
            payload["documents"] = []

        id_counter = id_counter + 1

    if payload["documents"]:
        results = results + new_results(fire_request(payload))

    return results


def new_results(response):
    return [result for result in response.json()["documents"]]


def fire_request(payload) -> Response:
    """
    Sends entity extraction request to Rapid API at
    https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/microsoft-text-analytics1.

    The response.json() has the following JSON structure::

    {
        "documents":[
            {
                "id":"1",
                "entities":[
                    {
                        "text":"trip",
                        "category":"Event",
                        "offset":18,
                        "length":4,
                        "confidenceScore":0.74
                    },
                    {
                        "text":"Seattle",
                        "category":"Location",
                        "subcategory":"GPE",
                        "offset":26,
                        "length":7,
                        "confidenceScore":1
                    }
                ],
                "warnings":[

                ]
            },
            {
                "id":"2",
                ...
            },
        ],
        "errors":[

        ],
        "modelVersion":"2021-06-01"
    }


    :param payload:  The Microsoft endpoint payload
    :return: a Rapid API response
    """
    url = "https://microsoft-text-analytics1.p.rapidapi.com/entities/recognition/general"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": current_app.config['X_RAPIDAPI_KEY_MICROSOFT_ENTITY_EXTRACTION'],
        "X-RapidAPI-Host": "microsoft-text-analytics1.p.rapidapi.com"
    }
    return requests.post(url, json=payload, headers=headers)


if __name__ == '__main__':
    pass
