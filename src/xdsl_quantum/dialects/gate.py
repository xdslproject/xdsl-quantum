from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import (
    SingleQubit,
    StaticGateAttribute,
)


@irdl_attr_definition
class IdentityGate(StaticGateAttribute):
    """
    An identity gate on an arbitrary number of qubits
    """

    name = "gate.id"

    @property
    def num_qubits(self) -> int | None:
        return None


@irdl_attr_definition
class HadamardGate(SingleQubit, StaticGateAttribute):
    name = "gate.h"


@irdl_attr_definition
class SGate(SingleQubit, StaticGateAttribute):
    name = "gate.s"


@irdl_attr_definition
class TGate(SingleQubit, StaticGateAttribute):
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
