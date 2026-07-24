from __future__ import annotations

import math

from xdsl.dialects.builtin import FloatData
from xdsl.ir import Dialect, ParametrizedAttribute, TypeAttribute
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
class AngleAttr(ParametrizedAttribute):
    """
    Attribute that wraps around a float attr, implicitly keeping it in the range
    [0, 2) and implicitly multiplying by pi
    """

    name = "angle.attr"
    data: FloatData

    def __init__(self, f: float):
        f_attr = FloatData(math.fmod(f, 2))
        super().__init__(f_attr)

    def as_float_raw(self) -> float:
        return self.data.data

    def as_float(self) -> float:
        return self.as_float_raw() * math.pi

    @classmethod
    def parse_parameters(cls, parser: AttrParser) -> tuple[FloatData]:
        with parser.in_angle_brackets():
            is_negative = parser.parse_optional_punctuation("-") is not None
            f = parser.parse_optional_number()
            if f is None:
                f = 1.0
            if isinstance(f, int):
                f = float(f)
            if f == 0.0:
                parser.parse_optional_keyword("pi")
            else:
                parser.parse_keyword("pi")
            if is_negative:
                f = -f
            return (FloatData(f % 2),)

    def print_parameters(self, printer: Printer) -> None:
        with printer.in_angle_brackets():
            f = self.as_float_raw()
            if f == 0.0:
                printer.print_string("0")
            elif f == 1.0:
                printer.print_string("pi")
            else:
                printer.print_string(f"{f}pi")


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
