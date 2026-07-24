from __future__ import annotations

from fractions import Fraction

from xdsl.ir import Data, Dialect, ParametrizedAttribute, TypeAttribute
from xdsl.irdl import (
    IRDLOperation,
    irdl_attr_definition,
    irdl_op_definition,
    prop_def,
    result_def,
    traits_def,
)
from xdsl.parser import AttrParser
from xdsl.printer import Printer
from xdsl.traits import ConstantLike, Pure


@irdl_attr_definition
class AngleAttr(Data[Fraction]):
    """
    Attribute that stores an angle as as a multiple of pi in the range [-1, 1)
    """

    name = "angle.attr"

    def __init__(self, fraction: Fraction):
        # Normalize to [-1, 1)
        fraction = (fraction + 1) % 2 - 1
        super().__init__(fraction)

    @classmethod
    def parse_parameter(cls, parser: AttrParser) -> Fraction:
        with parser.in_angle_brackets():
            is_negative = parser.parse_optional_punctuation("-") is not None
            numerator = parser.parse_optional_integer(
                allow_negative=False, allow_boolean=False
            )
            if numerator is None:
                numerator = 1
            if is_negative:
                numerator *= -1
            if numerator == 0:
                parser.parse_optional_keyword("pi")
            else:
                parser.parse_keyword("pi")
            if parser.parse_optional_punctuation("/"):
                denominator = parser.parse_integer(
                    allow_negative=False, allow_boolean=False
                )
            else:
                denominator = 1
            fraction = Fraction(numerator, denominator)
            return (fraction + 1) % 2 - 1

    def print_parameter(self, printer: Printer) -> None:
        with printer.in_angle_brackets():
            match self.data.numerator:
                case 0:
                    printer.print_string("0")
                    return
                case 1:
                    pass
                case -1:
                    printer.print_string("-")
                case i:
                    printer.print_int(i)
            printer.print_string("pi")
            if (d := self.data.denominator) != 1:
                printer.print_string("/")
                printer.print_int(d)


@irdl_attr_definition
class AngleType(ParametrizedAttribute, TypeAttribute):
    """
    A type for runtime angle values.
    """

    name = "angle.type"


@irdl_op_definition
class ConstantAngleOp(IRDLOperation):
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


Angle = Dialect(
    "angle",
    [
        ConstantAngleOp,
    ],
    [
        AngleAttr,
        AngleType,
    ],
)
