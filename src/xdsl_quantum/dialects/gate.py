from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import (
    GateAttribute,
    SingleQubit,
    Static,
)


@irdl_attr_definition
class IdentityGate(GateAttribute, Static):
    """
    An identity gate on an arbitrary number of qubits
    """

    name = "gate.id"

    @property
    def num_qubits(self) -> int | None:
        return None


@irdl_attr_definition
class HadamardGate(GateAttribute, SingleQubit, Static):
    name = "gate.h"


@irdl_attr_definition
class SGate(GateAttribute, SingleQubit, Static):
    name = "gate.s"


@irdl_attr_definition
class TGate(GateAttribute, SingleQubit, Static):
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
