import random
import string

import hanlp

HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)


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


def entity_extraction(texts: list[str]):
    nodes = []
    links = []

    node_name_to_id_map = {}
    link_set = set()
    for srl_results in HanLP(texts)["srl"]:
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


if __name__ == '__main__':
    pass
