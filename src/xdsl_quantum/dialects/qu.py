from xdsl.ir import Dialect, Operation, ParametrizedAttribute, SSAValue, TypeAttribute
from xdsl.irdl import (
    IRDLOperation,
    irdl_attr_definition,
    irdl_op_definition,
    operand_def,
    result_def,
)


@irdl_attr_definition
class BitType(ParametrizedAttribute, TypeAttribute):
    """
    Type for a single qubit.
    """

    name = "qu.bit"


@irdl_attr_definition
class RefType(ParametrizedAttribute, TypeAttribute):
    """
    Reference to a qubit
    """

    name = "qu.ref"


@irdl_op_definition
class LoadOp(IRDLOperation):
    """
    Load operation that converts a qubit reference to a qubit value.
    """

    name = "qu.load"

    ref = operand_def(RefType)
    qubit = result_def(BitType)

    assembly_format = "$ref attr-dict"

    def __init__(self, ref: SSAValue | Operation):
        super().__init__(operands=(ref,), result_types=(BitType(),))


Qu = Dialect(
    "qu",
    [
        LoadOp,
    ],
    [
        BitType,
        RefType,
    ],
)
