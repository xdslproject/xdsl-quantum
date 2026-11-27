from abc import ABC, abstractmethod

from xdsl.ir import ParametrizedAttribute


class QubitArityAttribute(ParametrizedAttribute, ABC):
    """
    Base attribute for quantum definitions with a number of qubits.
    """

    @property
    @abstractmethod
    def num_qubits(self) -> int | None:
        """
        The number of qubits this attribute spans.
        If the attribute takes a variable or unknown number of qubits then this
        should return None.
        """


class SingleQubit(QubitArityAttribute, ABC):
    """
    A quantum definition with a single qubit.
    """

    @property
    def num_qubits(self) -> int:
        return 1


class TwoQubit(QubitArityAttribute, ABC):
    """
    A quantum definition with two qubits.
    """

    @property
    def num_qubits(self) -> int:
        return 2
