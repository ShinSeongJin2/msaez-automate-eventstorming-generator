class DictUtil:
    @staticmethod
    def make_self_routing_dict(*nodes):
        return {node: node for node in nodes}