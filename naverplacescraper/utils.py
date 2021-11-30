class EmptyResult(Exception):
    """When the result is empty."""
    def __init__(self, msg: str='검색 결과가 없습니다.') -> None:
        self.msg = msg

    def __str__(self) -> str:
        return self.msg
