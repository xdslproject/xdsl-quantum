from collections.abc import Callable

from xdsl.ir import Dialect


def get_all_dialects() -> dict[str, Callable[[], Dialect]]:
    """Returns all available dialects."""

    def get_stabsim():
        from xdsl_quantum.dialects.stabsim import StabSim

        return StabSim

    return {"stabsim": get_stabsim}
