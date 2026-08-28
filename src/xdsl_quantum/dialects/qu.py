from xdsl.ir import Dialect, ParametrizedAttribute, TypeAttribute
from xdsl.irdl import irdl_attr_definition


@irdl_attr_definition
class BitType(ParametrizedAttribute, TypeAttribute):
    """
    Type for a single qubit
    """

    name = "qu.bit"


Qu = Dialect(
    "qu",
    [],
    [
        BitType,
    ],
)
