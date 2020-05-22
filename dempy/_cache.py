import io
import json
import os

from . import config


def create_cache_dir(data_dir):
    cache_dir = os.path.abspath(os.path.join(config.cache_dir, data_dir))

    try:
        os.makedirs(cache_dir)
    except OSError:
        pass

    return cache_dir


def build_cache_path(data_dir, data_file):
    cache_dir = create_cache_dir(data_dir)
    return os.path.normpath(os.path.join(cache_dir, data_file))


def cache_data(data_dir, data_file, data, binary=False, **kwargs):
    cache_file = build_cache_path(data_dir, data_file)

    if binary:
        with io.open(cache_file, "wb") as fp:
            fp.write(data)
    else:
        with io.open(cache_file, "w", encoding="utf-8") as fp:
            json.dump(data, fp, **kwargs)


def get_cached_data(data_dir, data_file, binary=False, **kwargs):
    cache_file = build_cache_path(data_dir, data_file)

    try:
        if binary:
            with io.open(cache_file, "rb") as fp:
                data = fp.read()
        else:
            with io.open(cache_file, "r", encoding="utf-8") as fp:
                data = json.load(fp, **kwargs)
        return data
    except (IOError, OSError) as e:
        raise Exception()


def del_cached_data(data_dir, data_file):
    cache_file = build_cache_path(data_dir, data_file)

    try:
        os.remove(cache_file)
    except (IOError, OSError):
        raise Exception()
