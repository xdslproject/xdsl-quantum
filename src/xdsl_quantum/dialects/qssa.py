from typing import ClassVar

from xdsl.ir import Dialect, Operation, SSAValue
from xdsl.irdl import (
    AnyInt,
    AnyRange,
    AttrSizedOperandSegments,
    IntVarConstraint,
    IRDLOperation,
    RangeOf,
    RangeVarConstraint,
    irdl_op_definition,
    prop_def,
    var_operand_def,
    var_result_def,
)

from xdsl_quantum.dialects.qu import BitType
from xdsl_quantum.quantum_operation import (
    QuantumOperationAttribute,
    QuantumOperationConstraint,
)


@irdl_op_definition
class GateOp(IRDLOperation):
    name = "qssa.gate"

    _P: ClassVar = RangeVarConstraint("P", AnyRange())
    _Q: ClassVar = IntVarConstraint("Q", AnyInt())

    gate = prop_def(QuantumOperationConstraint.gate(_P, _Q))

    params = var_operand_def(_P)

    in_qubits = var_operand_def(RangeOf(BitType()).of_length(_Q))

    out_qubits = var_result_def(RangeOf(BitType()).of_length(_Q))

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


Qssa = Dialect(
    "qssa",
    [
        GateOp,
    ],
    [],
)
