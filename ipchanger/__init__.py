from .cli import key_remap, parse_args


def run():
    args = parse_args()

    url_replacements = {}
    for snake_case, camel_case in key_remap.items():
        if value := getattr(args, snake_case):
            url_replacements[bytes(camel_case, "ascii")] = bytes(value, "ascii")
