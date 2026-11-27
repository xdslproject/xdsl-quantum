from typing import ClassVar

from xdsl.dialects.builtin import i1
from xdsl.ir import Dialect, Operation, SSAValue
from xdsl.irdl import (
    AttrSizedOperandSegments,
    IntVarConstraint,
    IRDLOperation,
    RangeOf,
    RangeVarConstraint,
    irdl_op_definition,
    prop_def,
    result_def,
    var_operand_def,
    var_result_def,
)

from xdsl_quantum.core.operation import (
    MeasurementAttribute,
    QuantumOperationAttribute,
    QuantumOperationConstraint,
)
from xdsl_quantum.dialects.qu import BitType


@irdl_op_definition
class GateOp(IRDLOperation):
    """
    QSSA Gate Operation.
    This operation takes optional classical inputs and returns no classical outputs.
    As it is a QSSA operation, the number of input and output qubits must be equal.
    """

    name = "qssa.gate"

    _P: ClassVar = RangeVarConstraint.get("P")
    _Q: ClassVar = IntVarConstraint.get("Q")

    gate = prop_def(QuantumOperationConstraint.gate(_P, _Q))

    params = var_operand_def(_P)

    in_qubits = var_operand_def(RangeOf.get(BitType()).of_length(_Q))

    out_qubits = var_result_def(RangeOf.get(BitType()).of_length(_Q))

    assembly_format = "`<` $gate `>` (`` `[` $params^ `]`)? $in_qubits attr-dict"

    irdl_options = (AttrSizedOperandSegments(as_property=True),)

    def __init__(
        self,
        gate: QuantumOperationAttribute,
        *in_qubits: SSAValue | Operation,
    ):
        super().__init__(
            operands=(in_qubits),
            properties={
                "gate": gate,
            },
            result_types=((BitType(),) * len(in_qubits),),
        )


@irdl_op_definition
class MeasureOp(IRDLOperation):
    name = "qssa.measure"

    _P: ClassVar = RangeVarConstraint.get("P")
    _Q: ClassVar = IntVarConstraint.get("Q")

    gate = prop_def(QuantumOperationConstraint.measurement(_P, _Q))

    params = var_operand_def(_P)

    in_qubits = var_operand_def(RangeOf.get(BitType()).of_length(_Q))

    result = result_def(i1)
    out_qubits = var_result_def(RangeOf.get(BitType()).of_length(_Q))

    assembly_format = "`<` $gate `>` (`` `[` $params^ `]`)? $in_qubits attr-dict"

    irdl_options = (AttrSizedOperandSegments(as_property=True),)

    def __init__(
        self,
        gate: MeasurementAttribute,
        *in_qubits: SSAValue | Operation,
        params: tuple[SSAValue | Operation, ...] = (),
    ):
        super().__init__(
            operands=(params, in_qubits),
            properties={
                "gate": gate,
            },
            result_types=(i1, (BitType(),) * len(in_qubits)),
        )


Qssa = Dialect(
    "qssa",
    [
        GateOp,
        MeasureOp,
    ],
    [],
)
