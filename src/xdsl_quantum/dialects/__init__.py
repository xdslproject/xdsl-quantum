from collections.abc import Callable

from xdsl.ir import Dialect


def get_all_dialects() -> dict[str, Callable[[], Dialect]]:
    """Returns all available dialects."""

    def get_qir():
        from xdsl_quantum.dialects.qir import QIR

        return QIR

    return {
        "qir": get_qir,
    }
