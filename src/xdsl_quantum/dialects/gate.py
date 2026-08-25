from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import GateAttribute


@irdl_attr_definition
class IdentityGate(GateAttribute):
    """
    An identity gate on an arbitrary number of qubits
    """

    name = "gate.id"

    @property
    def num_qubits(self) -> int | None:
        return None


Gate = Dialect(
    "gate",
    [],
    [
        IdentityGate,
    ],
)
