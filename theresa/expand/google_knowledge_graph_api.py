import requests
from requests import Response
from flask import current_app  # https://stackoverflow.com/a/32017603

from theresa.entity_extraction.graph_gpt import entity_extraction


def _detect_language_as_either_zh_or_en(text: str):
    """
    Returns the most probable language (either Chinese or English) of a specified text via RapidAPI at
    https://rapidapi.com/microsoft-azure-org-microsoft-cognitive-services/api/microsoft-text-analytics1/ (Detect
    Language)

    :param text:  The provided text to be analyzed

    :return: one of two values: "zh" or "en"
    """
    url = "https://microsoft-text-analytics1.p.rapidapi.com/languages"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": current_app.config['X_RAPIDAPI_KEY_MICROSOFT_LANGUAGE_DETECTION'],
        "X-RapidAPI-Host": "microsoft-text-analytics1.p.rapidapi.com"
    }
    payload = {
        "documents": [{
            "id": "1",
            "text": text
        }]
    }
    iso6391Name: str = requests.post(url, json=payload, headers=headers).json()["documents"][0]["detectedLanguage"][
        "iso6391Name"]

    if iso6391Name == "zh_chs":
        return "zh"

    return "en"


def _fire_request(query: str) -> Response:
    """
    Sends expand request to Google Knowledge Graph API.

    :param query:  The search term

    :return: a Google Knowledge Graph API response object (Not in Knowledge Graph Spec format)
    """
    iso_language: str = _detect_language_as_either_zh_or_en(query)

    QUERY_TEMPLATE = "https://kgsearch.googleapis.com/v1/entities:search?query={query}&key={" \
                     "api_key}&limit=1&indent=True&languages={language}"
    url = QUERY_TEMPLATE.format(
        query=query,
        api_key=current_app.config['GOOGLE_KNOWLEDGE_GRAPH_API_KEY'],
        language=iso_language
    )

    return requests.get(url)


def _get_queries(node) -> list[str]:
    """
    Tokenizing a node fields.

    Each field will fire a Google Knowledge Graph API

    :param node:  An object representing a Knowledge Graph Spec node

    :return: a list of Google Knowledge Graph API search queries
    """
    queries = []
    for field_name, field_value in node["fields"].items():
        queries.append(field_value.replace(" ", "+"))
    return queries


def node_expand(node: object):
    """
    Expands a given node.

    :param node:  An object representing a Knowledge Graph Spec node

    :return: a Knowledge Graph Spec graph what guarantees to contain the node being expanded
    """

    queries = _get_queries(node)

    nodes = []
    links = []
    for query in queries:
        response_body = _fire_request(query).json()

        if response_body["itemListElement"]:
            if response_body["itemListElement"][0]:
                if response_body["itemListElement"][0]["result"]:
                    if response_body["itemListElement"][0]["result"]["detailedDescription"]:
                        if response_body["itemListElement"][0]["result"]["detailedDescription"]["articleBody"]:
                            expanded_graph = entity_extraction(
                                response_body["itemListElement"][0]["result"]["detailedDescription"]["articleBody"]
                            )

                            nodes.extend(expanded_graph["nodes"])
                            links.extend(expanded_graph["links"])

    for expanded_node in nodes:
        if node["id"] == expanded_node["id"]:
            nodes.remove(expanded_node)

    for expanded_node in nodes:
        links.append({
            "source": node["id"],
            "target": expanded_node["id"]
        })

    nodes.append(node)

    return {
        "nodes": nodes,
        "links": links
    }


if __name__ == '__main__':
    pass
