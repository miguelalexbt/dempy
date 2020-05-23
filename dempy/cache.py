import io
import os
import shutil
import glob
from . import config


def clear():
    shutil.rmtree(config.cache_dir)


def _add_file_extension(cache_file):
    globs = glob.glob(cache_file + ".*")
    return globs[0] if len(globs) == 1 else cache_file


def _build_cache_path(data_dir, data_file):
    cache_path = os.path.abspath(os.path.join(config.cache_dir, data_dir))

    try:
        os.makedirs(cache_path)
    except OSError:
        pass

    return os.path.normpath(os.path.join(cache_path, data_file))


def _cache_data(data_dir, data_file, data, serializer=None):
    cache_file = _build_cache_path(data_dir, data_file)

    with io.open(cache_file, "wb") as fp:
        data = data if serializer is None else serializer(data).SerializeToString()
        fp.write(data)


def _get_cached_data(data_dir, data_file, deserializer=None):
    cache_file = _build_cache_path(data_dir, data_file)

    if deserializer is None:
        cache_file = _add_file_extension(cache_file)

    try:
        with io.open(cache_file, "rb") as fp:
            data = fp.read()
        return data if deserializer is None else deserializer(data)
    except (IOError, OSError):
        raise FileNotFoundError


# def del_cached_data(data_dir, data_file):
#     cache_file = _build_cache_path(data_dir, data_file)
#
#     try:
#         os.remove(cache_file)
#     except (IOError, OSError):
#         raise FileNotFoundError
