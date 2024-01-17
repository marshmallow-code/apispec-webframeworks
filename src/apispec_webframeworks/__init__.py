from importlib.metadata import distribution

__version__ = str(distribution("apispec-webframeworks").version)
