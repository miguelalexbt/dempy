import io
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


def cache_data(data_dir, data_file, data, serializer=None):
    cache_file = build_cache_path(data_dir, data_file)

    with io.open(cache_file, "wb") as fp:
        data = data if serializer is None else serializer(data).SerializeToString()
        fp.write(data)


def get_cached_data(data_dir, data_file, deserializer=None):
    cache_file = build_cache_path(data_dir, data_file)

    try:
        with io.open(cache_file, "rb") as fp:
            data = fp.read()
        return data if deserializer is None else deserializer(data)
    except (IOError, OSError):
        raise FileNotFoundError


def del_cached_data(data_dir, data_file):
    cache_file = build_cache_path(data_dir, data_file)

    try:
        os.remove(cache_file)
    except (IOError, OSError):
        raise FileNotFoundError
