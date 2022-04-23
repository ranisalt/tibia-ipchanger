__version__ = "0.1.1"

from .cli import change_client_ip, key_remap, parse_args


def run():
    args = parse_args()

    url_replacements = {}
    for snake_case, camel_case in key_remap.items():
        if value := getattr(args, snake_case):
            url_replacements[bytes(camel_case, "ascii")] = bytes(value, "ascii")

    change_client_ip(args.basedir, args.rsa, url_replacements)
