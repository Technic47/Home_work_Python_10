import glob
import os


def delete() -> None:
    """delete all cache files in directory"""
    for file in glob.glob('cache/*'):
        os.remove(file)
