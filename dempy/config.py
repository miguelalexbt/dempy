import io
import os
import configparser

_defaults = {
    "base_url": "http://localhost/",
    "user": "",
    "password": "",
    "cache_dir": os.path.expanduser(os.path.join("~", ".dempy", "cache"))
}

base_url = _defaults["base_url"]
user = _defaults["user"]
password = _defaults["password"]
cache_dir = _defaults["cache_dir"]


def use_profile(profile_key: str) -> None:
    _setup(profile_key)


def _setup(profile_key: str = "DEFAULT"):
    global base_url
    global user
    global password
    global cache_dir

    try:
        os.mkdir(os.path.expanduser(os.path.join("~", ".dempy")))
    except FileExistsError:
        pass

    config = _parse_config(profile_key)
    base_url = config.get("base_url")
    user = config.get("user")
    password = config.get("password")
    cache_dir = config.get("cache_dir")

    try:
        os.mkdir(cache_dir)
    except FileExistsError:
        pass


def _parse_config(profile_key: str):
    config_file = os.path.expanduser(os.path.join("~", ".dempy", "config"))
    parser = configparser.RawConfigParser(defaults=_defaults)

    if not os.path.exists(config_file):
        with io.open(config_file, "w") as fp:
            parser.write(fp)

    parser.read(config_file)

    try:
        config = parser[profile_key]
    except KeyError:
        config = parser["DEFAULT"]

    return config


# __all__ = [
#     'use_default'
# ]

_setup()
