import pkg_resources

__version__ = str(
    pkg_resources.get_distribution("apispec-webframeworks").parsed_version
)
