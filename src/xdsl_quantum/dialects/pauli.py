from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import StaticGateAttribute, SingleQubit


@irdl_attr_definition
class XAttr(SingleQubit, StaticGateAttribute):
    name = "pauli.x"


@irdl_attr_definition
class YAttr(SingleQubit, StaticGateAttribute):
    name = "pauli.y"


@irdl_attr_definition
class ZAttr(SingleQubit, StaticGateAttribute):
    name = "pauli.z"


Pauli = Dialect(
    "pauli",
    [],
    [
        XAttr,
        YAttr,
        ZAttr,
    ],
)
