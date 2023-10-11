import random
import string


def _random_id():
    return "n" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20)).lower()


def _construct_knowledge_graph_spec_node(extrapolated_entity: str):
    return {
        "id": _random_id(),
        "fields": {
            "name": extrapolated_entity,
            "type": "entity"
        }
    }


def _construct_knowledge_graph_spec_link(source: str, target: str, extrapolated_relationship: str):
    return {
        "id": _random_id(),
        "source": source,
        "target": target,
        "fields": {
            "type": extrapolated_relationship
        }
    }


def _get_hanlp_results(texts: list[str]):
    import requests
    import json

    url = "http://127.0.0.1:5001/invocations"

    payload = json.dumps({
        "dataframe_split": {
            "columns": ["text"],
            "data": [[text] for text in texts]
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return [prediction["0"] for prediction in response.json()["predictions"]]


def _convert_to_knowledge_graph_spec(model_results):
    nodes = []
    links = []

    node_name_to_id_map = {}
    link_set = set()
    for srl_results in model_results:
        for srl_result in srl_results:
            subject = None
            verb = None
            object = None

            for tuple in srl_result:
                if tuple[1] == "ARG0":
                    subject = tuple
                if tuple[1] == "PRED":
                    verb = tuple
                if tuple[1] == "ARG1":
                    object = tuple

                if subject and verb and object:
                    source_node = _construct_knowledge_graph_spec_node(subject[0])
                    target_node = _construct_knowledge_graph_spec_node(object[0])

                    source_node_id = source_node["id"]
                    source_node_name = source_node["fields"]["name"]
                    target_node_id = target_node["id"]
                    target_node_name = target_node["fields"]["name"]

                    if source_node_name not in node_name_to_id_map.keys():
                        node_name_to_id_map[source_node_name] = source_node_id
                        nodes.append(source_node)
                    if target_node_name not in node_name_to_id_map.keys():
                        node_name_to_id_map[target_node_name] = target_node_id
                        nodes.append(target_node)

                    link: str = source_node_name + target_node_name + verb[0]
                    if link not in link_set:
                        links.append(
                            _construct_knowledge_graph_spec_link(
                                node_name_to_id_map[source_node_name],
                                node_name_to_id_map[target_node_name],
                                verb[0]
                            )
                        )
                        link_set.add(link)

                    subject = None
                    verb = None
                    object = None

    return {
        "nodes": nodes,
        "links": links
    }


def entity_extraction(texts: list[str]):
    return _convert_to_knowledge_graph_spec(_get_hanlp_results(texts))


if __name__ == '__main__':
    print(entity_extraction([
        "米哈游成立于2011年,致力于为用户提供美好的、 超出预期的产品与内容。米哈游多年来秉持技术自主创新,坚持走原创精品之路,围绕原创IP打造了涵盖漫画、动画、游戏、音乐、小说及动漫周边的全产业链。",
        "我爱中国"
    ]))
