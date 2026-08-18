"""Quantum gates and operations are likely to be shared between different dialects.
Rather than creating a duplicate operation in each dialect, we encode each quantum
operation as an attribute. The `QuantumOperationAttribute` generalises over gate
operations and measurements, and specifies the number of classical inputs and outputs
the operation has.

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

from xdsl.ir import ParametrizedAttribute, TypeAttribute


class QuantumOperationAttribute(ParametrizedAttribute, ABC):
    """
    Base attribute for all quantum operations.
    """

    @property
    @abstractmethod
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        """The classical inputs or parameters to the operation."""

    @property
    @abstractmethod
    def classical_results(self) -> tuple[TypeAttribute, ...]:
        """The classical outcome space of running the operation."""

    @property
    @abstractmethod
    def num_qubits(self) -> int | None:
        """
        How many qubits this operation acts on.
        If the operation takes a variable or unknown number of qubits then this should
        return None.
        """


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
