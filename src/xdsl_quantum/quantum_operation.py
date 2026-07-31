from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass

from typing_extensions import TypeVar
from xdsl.ir import (
    Attribute,
    ParametrizedAttribute,
    TypeAttribute,
    field,
)
from xdsl.irdl import (
    AnyAttr,
    AnyInt,
    AttrConstraint,
    ConstraintContext,
    IntConstraint,
    RangeConstraint,
    RangeOf,
)
from xdsl.utils.exceptions import VerifyException


class QuantumOperationAttribute(ParametrizedAttribute, ABC):
    """
    Quantum gates and operations are likely to be shared between different dialects.
    Rather than creating a duplicate operation in each dialect, we encode each quantum
    operation as an attribute. The `QuantumOperationAttribute` generalises over gate
    operations and measurements, and specifies the number of classical inputs and
    outputs the operation has. Additional properties are specified by inheriting from
    this Attribute.

    We consider all operations to be non destructive, i.e. they have
    the same number of input and output qubits.

    """

    @property
    @abstractmethod
    def classical_inputs(self) -> tuple[TypeAttribute, ...]: ...

    @property
    @abstractmethod
    def classical_results(self) -> tuple[TypeAttribute, ...]: ...

    @property
    @abstractmethod
    def num_qubits(self) -> int: ...


@dataclass(frozen=True)
class QuantumOperationConstraint(AttrConstraint[QuantumOperationAttribute]):
    """Constrains the inputs and results of a QuantumOperationConstraint"""

    in_constr: RangeConstraint = field(default=RangeOf(AnyAttr()))
    out_constr: RangeConstraint = field(default=RangeOf(AnyAttr()))
    qubit_constr: IntConstraint = field(default=AnyInt())

    def verify(self, attr: Attribute, constraint_context: ConstraintContext) -> None:
        if not isinstance(attr, QuantumOperationAttribute):
            raise VerifyException(f"{attr} should be of type QuantumOperationAttribute")
        self.in_constr.verify(attr.classical_inputs, constraint_context)
        self.out_constr.verify(attr.classical_results, constraint_context)
        self.qubit_constr.verify(attr.num_qubits, constraint_context)

    def variables(self) -> set[str]:
        return (
            self.in_constr.variables()
            | self.out_constr.variables()
            | self.qubit_constr.variables()
        )

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
    A quantum gate is simply an operation with no classical inputs or outputs
    """

    @property
    def classical_inputs(self) -> tuple[()]:
        return ()

    @property
    def classical_results(self) -> tuple[()]:
        return ()


class SingleQubitGateAttribute(GateAttribute, ABC):
    """
    A quantum gate on a single qubit
    """

    @property
    def num_qubits(self) -> int:
        return 1


class TwoQubitGateAttribute(GateAttribute, ABC):
    """
    A quantum gate on two qubits
    """

    @property
    def num_qubits(self) -> int:
        return 2
