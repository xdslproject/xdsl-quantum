from collections.abc import Sequence
from typing import Self

from xdsl.dialects.utils import AbstractYieldOperation
from xdsl.ir import Attribute, Block, Dialect, Operation, Region, SSAValue
from xdsl.irdl import (
    IRDLOperation,
    irdl_op_definition,
    lazy_traits_def,
    operand_def,
    region_def,
    traits_def,
    var_result_def,
)
from xdsl.parser import Parser
from xdsl.printer import Printer
from xdsl.traits import (
    HasParent,
    IsTerminator,
    Pure,
    SingleBlockImplicitTerminator,
)

from xdsl_quantum.dialects.qu import BitType


@irdl_op_definition
class QscfYieldOp(AbstractYieldOperation[Attribute]):
    name = "qscf.yield"

    traits = lazy_traits_def(
        lambda: (
            IsTerminator(),
            HasParent(QifOp),
            Pure(),
        )
    )


@irdl_op_definition
class QifOp(IRDLOperation):
    """
    Quantum if operation
    """

    name = "qscf.qif"

    output = var_result_def()
    cond = operand_def(BitType)

    true_region = region_def("single_block")
    # TODO this should be optional under certain conditions
    false_region = region_def()

    traits = traits_def(
        SingleBlockImplicitTerminator(QscfYieldOp),
        # RecursiveMemoryEffect(),
        # RecursivelySpeculatable(),
        # IfOpHasCanonicalizationPatternsTrait(),
    )

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
            result_types=[return_types],
            regions=[true_region, false_region],
            attributes=attr_dict,
        )

    @staticmethod
    def parse_region_with_qscfyield(parser: Parser) -> Region:
        region = parser.parse_region()
        block = region.blocks.last
        if block is None:
            block = Block()
            region.add_block(block)
        last_op = block.last_op
        if last_op is not None and last_op.has_trait(IsTerminator):
            return region

        block.add_op(QscfYieldOp())

        return region

    @classmethod
    def parse(cls, parser: Parser) -> Self:
        cond = parser.parse_operand(BitType())
        return_types = []
        if parser.parse_optional_punctuation("->"):
            return_types = parser.parse_comma_separated_list(
                parser.Delimiter.PAREN, parser.parse_type
            )

        then_region = cls.parse_region_with_qscfyield(parser)

        else_region = (
            cls.parse_region_with_qscfyield(parser)
            if parser.parse_optional_keyword("else")
            else Region()
        )

        attr_dict = parser.parse_optional_attr_dict()

        return cls(cond, return_types, then_region, else_region, attr_dict)

    def print(self, printer: Printer):
        printer.print_string(" ")
        printer.print_operand(self.cond)

        print_block_terminators = False
        if bool(self.output):
            printer.print_string(" -> (")
            printer.print_list(self.output.types, printer.print_attribute)
            printer.print_string(")")
            print_block_terminators = True

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
    [QscfYieldOp, QifOp],
    [],
)
