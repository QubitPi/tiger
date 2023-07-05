import requests
from requests import Response
from flask import current_app # https://stackoverflow.com/a/32017603

from theresa.entity_extraction.rapid_api import entity_extraction
from theresa.entity_extraction.rapid_api import transform_to_knowledge_graph_spec

def node_expand(node: object):
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

    query = node["fields"]["name"].replace(" ", "+")

    response_body = fire_request(query).json()

    if response_body["itemListElement"]:
        if response_body["itemListElement"][0]:
            if response_body["itemListElement"][0]["result"]:
                if response_body["itemListElement"][0]["result"]["detailedDescription"]:
                    if response_body["itemListElement"][0]["result"]["detailedDescription"]["articleBody"]:
                        # return response_body["itemListElement"][0]["result"]["detailedDescription"]["articleBody"]
                        return transform_to_knowledge_graph_spec(
                            entity_extraction(
                                [
                                    response_body["itemListElement"][0]["result"]["detailedDescription"]["articleBody"]
                                ]
                            )
                        )

    return {
        "nodes": [],
        "relationships": []
    }


def fire_request(query: str) -> Response:
    """
    Sends expand request to Google Knowledge Graph API.

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
    QUERY_TEMPLATE = "https://kgsearch.googleapis.com/v1/entities:search?query={query}&key={api_key}&limit=1&indent=True"
    url = QUERY_TEMPLATE.format(query=query, api_key=current_app.config['GOOGLE_KNOWLEDGE_GRAPH_API_KEY'])

    return requests.get(url)


if __name__ == '__main__':
    pass
