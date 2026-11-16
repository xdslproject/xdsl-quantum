from xdsl.dialect_interfaces.constant_materialization import (
    ConstantMaterializationInterface,
)
from xdsl.ir import Attribute, Dialect, Operation

from .attrs import AngleAttr, AngleType
from .ops import AddAngleOp, ConstantAngleOp, ScalarMultOp


class AngleConstantMaterializationInterface(ConstantMaterializationInterface):
    def materialize_constant(
        self, value: Attribute, type: Attribute
    ) -> Operation | None:
        if type == AngleType() and isinstance(value, AngleAttr):
            return ConstantAngleOp(value)


Angle = Dialect(
    "angle",
    [
        ConstantAngleOp,
        AddAngleOp,
        ScalarMultOp,
    ],
    [
        AngleAttr,
        AngleType,
    ],
    [AngleConstantMaterializationInterface()],
)
