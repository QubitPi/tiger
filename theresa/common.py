def remove_duplicates(nodes: list) -> list:
    """
    De-duplicates nodes by node.id and returns a new list of unique nodes.

    :param nodes:  The node list with potential duplicaets

    :return: a list of nodes with unique id's
    """
    return list({node["fields"]["name"]: node for node in nodes}.values())
