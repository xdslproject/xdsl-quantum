from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import (
    GateAttribute,
    SingleQubitGateAttribute,
)


@irdl_attr_definition
class IdentityGate(GateAttribute):
    """
    An identity gate on an arbitrary number of qubits
    """

    name = "gate.id"

    @property
    def num_qubits(self) -> int | None:
        return None


@irdl_attr_definition
class HadamardGate(SingleQubitGateAttribute):
    name = "gate.h"


@irdl_attr_definition
class SGate(SingleQubitGateAttribute):
    name = "gate.s"


@irdl_attr_definition
class TGate(SingleQubitGateAttribute):
    name = "gate.t"


Gate = Dialect(
    "gate",
    [],
    [
        IdentityGate,
        HadamardGate,
        SGate,
        TGate,
    ],
)
