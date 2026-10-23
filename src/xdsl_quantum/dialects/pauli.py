from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import GateAttribute, SingleQubit


@irdl_attr_definition
class XAttr(SingleQubit, GateAttribute):
    name = "pauli.x"


@irdl_attr_definition
class YAttr(SingleQubit, GateAttribute):
    name = "pauli.y"


@irdl_attr_definition
class ZAttr(SingleQubit, GateAttribute):
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
