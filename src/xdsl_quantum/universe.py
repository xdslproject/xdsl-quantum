from xdsl.universe import Universe

from xdsl_quantum.dialects import get_all_dialects  # TODO: Change this
from xdsl_quantum.transforms import get_all_passes  # TODO: Change this

UNIVERSE = Universe(
    all_dialects=get_all_dialects(),
    all_passes=get_all_passes(),
)
