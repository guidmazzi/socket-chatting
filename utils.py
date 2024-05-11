def utfDecode(algo: bytes) -> str:
    return algo.decode("utf-8")


def utfEncode(algo: str) -> bytes:
    return algo.encode("utf-8")
