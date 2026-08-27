from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import SingleQubitGateAttribute


@irdl_attr_definition
class XAttr(SingleQubitGateAttribute):
    name = "pauli.x"


@irdl_attr_definition
class YAttr(SingleQubitGateAttribute):
    name = "pauli.y"


@irdl_attr_definition
class ZAttr(SingleQubitGateAttribute):
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
