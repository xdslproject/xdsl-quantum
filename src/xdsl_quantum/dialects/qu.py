from xdsl.ir import Dialect, ParametrizedAttribute, TypeAttribute
from xdsl.irdl import irdl_attr_definition


@irdl_attr_definition
class BitType(ParametrizedAttribute, TypeAttribute):
    """
    Type for a single qubit
    """

    name = "qu.bit"


@irdl_attr_definition
class RefType(ParametrizedAttribute, TypeAttribute):
    """
    Reference to a qubit
    """

    name = "qu.ref"


Qu = Dialect(
    "qu",
    [],
    [
        BitType,
        RefType,
    ],
)
