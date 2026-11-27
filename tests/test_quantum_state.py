import pytest
from typing_extensions import TypeVar
from xdsl.dialects.builtin import i1
from xdsl.ir import VerifyException
from xdsl.irdl import (
    EqIntConstraint,
    IntTypeVarConstraint,
    IntVarConstraint,
    VerificationContext,
    irdl_attr_definition,
)

from xdsl_quantum.core.state import (
    StateAttribute,
    StateConstraint,
)


@irdl_attr_definition
class ExampleState(StateAttribute):
    name = "test.state"

    @property
    def num_qubits(self) -> int | None:
        return 2


@irdl_attr_definition
class VariableSizeState(StateAttribute):
    name = "test.variable_size_state"

    @property
    def num_qubits(self) -> int | None:
        return


def test_quantum_state_constraint() -> None:
    any_quantum_state = StateConstraint.get()

    assert not any_quantum_state.can_infer(set())
    assert any_quantum_state.variables() == set()
    any_quantum_state.verify(ExampleState(), VerificationContext())
    any_quantum_state.verify(VariableSizeState(), VerificationContext())

    with pytest.raises(VerifyException, match="i1 should be a quantum state"):
        any_quantum_state.verify(i1, VerificationContext())

    one_qubit_constr = StateConstraint.get(qubit_constr=1)

    assert not one_qubit_constr.can_infer(set())
    assert one_qubit_constr.variables() == set()
    one_qubit_constr.verify(VariableSizeState(), VerificationContext())

    with pytest.raises(VerifyException, match="Invalid value 2, expected 1"):
        one_qubit_constr.verify(ExampleState(), VerificationContext())

    two_qubit_constr = StateConstraint.get(qubit_constr=2)

    assert not two_qubit_constr.can_infer(set())
    assert two_qubit_constr.variables() == set()
    two_qubit_constr.verify(ExampleState(), VerificationContext())
    two_qubit_constr.verify(VariableSizeState(), VerificationContext())


def test_quantum_state_constraint_variables() -> None:
    int_constraint = IntVarConstraint.get("N")
    constr = StateConstraint.get(qubit_constr=int_constraint)

    assert not constr.can_infer(set())
    assert constr.variables() == {"N"}

    constr.verify(ExampleState(), VerificationContext())
    constr.verify(VariableSizeState(), VerificationContext())


def test_quantum_state_constraint_mapping_type_vars() -> None:
    mapped = StateConstraint.get(qubit_constr=2).mapping_type_vars({})

    assert isinstance(mapped, StateConstraint)
    assert mapped.qubit_constr == EqIntConstraint(2)


def test_quantum_state_constraint_mapping_nested_type_var() -> None:
    T = TypeVar("T")
    constr = StateConstraint.get(
        qubit_constr=IntTypeVarConstraint(T, IntVarConstraint.get("N"))
    )

    mapped = constr.mapping_type_vars({T: IntVarConstraint.get("M")})

    assert isinstance(mapped, StateConstraint)
    assert mapped.qubit_constr == IntVarConstraint.get("M")
