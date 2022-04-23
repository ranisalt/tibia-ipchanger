import argparse
import pathlib
import subprocess
from functools import partial
from typing import Mapping

from .client import find_client_rodata, overlay_file
from .rsa import OPENTIBIA_RSA, replace_rsa
from .urls import replace_urls

key_remap = {
    "tibia_page_url": "tibiaPageUrl",
    "tibia_store_get_coins_url": "tibiaStoreGetCoinsUrl",
    "get_premium_url": "getPremiumUrl",
    "create_account_url": "createAccountUrl",
    "create_tournament_character_url": "createTournamentCharacterUrl",
    "access_account_url": "accessAccountUrl",
    "lost_account_url": "lostAccountUrl",
    "manual_url": "manualUrl",
    "faq_url": "faqUrl",
    "premium_features_url": "premiumFeaturesUrl",
    "limesurvey_url": "limesurveyUrl",
    "hints_url": "hintsUrl",
    "twitch_tibia_url": "twitchTibiaUrl",
    "youtube_tibia_url": "youTubeTibiaUrl",
    "crash_report_url": "crashReportUrl",
    "fps_history_recipient": "fpsHistoryRecipient",
    "tutorial_progress_web_service": "tutorialProgressWebService",
    "tournament_details_url": "tournamentDetailsUrl",
    "login_web_service": "loginWebService",
    "client_web_service": "clientWebService",
}


def parse_args():
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

    return parser.parse_args()


def change_client_ip(
    basedir: pathlib.Path, rsa: bytes, url_replacements: Mapping[str, str]
):
    client_path = basedir / "packages" / "Tibia" / "bin" / "client"
    assert client_path.is_file(), f"Could not find client binary in {client_path}."

    launcher_path = basedir / "Tibia"
    assert client_path.is_file(), f"Could not find launcher binary in {launcher_path}."

    client_bytes = bytearray(client_path.read_bytes())
    rodata, start, end = find_client_rodata(client_bytes)
    client_bytes[start:end] = replace_rsa(replace_urls(rodata, url_replacements), rsa)

    with overlay_file(client_path):
        client_path.write_bytes(client_bytes)
        client_path.chmod(0o755)

        subprocess.run(
            ["-battleye"],
            executable=launcher_path,
            cwd=launcher_path.parent,
            check=True,
        )
