from abc import ABC

from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.dialects.angle import AngleType
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


class RotationGate(GateAttribute, SingleQubit, ABC):
    """
    Base class for single-qubit rotation gates parameterized by an angle.
    """

    @property
    def classical_inputs(self) -> tuple[AngleType, ...]:
        return (AngleType(),)


@irdl_attr_definition
class RXGate(RotationGate):
    """
    X-rotation gate parameterized by an angle.
    """

    name = "gate.rx"


@irdl_attr_definition
class RYGate(RotationGate):
    """
    Y-rotation gate parameterized by an angle.
    """

    name = "gate.ry"


@irdl_attr_definition
class RZGate(RotationGate):
    """
    Z-rotation gate parameterized by an angle.
    """

    name = "gate.rz"


Gate = Dialect(
    "gate",
    [],
    [
        IdentityGate,
        HadamardGate,
        SGate,
        TGate,
        RXGate,
        RYGate,
        RZGate,
    ],
)
