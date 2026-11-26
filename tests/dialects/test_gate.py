from xdsl.dialects.builtin import i1

from xdsl_quantum.dialects.angle.attrs import AngleType
from xdsl_quantum.dialects.gate import (
    ConditionedGate,
    ControlGate,
    HadamardGate,
    IdentityGate,
    RXGate,
    TGate,
)


def test_control_gate_qubit_counts() -> None:
    """Test that ControlGate correctly adds one qubit to the inner gate."""
    control_h = ControlGate(HadamardGate())
    assert control_h.num_qubits == 2  # 1 (inner) + 1 (control)

    control_id = ControlGate(IdentityGate())
    assert control_id.num_qubits is None  # Inner is None, so result is None


def test_control_gate_parameters() -> None:
    """Test that ControlGate preserves classical parameters from inner gate."""
    # Single-qubit gates have no parameters
    control_h = ControlGate(HadamardGate())
    assert control_h.classical_inputs == ()

    # Rotation gates have angle parameters
    control_rx = ControlGate(RXGate())
    assert control_rx.classical_inputs == (AngleType(),)


def test_conditioned_gate_qubit_counts() -> None:
    """Test that ConditionedGate preserves qubit count from inner gate."""
    # Condition on single-qubit gates
    cond_h = ConditionedGate(HadamardGate())
    assert cond_h.num_qubits == 1

    # Condition on identity (arbitrary qubits)
    cond_id = ConditionedGate(IdentityGate())
    assert cond_id.num_qubits is None


def test_conditioned_gate_parameters() -> None:
    """Test that ConditionedGate adds one classical bit for the condition."""
    # Single-qubit gates have no parameters
    cond_h = ConditionedGate(HadamardGate())
    assert cond_h.classical_inputs == (i1,)

    # Rotation gates have angle parameters plus the condition bit
    cond_rx = ConditionedGate(RXGate())
    assert cond_rx.classical_inputs == (i1, AngleType())


def test_nested_control_gate() -> None:
    """Test doubly-controlled gates (control on control)."""
    # Toffoli-like gate: control on controlled-T
    control_control_t = ControlGate(ControlGate(TGate()))
    assert control_control_t.num_qubits == 3  # 1 (inner) + 1 + 1
    assert control_control_t.classical_inputs == ()


def test_nested_conditioned_gate() -> None:
    """Test doubly-conditioned gates."""
    # Condition on conditioned-H
    cond_cond_h = ConditionedGate(ConditionedGate(HadamardGate()))
    assert cond_cond_h.num_qubits == 1
    assert cond_cond_h.classical_inputs == (i1, i1)  # Two condition bits


def test_control_conditioned_gate() -> None:
    """Test control on a conditioned gate."""
    # Control on conditioned-T
    control_cond_t = ControlGate(ConditionedGate(TGate()))
    assert control_cond_t.num_qubits == 2  # 1 (inner) + 1 (control)
    assert control_cond_t.classical_inputs == (i1,)  # One condition bit


def test_conditioned_control_gate() -> None:
    """Test condition on a controlled gate."""
    # Condition on controlled-H
    cond_control_h = ConditionedGate(ControlGate(HadamardGate()))
    assert cond_control_h.num_qubits == 2  # 1 (inner) + 1 (control)
    assert cond_control_h.classical_inputs == (i1,)  # One condition bit
