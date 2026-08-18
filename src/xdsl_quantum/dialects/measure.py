from xdsl.dialects.builtin import i1
from xdsl.ir import Dialect, TypeAttribute
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.dialects.angle import AngleType
from xdsl_quantum.quantum_operation import QuantumOperationAttribute


class MeasurementAttribute(QuantumOperationAttribute):
    @property
    def classical_results(self) -> tuple[TypeAttribute, ...]:
        return (i1,)


@irdl_attr_definition
class CompBasisMeasurement(MeasurementAttribute):
    name = "measure.comp_basis"

    @property
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        return ()

    @property
    def num_qubits(self) -> int:
        return 1


@irdl_attr_definition
class XYPlaneMeasurement(MeasurementAttribute):
    name = "measure.xy_plane"

    @property
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        return (AngleType(),)

    @property
    def num_qubits(self) -> int:
        return 1


# Example to generalise later


@irdl_attr_definition
class PauliXXMeasurement(MeasurementAttribute):
    name = "measure.xx"

    @property
    def classical_inputs(self) -> tuple[TypeAttribute, ...]:
        return ()

    @property
    def num_qubits(self) -> int:
        return 2


Measure = Dialect(
    "measure",
    [],
    [
        CompBasisMeasurement,
        XYPlaneMeasurement,
        PauliXXMeasurement,
    ],
)
