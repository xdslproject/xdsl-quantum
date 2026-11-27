from abc import ABC
from collections.abc import Sequence
from typing import Self

from xdsl.ir import Attribute, Block, Dialect, Operation, Region, SSAValue
from xdsl.irdl import (
    IRDLOperation,
    irdl_op_definition,
    operand_def,
    region_def,
    traits_def,
    var_result_def,
)
from xdsl.parser import Parser
from xdsl.printer import Printer
from xdsl.traits import NoTerminator

from xdsl_quantum.dialects.qu import RefType


class QifLikeOp(IRDLOperation, ABC):
    """
    Base Quantum if operation
    """

    cond = operand_def()
    results = var_result_def()

    true_region = region_def("single_block")
    # TODO this should be optional under certain conditions
    false_region = region_def()

    def __init__(
        self,
        cond: SSAValue | Operation,
        return_types: Sequence[Attribute],
        true_region: Region | Sequence[Block] | Sequence[Operation],
        false_region: Region | Sequence[Block] | Sequence[Operation] | None = None,
        attr_dict: dict[str, Attribute] | None = None,
    ):
        if false_region is None:
            false_region = Region()

        super().__init__(
            operands=[cond],
            result_types=return_types,
            regions=[true_region, false_region],
            attributes=attr_dict,
        )


@irdl_op_definition
class QifOp(QifLikeOp):
    """
    Quantum if operation
    """

    name = "qscf.qif"

    cond = operand_def(RefType)

    traits = traits_def(NoTerminator())

    def __init__(
        self,
        cond: SSAValue | Operation,
        true_region: Region | Sequence[Block] | Sequence[Operation],
        false_region: Region | Sequence[Block] | Sequence[Operation] | None = None,
        attr_dict: dict[str, Attribute] | None = None,
    ):
        if false_region is None:
            false_region = Region()

        super().__init__(
            cond=cond,
            return_types=[],
            true_region=true_region,
            false_region=false_region,
            attr_dict=attr_dict,
        )

    @classmethod
    def parse(cls, parser: Parser) -> Self:
        cond = parser.parse_operand(RefType())
        if parser.parse_optional_punctuation("->"):
            parser.parse_characters("()")

        then_region = parser.parse_region()
        block = then_region.blocks.last
        if block is None:
            block = Block()
            then_region.add_block(block)

        else_region = (
            parser.parse_region() if parser.parse_optional_keyword("else") else Region()
        )

        attr_dict = parser.parse_optional_attr_dict()

        return cls(cond, then_region, else_region, attr_dict)

    def print(self, printer: Printer):
        printer.print_string(" ")
        printer.print_operand(self.cond)

        print_block_terminators = False

        printer.print_string(" ")
        printer.print_region(
            self.true_region,
            print_entry_block_args=False,
            print_block_terminators=print_block_terminators,
        )

        if bool(self.false_region.blocks):
            printer.print_string(" else ")
            printer.print_region(
                self.false_region,
                print_entry_block_args=False,
                print_block_terminators=print_block_terminators,
            )

        if bool(self.attributes.keys()):
            printer.print_attr_dict(self.attributes)


Qscf = Dialect(
    "qscf",
    [QifOp],
    [],
)
