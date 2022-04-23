tibia-ipchanger
===============

Installing
----------

Install from [PyPI](https://pypi.org/project/tibia-ipchanger/) using `pip`:

```
$ pip install --upgrade tibia-ipchanger
```

Or, even better, install with [`pipx`](https://pypi.org/project/pipx/):

```
$ pipx install tibia-ipchanger
```

Usage
-----

Run `ipchanger <basedir>`, where `basedir` is the path to the directory where the
launcher is installed. This is the directory containing an executable named `Tibia`, a
file named `launchermetadata.json` and a directory named `packages`.

It is **NOT** the directory containing `3rdpartylicenses` `assets`, `bin` and other
client data, but two directories parent to that one.

To replace an URL, simply pass `--url-as-snake-case <new url>` to the command line,
e.g. `ipchanger path/to/Tibia --login-web-service https://myot.com/login.php` will
replace `loginWebService` with `https://myot.com/login.php`.

The script will create a temporary version of your currently installed client that is
restored after immediately launch, so you can still play regular Tibia by launching the
client as usual.

To see a list of available URLs to change, run `ipchanger -h`:

```
$ ipchanger -h
...
  --tibia-page-url TIBIA_PAGE_URL
  --tibia-store-get-coins-url TIBIA_STORE_GET_COINS_URL
  --get-premium-url GET_PREMIUM_URL
  --create-account-url CREATE_ACCOUNT_URL
  --create-tournament-character-url CREATE_TOURNAMENT_CHARACTER_URL
  --access-account-url ACCESS_ACCOUNT_URL
  --lost-account-url LOST_ACCOUNT_URL
  --manual-url MANUAL_URL
  --faq-url FAQ_URL
  --premium-features-url PREMIUM_FEATURES_URL
  --limesurvey-url LIMESURVEY_URL
  --hints-url HINTS_URL
  --twitch-tibia-url TWITCH_TIBIA_URL
  --youtube-tibia-url YOUTUBE_TIBIA_URL
  --crash-report-url CRASH_REPORT_URL
  --fps-history-recipient FPS_HISTORY_RECIPIENT
  --tutorial-progress-web-service TUTORIAL_PROGRESS_WEB_SERVICE
  --tournament-details-url TOURNAMENT_DETAILS_URL
  --login-web-service LOGIN_WEB_SERVICE
  --client-web-service CLIENT_WEB_SERVICE
```

URLs that are not set will be kept as original. The total length of replaced URLs must
not exceed the total length of the original URLs that are to be replaced, in which case
the script will fail to launch the client.

License
-------

Work licensed under the [MIT License](LICENSE).
