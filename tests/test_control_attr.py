import pytest
from xdsl.ir import VerifyException
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.dialects.gate import ControlGate
from xdsl_quantum.quantum_operation import MeasurementAttribute, Static


@irdl_attr_definition
class ExampleMeasurementGate(MeasurementAttribute, Static):
    name = "test.measurement_gate"

    @property
    def num_qubits(self) -> int | None:
        return


def test_controlled_gate() -> None:
    with pytest.raises(
        VerifyException,
        match=(
            """parameter 'inner' does not verify:\nincorrect length for"""
            """ range variable:\nInvalid value 1, expected 0"""
        ),
    ):
        ControlGate(ExampleMeasurementGate())
