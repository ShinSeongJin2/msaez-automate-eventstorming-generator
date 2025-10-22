class ListUtil:
    @staticmethod
    def get_safely(list: list, index: int, default: any = None) -> any:
        if index < 0 or index >= len(list):
            return default
        return list[index]