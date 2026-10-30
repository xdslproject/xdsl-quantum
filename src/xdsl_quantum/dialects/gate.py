from xdsl.ir import Attribute, Dialect, TypeAttribute
from xdsl.irdl import AnyRange, irdl_attr_definition, param_def
from xdsl.parser import AttrParser
from xdsl.printer import Printer

from xdsl_quantum.quantum_operation import (
    GateAttribute,
    QuantumOperationAttribute,
    QuantumOperationConstraint,
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


@irdl_attr_definition
class ControlGate(GateAttribute):
    """
    Creates the "controlled" version of a (possibly parametrized) gate.
    """

    name = "gate.control"

    inner: QuantumOperationAttribute = param_def(
        QuantumOperationConstraint.get(out_constr=AnyRange().of_length(0))
    )

    @property
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        return self.inner.classical_inputs

    @property
    def num_qubits(self) -> int | None:
        inner_qubits = self.inner.num_qubits
        if inner_qubits is None:
            return
        return inner_qubits + 1

    @classmethod
    def parse_parameters(cls, parser: AttrParser) -> tuple[Attribute]:
        with parser.in_angle_brackets():
            return (parser.parse_attribute(),)

    def print_parameters(self, printer: Printer) -> None:
        with printer.in_angle_brackets():
            printer.print_attribute(self.inner)


Gate = Dialect(
    "gate",
    [],
    [
        IdentityGate,
        HadamardGate,
        SGate,
        TGate,
        ControlGate,
    ],
)
