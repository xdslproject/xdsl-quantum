from xdsl.dialects.builtin import i1
from xdsl.ir import Dialect, TypeAttribute
from xdsl.irdl import AnyAttr, RangeOf, irdl_attr_definition, param_def

from xdsl_quantum.dialects.angle import AngleType
from xdsl_quantum.quantum_operation import (
    QuantumOperationAttribute,
    QuantumOperationConstraint,
    SingleQubitGateAttribute,
    TwoQubitGateAttribute,
)


@irdl_attr_definition
class XGate(SingleQubitGateAttribute):
    name = "gate.x"


@irdl_attr_definition
class YGate(SingleQubitGateAttribute):
    name = "gate.y"


@irdl_attr_definition
class ZGate(SingleQubitGateAttribute):
    name = "gate.z"


@irdl_attr_definition
class HadamardGate(SingleQubitGateAttribute):
    name = "gate.h"


@irdl_attr_definition
class CZGate(TwoQubitGateAttribute):
    name = "gate.cz"


@irdl_attr_definition
class CXGate(TwoQubitGateAttribute):
    name = "gate.cx"


@irdl_attr_definition
class CondGate(QuantumOperationAttribute):
    name = "gate.cond"

    inner: QuantumOperationAttribute = param_def(
        QuantumOperationConstraint(out_constr=RangeOf(AnyAttr()).of_length(0))
    )

    @property
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        return self.inner.classical_inputs

    @property
    def classical_results(self) -> tuple[TypeAttribute, ...]:
        return ()

    @property
    def num_qubits(self) -> int:
        return self.inner.num_qubits + 1


@irdl_attr_definition
class ClassicalCondGate(QuantumOperationAttribute):
    name = "gate.ccond"

    inner: QuantumOperationAttribute = param_def(
        QuantumOperationConstraint(out_constr=RangeOf(AnyAttr()).of_length(0))
    )

    @property
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        return (i1, *self.inner.classical_inputs)

    @property
    def classical_results(self) -> tuple[()]:
        return ()

    @property
    def num_qubits(self) -> int:
        return self.inner.num_qubits


class RotationGateAttribute(QuantumOperationAttribute):
    @property
    def classical_inputs(self) -> tuple[AngleType]:
        return (AngleType(),)

    @property
    def classical_results(self) -> tuple[()]:
        return ()


class SingleQubitRotationGateAttribute(RotationGateAttribute):
    @property
    def num_qubits(self) -> int:
        return 1


@irdl_attr_definition
class RXGate(SingleQubitRotationGateAttribute):
    name = "gate.rx"


@irdl_attr_definition
class RYGate(SingleQubitRotationGateAttribute):
    name = "gate.ry"


@irdl_attr_definition
class RZGate(SingleQubitRotationGateAttribute):
    name = "gate.rz"


Gate = Dialect(
    "gate",
    [],
    [
        XGate,
        YGate,
        ZGate,
        HadamardGate,
        CondGate,
        ClassicalCondGate,
        CZGate,
        CXGate,
        RXGate,
        RYGate,
        RZGate,
    ],
)
