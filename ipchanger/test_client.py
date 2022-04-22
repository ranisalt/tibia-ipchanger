import os
import pathlib
import tempfile

import pytest

from .client import overlay_file


@pytest.fixture
def client_path(tmp_path: pathlib.Path):
    tmp_file = tempfile.NamedTemporaryFile(dir=tmp_path, delete=False)
    tmp_file.close()
    yield pathlib.Path(tmp_file.name)
    os.unlink(tmp_file.name)


def test_overlay_client(client_path: pathlib.Path):
    token = os.urandom(16)
    client_path.write_bytes(token)

    with overlay_file(client_path):
        assert not client_path.exists()

        bak = client_path.with_name(f".{client_path.name}.bak")
        assert bak.exists() and bak.read_bytes() == token

    assert not bak.exists()
    assert client_path.exists() and client_path.read_bytes() == token


def test_overlay_client_dest_exists(client_path: pathlib.Path):
    bak = client_path.with_name(f".{client_path.name}.bak")
    bak.write_bytes(b"")

    with pytest.raises(
        AssertionError, match="^Backup file .* already exists, aborting.$"
    ):
        with overlay_file(client_path):
            ...  # pragma: no cover

    os.unlink(bak)
