from collections.abc import Callable

from xdsl.ir import Dialect


def get_all_dialects() -> dict[str, Callable[[], Dialect]]:
    """Returns all available dialects."""

    def get_angle():
        from xdsl_quantum.dialects.angle import Angle

        return Angle

    def get_pauli():
        from xdsl_quantum.dialects.pauli import Pauli

        return Pauli

    def get_qu():
        from xdsl_quantum.dialects.qu import Qu

        return Qu

    return {
        "angle": get_angle,
        "pauli": get_pauli,
        "qu": get_qu,
    }
