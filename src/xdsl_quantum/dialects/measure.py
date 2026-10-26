from xdsl.ir import Dialect
from xdsl.irdl import irdl_attr_definition

from xdsl_quantum.quantum_operation import (
    MeasurementAttribute,
    SingleQubit,
    Static,
)


@irdl_attr_definition
class XMeasure(MeasurementAttribute, SingleQubit, Static):
    """
    X basis measurement
    """

    name = "measure.x"


@irdl_attr_definition
class YMeasure(MeasurementAttribute, SingleQubit, Static):
    """
    Y basis measurement
    """

    name = "measure.y"


@irdl_attr_definition
class ZMeasure(MeasurementAttribute, SingleQubit, Static):
    """
    Z basis measurement
    """

    name = "measure.z"


Measure = Dialect(
    "measure",
    [],
    [
        XMeasure,
        YMeasure,
        ZMeasure,
    ],
)
