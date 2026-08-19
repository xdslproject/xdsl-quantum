"""Quantum gates and operations are likely to be shared between different dialects.
Rather than creating a duplicate operation in each dialect, we encode these as
attributes to be used by more generic operations. The `QuantumOperationAttribute`
interface generalises over gate operations and measurements, and specifies the number of
classical inputs and outputs the operation has, as well as (optionally) how many qubits
it acts on.

We consider all operations to be non-destructive, meaning they have the same number of
input and output qubits, but ultimately the dialect can decide how these are used.

Generalising over quantum operations with attributes has two advantages:
- Static properties of common gates and subprocedures can be encoded once on the
attribute, rather than being redefined for every dialect these gates are used in.
- Certain transformations may be able to act in an operation independent way, for
instance translating from the 'qssa' to 'qref' dialect does not need any knowledge of
which quantum operations are being performed.

"""

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass

from typing_extensions import TypeForm, TypeVar
from xdsl.ir import (
    Attribute,
    ParametrizedAttribute,
    TypeAttribute,
)
from xdsl.irdl import (
    AnyAttr,
    AnyInt,
    AttrConstraint,
    ConstraintContext,
    IntConstraint,
    RangeConstraint,
    RangeOf,
    get_int_constraint,
)
from xdsl.utils.exceptions import VerifyException


class QuantumOperationAttribute(ParametrizedAttribute, ABC):
    """
    Base attribute for all quantum operations.
    """

    @property
    @abstractmethod
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        """The types of the classical inputs, given as a"""

    @property
    @abstractmethod
    def classical_results(self) -> tuple[TypeAttribute, ...]:
        """The classical outcomes of the operation."""

    @property
    @abstractmethod
    def num_qubits(self) -> int | None:
        """
        How many qubits this operation acts on.
        If the operation takes a variable or unknown number of qubits then this should
        return None.
        """


@dataclass(frozen=True)
class QuantumOperationConstraint(AttrConstraint[QuantumOperationAttribute]):
    """Constrains the inputs and results of a QuantumOperationAttribute."""

    in_constr: RangeConstraint
    out_constr: RangeConstraint
    qubit_constr: IntConstraint

    @staticmethod
    def get(
        in_constr: RangeConstraint | None = None,
        out_constr: RangeConstraint | None = None,
        qubit_constr: int | TypeForm[int] | IntConstraint | None = None,
    ) -> AttrConstraint[QuantumOperationAttribute]:

        if in_constr is None:
            in_constr = RangeOf(AnyAttr())

        if out_constr is None:
            out_constr = RangeOf(AnyAttr())

        if qubit_constr is None:
            qubit_constr = AnyInt()
        elif not isinstance(qubit_constr, IntConstraint):
            qubit_constr = get_int_constraint(qubit_constr)

        return QuantumOperationConstraint(in_constr, out_constr, qubit_constr)

    @staticmethod
    def gate(
        qubit_constr: int | TypeForm[int] | IntConstraint | None = None,
    ) -> AttrConstraint[QuantumOperationAttribute]:
        return QuantumOperationConstraint.get(
            in_constr=RangeOf(AnyAttr()).of_length(0),
            out_constr=RangeOf(AnyAttr()).of_length(0),
            qubit_constr=qubit_constr,
        )

    def verify(self, attr: Attribute, constraint_context: ConstraintContext) -> None:
        if not isinstance(attr, QuantumOperationAttribute):
            raise VerifyException(f"{attr} should be a quantum operation")
        self.in_constr.verify(attr.classical_inputs, constraint_context)
        self.out_constr.verify(attr.classical_results, constraint_context)
        if attr.num_qubits is not None:
            self.qubit_constr.verify(attr.num_qubits, constraint_context)

    def variables(self) -> set[str]:
        return self.in_constr.variables() | self.out_constr.variables()

    def mapping_type_vars(
        self, type_var_mapping: Mapping[TypeVar, AttrConstraint | IntConstraint]
    ) -> AttrConstraint[QuantumOperationAttribute]:
        return QuantumOperationConstraint(
            self.in_constr.mapping_type_vars(type_var_mapping),
            self.out_constr.mapping_type_vars(type_var_mapping),
            self.qubit_constr.mapping_type_vars(type_var_mapping),
        )


class GateAttribute(QuantumOperationAttribute, ABC):
    """
    A quantum gate is an operation with no classical inputs or outputs
    """

    @property
    def classical_inputs(self) -> tuple[()]:
        return ()

    @property
    def classical_results(self) -> tuple[()]:
        return ()


class SingleQubitGateAttribute(GateAttribute, ABC):
    """
    A quantum gate on a single qubit.
    """

    @property
    def num_qubits(self) -> int:
        return 1


class TwoQubitGateAttribute(GateAttribute, ABC):
    """
    A quantum gate on two qubits.
    """

    @property
    def num_qubits(self) -> int:
        return 2
