from collections.abc import Sequence

from xdsl.ir import Attribute, Block, Dialect, Operation, Region, SSAValue
from xdsl.irdl import (
    IRDLOperation,
    operand_def,
    region_def,
    var_result_def,
)


class QifOp(IRDLOperation):
    """
    Base Quantum if operation
    """

    name = "qscf.qif"

    output = var_result_def()
    cond = operand_def()

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
            result_types=[return_types],
            regions=[true_region, false_region],
            attributes=attr_dict,
        )


Qscf = Dialect(
    "qscf",
    [QifOp],
    [],
)
