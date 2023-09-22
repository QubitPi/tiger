from collections.abc import Iterable

from theresa.common import remove_duplicates


def _convert_to_spec_node(neo4j_node: object):
    fields: dict = neo4j_node["properties"]
    fields["label"] = neo4j_node["labels"][0]

    return {
        "id": neo4j_node["elementId"],
        "fields": fields
    }


def _extract_nodes(rdf_triple: Iterable) -> object:
    source_and_target = [value for key, value in rdf_triple.items() if value["elementType"] == "node"]

    source = source_and_target[0]
    target = source_and_target[1]

    return [_convert_to_spec_node(source), _convert_to_spec_node(target)]


def _convert_to_spec_link(neo4j_link: object):
    return {
        "id": neo4j_link["elementId"],
        "source": neo4j_link["startNodeElementId"],
        "target": neo4j_link["endNodeElementId"],
        "fields": {
            "label": neo4j_link["type"]
        }
    }


def _extract_link(rdf_triple: Iterable) -> object:
    link = [value for key, value in rdf_triple.items() if value["elementType"] == "relationship"][0]
    return _convert_to_spec_link(link)


def neo4json_2_spec(json: object) -> object:
    """
    Converts a Graph in JSON format exported from Neo4J Browser to a Graph in Knowledge Graph Format.

    An example JSON from Neo4J Browser is::

        [
            {
                "r":{
                    "elementType":"relationship",
                    "identity":2,
                    "start":0,
                    "end":1,
                    "type":"got interrupted by",
                    "properties":{

                    },
                    "elementId":"2",
                    "startNodeElementId":"0",
                    "endNodeElementId":"1"
                },
                "m":{
                    "elementType":"node",
                    "identity":1,
                    "labels":[
                        "Undefined"
                    ],
                    "properties":{
                        "name":"Hacker",
                        "description":"A person who eavesdrops communication",
                        "id":"attacker"
                    },
                    "elementId":"1"
                },
                "n":{
                    "elementType":"node",
                    "identity":0,
                    "labels":[
                        "Person"
                    ],
                    "properties":{
                        "name":"Bob",
                        "description":"A person who sends an email",
                        "label":"Person",
                        "id":"sender"
                    },
                    "elementId":"0"
                }
            },
            {
                "r":{
                    "elementType":"relationship",
                    "identity":3,
                    "start":1,
                    "end":2,
                    "type":"sends 'fake' message to alice",
                    "properties":{

                    },
                    "elementId":"3",
                    "startNodeElementId":"1",
                    "endNodeElementId":"2"
                },
                "m":{
                    "elementType":"node",
                    "identity":2,
                    "labels":[
                        "Person"
                    ],
                    "properties":{
                        "name":"Alice",
                        "description":"A person who receives a message",
                        "label":"Person",
                        "id":"receiver"
                    },
                    "elementId":"2"
                },
                "n":{
                    "elementType":"node",
                    "identity":1,
                    "labels":[
                        "Undefined"
                    ],
                    "properties":{
                        "name":"Hacker",
                        "description":"A person who eavesdrops communication",
                        "id":"attacker"
                    },
                    "elementId":"1"
                }
            }
        ]

    :param json:  The JSON file content from Neo4J Browser export, unchanged

    :return: the converted Graph JSON in Knowledge Graph Spec format
    """

    nodes: list = []
    links: list = []

    for rdf_triple in [triple for triple in json]:
        nodes.extend(_extract_nodes(rdf_triple))
        links.append(_extract_link(rdf_triple))

    return {
        "nodes": remove_duplicates(nodes),
        "links": links
    }
