from collections.abc import Callable

from xdsl.ir import Dialect


def get_all_dialects() -> dict[str, Callable[[], Dialect]]:
    """Returns all available dialects."""

    def get_angle():
        from xdsl_quantum.dialects.angle import Angle

        return Angle

    return {"angle": get_angle}
