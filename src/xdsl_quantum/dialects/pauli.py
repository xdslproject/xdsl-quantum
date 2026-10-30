from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import GateAttribute, SingleQubit, Static


@irdl_attr_definition
class XAttr(GateAttribute, SingleQubit, Static):
    name = "pauli.x"


@irdl_attr_definition
class YAttr(GateAttribute, SingleQubit, Static):
    name = "pauli.y"


@irdl_attr_definition
class ZAttr(GateAttribute, SingleQubit, Static):
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
