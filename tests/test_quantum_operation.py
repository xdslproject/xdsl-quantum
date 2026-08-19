import re

import pytest
from xdsl.dialects.builtin import i1
from xdsl.ir import TypeAttribute, VerifyException
from xdsl.irdl import (
    AnyAttr,
    ConstraintContext,
    RangeOf,
    RangeVarConstraint,
    irdl_attr_definition,
)

from xdsl_quantum.quantum_operation import (
    GateAttribute,
    QuantumOperationAttribute,
    QuantumOperationConstraint,
)


@irdl_attr_definition
class ExampleOperation(QuantumOperationAttribute):
    name = "test.example"

    @property
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        return (i1, i1)

    @property
    def classical_results(self) -> tuple[TypeAttribute, ...]:
        return (i1,)

    @property
    def num_qubits(self) -> int | None:
        return 2


@irdl_attr_definition
class ExampleGate(GateAttribute):
    name = "test.gate"

    @property
    def num_qubits(self) -> int | None:
        return


def test_quantum_operation_constraint() -> None:
    any_quantum_operation = QuantumOperationConstraint.get()

    assert not any_quantum_operation.can_infer(set())
    assert any_quantum_operation.variables() == set()
    any_quantum_operation.verify(ExampleOperation(), ConstraintContext())
    any_quantum_operation.verify(ExampleGate(), ConstraintContext())

    with pytest.raises(VerifyException, match="i1 should be a quantum operation"):
        any_quantum_operation.verify(i1, ConstraintContext())

    gate_constr = QuantumOperationConstraint.gate()

    assert not gate_constr.can_infer(set())
    assert gate_constr.variables() == set()
    gate_constr.verify(ExampleGate(), ConstraintContext())

    with pytest.raises(VerifyException, match="Invalid value 2, expected 0"):
        gate_constr.verify(ExampleOperation(), ConstraintContext())

    range_constraint = RangeVarConstraint("R", RangeOf(AnyAttr()))
    same_in_out_constr = QuantumOperationConstraint.get(
        range_constraint, range_constraint
    )

    assert not same_in_out_constr.can_infer({"R"})
    assert same_in_out_constr.variables() == {"R"}

    same_in_out_constr.verify(ExampleGate(), ConstraintContext())
    with pytest.raises(
        VerifyException,
        match=re.escape(
            "attributes ('i1', 'i1') expected from range variable 'R', but got ('i1',)"
        ),
    ):
        same_in_out_constr.verify(ExampleOperation(), ConstraintContext())

    one_qubit_constr = QuantumOperationConstraint.get(qubit_constr=1)

    assert not one_qubit_constr.can_infer(set())
    assert one_qubit_constr.variables() == set()

    one_qubit_constr.verify(ExampleGate(), ConstraintContext())

    with pytest.raises(VerifyException, match="Invalid value 2, expected 1"):
        one_qubit_constr.verify(ExampleOperation(), ConstraintContext())

    two_qubit_constr = QuantumOperationConstraint.get(qubit_constr=2)
    assert not two_qubit_constr.can_infer(set())
    assert two_qubit_constr.variables() == set()

    two_qubit_constr.verify(ExampleOperation(), ConstraintContext())
    two_qubit_constr.verify(ExampleGate(), ConstraintContext())
