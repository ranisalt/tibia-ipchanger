import pytest

from .rsa import CIPSOFT_RSA, OPENTIBIA_RSA, replace_rsa


def test_replace_rsa():
    data = b"XYZ" * 500 + b"\x00" + CIPSOFT_RSA + b"\x00" + b"XYZ" * 500
    expected = b"XYZ" * 500 + b"\x00" + OPENTIBIA_RSA + b"\x00" + b"XYZ" * 500

    assert replace_rsa(data) == expected


def test_replace_rsa_short_replacement():
    data = b"XYZ" * 500 + b"\x00" + CIPSOFT_RSA[::-1] + b"\x00" + b"XYZ" * 500

    with pytest.raises(
        AssertionError, match=r"^Replacement RSA key is not 256 bytes long\.$"
    ):
        replace_rsa(data, OPENTIBIA_RSA[:-1])


def test_replace_rsa_missing_key():
    data = b"XYZ" * 500 + b"\x00" + CIPSOFT_RSA[::-1] + b"\x00" + b"XYZ" * 500

    with pytest.raises(AssertionError, match=r"^Could not find RSA key to replace\.$"):
        replace_rsa(data)
