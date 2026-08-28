from xdsl.universe import Universe

from xdsl_quantum.dialects import get_all_dialects
from xdsl_quantum.transforms import get_all_passes

UNIVERSE = Universe(
    all_dialects=get_all_dialects(),
    all_passes=get_all_passes(),
)
