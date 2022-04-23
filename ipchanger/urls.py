from collections.abc import Generator, Mapping


def parse_urls(urls: bytes) -> Generator[tuple[bytes, bytes], None, None]:
    """Parses URLS section and generates tuples of (key, value) for each URL.

    >>> urls = b'\\ntibiaPageUrl=https://www.tibia.com\\nloginWebService=https://www.tibia.com/clientservices/loginservice.php\\nclientWebService=https://www.tibia.com/clientservices/clientservices.php\\n\\n'
    >>> [*parse_urls(urls)]
    [(b'tibiaPageUrl', b'https://www.tibia.com'), (b'loginWebService', b'https://www.tibia.com/clientservices/loginservice.php'), (b'clientWebService', b'https://www.tibia.com/clientservices/clientservices.php')]
    """
    for url in urls.strip().split(b"\n"):
        key, value = url.split(b"=", maxsplit=1)
        yield key, value


def replace_urls(data: bytearray, replacements: Mapping[bytes, bytes]) -> bytes:
    """
    >>> urls = b'PREFIX[URLS]\\ntibiaPageUrl=https://www.tibia.com\\nloginWebService=https://www.tibia.com/clientservices/loginservice.php\\nclientWebService=https://www.tibia.com/clientservices/clientservices.php\\n\\n[GRAPHICS]SUFFIX'
    >>> replacements = {b'loginWebService': b'http://127.0.0.1:8000/login.php'}
    >>> replace_urls(urls, replacements)
    b'PREFIX[URLS]\\ntibiaPageUrl=https://www.tibia.com\\nloginWebService=http://127.0.0.1:8000/login.php\\nclientWebService=https://www.tibia.com/clientservices/clientservices.php                      \\n\\n[GRAPHICS]SUFFIX'
    """
    start = data.find(b"[URLS]\n") + 7
    end = data.find(b"\n\n[", start)

    assert start < end, "Could not find URLs configuration."

    urls_section = data[start:end]
    urls = b"\n".join(
        b"=".join((key, replacements.get(key, value)))
        for key, value in parse_urls(urls_section)
    )

    assert (
        len(urls) <= end - start
    ), f"URLs configuration is longer than original by {len(urls) - end + start} characters."

    return b"".join((data[:start], urls.ljust(end - start, b" "), data[end:]))
