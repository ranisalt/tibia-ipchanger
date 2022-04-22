__version__ = "0.1.0"

import argparse
import pathlib
import subprocess
from functools import partial
from typing import Mapping

from .client import find_client_rodata, overlay_file
from .rsa import OPENTIBIA_RSA, replace_rsa
from .urls import key_remap, replace_urls


def parse_args() -> tuple[pathlib.Path, bytes, Mapping[bytes, bytes]]:
    parser = argparse.ArgumentParser()
    parser.add_argument("basedir", type=pathlib.Path, help="Path to Tibia directory")

    parser.add_argument(
        "-r",
        "--rsa",
        type=partial(bytes, encoding="ascii"),
        help="RSA key to use (in hex format).",
        default=OPENTIBIA_RSA,
    )

    url_parser = parser.add_argument_group(
        "replaceable urls",
        "You can replace any of these URLs in the client. Any unset replacement will be kept as original.",
    )
    for k in key_remap:
        url_parser.add_argument(f"--{k.replace('_', '-')}")

    args = parser.parse_args()

    replacements = {}
    for snake_case, camel_case in key_remap.items():
        if value := getattr(args, snake_case):
            replacements[bytes(camel_case, "ascii")] = bytes(value, "ascii")

    return args.basedir, args.rsa, replacements


def change_client_ip():
    basedir, rsa, replacements = parse_args()

    client_path = basedir / "packages" / "Tibia" / "bin" / "client"
    assert client_path.is_file(), f"Could not find client binary in {client_path}."

    launcher_path = basedir / "Tibia"
    assert client_path.is_file(), f"Could not find launcher binary in {launcher_path}."

    client_bytes = bytearray(client_path.read_bytes())
    rodata, start, end = find_client_rodata(client_bytes)
    client_bytes[start:end] = replace_rsa(replace_urls(rodata, replacements), rsa)

    with overlay_file(client_path):
        client_path.write_bytes(client_bytes)
        client_path.chmod(0o755)

        subprocess.run(
            ["-battleye"],
            executable=launcher_path,
            cwd=launcher_path.parent,
            check=True,
        )
