from __future__ import annotations

from collections.abc import Sequence

from xdsl.dialect_interfaces.constant_materialization import (
    ConstantMaterializationInterface,
)
from xdsl.dialects.builtin import Float64Type, FloatAttr
from xdsl.interfaces import HasFolderInterface
from xdsl.ir import (
    Attribute,
    Data,
    Dialect,
    Operation,
    ParametrizedAttribute,
    SSAValue,
    TypeAttribute,
)
from xdsl.irdl import (
    IRDLOperation,
    irdl_attr_definition,
    irdl_op_definition,
    operand_def,
    prop_def,
    result_def,
    traits_def,
)
from xdsl.parser import AttrParser
from xdsl.printer import Printer
from xdsl.traits import ConstantLike, Pure


@irdl_attr_definition
class AngleAttr(Data[float]):
    """
    Attribute that stores an angle as a float multiple of pi.
    """

    name = "angle.attr"

    @classmethod
    def parse_parameter(cls, parser: AttrParser) -> float:
        with parser.in_angle_brackets():
            is_negative = parser.parse_optional_punctuation("-") is not None
            value = parser.parse_optional_number()
            if value is None:
                value = 1.0
            if is_negative:
                value = -value
            parser.parse_keyword("pi")
            return value

    def print_parameter(self, printer: Printer) -> None:
        with printer.in_angle_brackets():
            match self.data:
                case 0:
                    printer.print_string("0pi")
                case 1:
                    printer.print_string("pi")
                case -1:
                    printer.print_string("-pi")
                case i:
                    printer.print_string(f"{i:g}pi")

    def __add__(self, other: AngleAttr) -> AngleAttr:
        return AngleAttr(self.data + other.data)

    def __mul__(self, other: float) -> AngleAttr:
        return AngleAttr(self.data * other)


@irdl_attr_definition
class AngleType(ParametrizedAttribute, TypeAttribute):
    """
    A type for runtime angle values.
    """

    name = "angle.type"


@irdl_op_definition
class ConstantAngleOp(IRDLOperation, HasFolderInterface):
    """
    Constant-like operation for producing angles
    """

    name = "angle.constant"

    angle = prop_def(AngleAttr)

    out = result_def(AngleType)

    assembly_format = "`` $angle attr-dict"

    traits = traits_def(Pure(), ConstantLike())

    def __init__(self, angle: AngleAttr):
        super().__init__(
            properties={
                "angle": angle,
            },
            result_types=(AngleType(),),
        )

    def fold(self) -> Sequence[SSAValue | Attribute] | None:
        return (self.angle,)


@irdl_op_definition
class AddAngleOp(IRDLOperation, HasFolderInterface):
    """
    Adds two angles.
    """

    name = "angle.add"

    lhs = operand_def(AngleType)

    rhs = operand_def(AngleType)

    out = result_def(AngleType)

    assembly_format = "$lhs `,` $rhs attr-dict"

    def __init__(self, lhs: SSAValue | Operation, rhs: SSAValue | Operation):
        super().__init__(operands=(lhs, rhs), result_types=(AngleType(),))

    def fold(self) -> Sequence[SSAValue | Attribute] | None:
        lhs = ConstantLike.get_constant_value(self.lhs)
        rhs = ConstantLike.get_constant_value(self.rhs)
        if isinstance(lhs, AngleAttr) and isinstance(rhs, AngleAttr):
            return (lhs + rhs,)


@irdl_op_definition
class ScalarMultOp(IRDLOperation, HasFolderInterface):
    """
    Scalar multiplication operation.
    Multiplies an angle by a scalar float value.
    """

    name = "angle.scalar_mult"

    scalar = prop_def(FloatAttr.constr(Float64Type()))
    angle = operand_def(AngleType)
    result = result_def(AngleType)

    assembly_format = "$scalar `,` $angle attr-dict"

    traits = traits_def(Pure())

    def __init__(self, scalar: float | FloatAttr[Float64Type], angle: SSAValue):
        if isinstance(scalar, int | float):
            scalar = FloatAttr(scalar, Float64Type())
        super().__init__(
            operands=[angle],
            properties={"scalar": scalar},
            result_types=[AngleType()],
        )

    def fold(self) -> Sequence[SSAValue | Attribute] | None:
        scalar_value = self.scalar.value.data
        if scalar_value == 0:
            return (AngleAttr(0),)
        if scalar_value == 1.0:
            return (self.angle,)
        const_angle = ConstantLike.get_constant_value(self.angle)
        if isinstance(const_angle, AngleAttr):
            return (const_angle * scalar_value,)


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
