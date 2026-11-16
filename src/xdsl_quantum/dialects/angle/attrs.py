from __future__ import annotations

from xdsl.ir import Data, ParametrizedAttribute, TypeAttribute
from xdsl.irdl import irdl_attr_definition
from xdsl.parser import AttrParser
from xdsl.printer import Printer


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
