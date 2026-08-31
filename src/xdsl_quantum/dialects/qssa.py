from typing import ClassVar

from xdsl.ir import Dialect, Operation, SSAValue
from xdsl.irdl import (
    AnyInt,
    IntVarConstraint,
    IRDLOperation,
    RangeOf,
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

    _Q: ClassVar = IntVarConstraint("Q", AnyInt())

    gate = prop_def(QuantumOperationConstraint.gate(_Q))

    in_qubits = var_operand_def(RangeOf(BitType()).of_length(_Q))

    out_qubits = var_result_def(RangeOf(BitType()).of_length(_Q))

    assembly_format = "`<` $gate `>` $in_qubits attr-dict"

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
