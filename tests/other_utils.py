import os
from contextlib import contextmanager
from tempfile import TemporaryDirectory


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def inside_tempdir():
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    with TemporaryDirectory() as tmpdir:
        with inside_dir(tmpdir):
            yield
