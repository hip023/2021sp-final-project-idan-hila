from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    from setuptools_scm import get_version

    try:
        __version__ = get_version(root="..", relative_to=__file__)
    except Exception:
        pass
