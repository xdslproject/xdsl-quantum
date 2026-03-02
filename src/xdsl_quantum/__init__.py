class LazyVersion:
    """
    Resolving the version dynamically is slow, hence this lazy wrapper to get the
    version only when needed.
    """

    _version: str | None

    def __init__(self):
        self._version = None

    def __str__(self):
        if self._version is None:
            from importlib.metadata import PackageNotFoundError, version

            name = "xdsl_quantum"
            try:
                self._version = version(name)
            except PackageNotFoundError:
                # package is not installed
                self._version = f"Error: {name} not installed"

        return self._version


__version__ = LazyVersion()
