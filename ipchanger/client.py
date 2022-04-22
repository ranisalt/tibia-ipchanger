import io
import os
import pathlib
from contextlib import contextmanager

from elftools.elf.elffile import ELFFile
from elftools.elf.sections import Section


def find_client_rodata(client_binary: bytes) -> tuple[bytes, int, int]:
    elf = ELFFile(io.BytesIO(client_binary))

    rodata_sect: Section = elf.get_section_by_name(".rodata")

    header = rodata_sect.header
    return rodata_sect.data(), header.sh_offset, header.sh_offset + header.sh_size


@contextmanager
def overlay_file(client_path: pathlib.Path):
    client_backup_path = client_path.with_name(f".{client_path.name}.bak")
    assert (
        not client_backup_path.exists()
    ), f"Backup file {client_backup_path} already exists, aborting."

    try:
        os.rename(client_path, client_backup_path)
        yield
    finally:
        os.rename(client_backup_path, client_path)
