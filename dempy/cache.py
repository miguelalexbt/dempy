import io
import os

from . import config

# TODO early draft, to be changed later

def _create_cache_dir(dir):
    cache_dir = os.path.join(config.cache_dir, dir)

    try:
        os.makedirs(cache_dir)
    except OSError:
        pass

    return cache_dir
