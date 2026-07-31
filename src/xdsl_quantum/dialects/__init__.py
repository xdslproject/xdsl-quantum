from collections.abc import Callable

from xdsl.ir import Dialect


def get_all_dialects() -> dict[str, Callable[[], Dialect]]:
    """Returns all available dialects."""

    def get_angle():
        from xdsl_quantum.dialects.angle import Angle

        return Angle

    def get_gate():
        from xdsl_quantum.dialects.gate import Gate

        return Gate

    def get_measure():
        from xdsl_quantum.dialects.measure import Measure

        return Measure

    return {
        "angle": get_angle,
        "gate": get_gate,
        "measure": get_measure,
    }
