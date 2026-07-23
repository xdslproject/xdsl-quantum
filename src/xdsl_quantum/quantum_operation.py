from abc import ABC, abstractmethod

from xdsl.ir import ParametrizedAttribute, TypeAttribute


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
