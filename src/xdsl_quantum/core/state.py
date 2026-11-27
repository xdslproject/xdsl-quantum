"""Quantum states are shared between different dialects for the same reasons as
quantum operations (see `operation.py`): rather than redefining states in each dialect,
we encode them as attributes to be used by more generic operations. The
`StateAttribute` interface generalises over the possible start states of a qubit
allocation, specifying only how many qubits the state spans.
"""

from collections.abc import Mapping

from typing_extensions import TypeForm, TypeVar
from xdsl.ir import Attribute
from xdsl.irdl import (
    AnyInt,
    AttrConstraint,
    IntConstraint,
    VerificationContext,
    get_int_constraint,
)
from xdsl.utils.exceptions import VerifyException

from xdsl_quantum.core.arity import QubitArityAttribute


class StateAttribute(QubitArityAttribute):
    """
    Base attribute for all quantum states.
    """


class StateConstraint(AttrConstraint[StateAttribute]):
    """Constrains the number of qubits of a StateAttribute."""

    qubit_constr: IntConstraint

    def __init__(self, qubit_constr: IntConstraint | None = None):
        if qubit_constr is None:
            qubit_constr = AnyInt()
        self.qubit_constr = qubit_constr

    @staticmethod
    def get(
        qubit_constr: int | TypeForm[int] | IntConstraint | None = None,
    ) -> AttrConstraint[StateAttribute]:
        if qubit_constr is None:
            return StateConstraint()
        elif not isinstance(qubit_constr, IntConstraint):
            qubit_constr = get_int_constraint(qubit_constr)
        return StateConstraint(qubit_constr)

    def verify(self, attr: Attribute, constraint_context: VerificationContext) -> None:
        if not isinstance(attr, StateAttribute):
            raise VerifyException(f"{attr} should be a quantum state")
        if attr.num_qubits is not None:
            self.qubit_constr.verify(attr.num_qubits, constraint_context)

    def variables(self) -> set[str]:
        return self.qubit_constr.variables()

    def mapping_type_vars(
        self, type_var_mapping: Mapping[TypeVar, AttrConstraint | IntConstraint]
    ) -> AttrConstraint[StateAttribute]:
        return StateConstraint(self.qubit_constr.mapping_type_vars(type_var_mapping))
