from collections.abc import Sequence

from xdsl.dialects.builtin import Float64Type, FloatAttr
from xdsl.interfaces import HasCanonicalizationPatternsInterface, HasFolderInterface
from xdsl.ir import Attribute, Operation, SSAValue
from xdsl.irdl import (
    IRDLOperation,
    irdl_op_definition,
    operand_def,
    prop_def,
    result_def,
    traits_def,
)
from xdsl.pattern_rewriter import RewritePattern
from xdsl.traits import ConstantLike, Pure

from .attrs import AngleAttr, AngleType


@irdl_op_definition
class ConstantAngleOp(IRDLOperation, HasFolderInterface):
    """
    Constant-like operation for producing angles.
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

    def fold(self) -> Sequence[SSAValue | Attribute] | None:
        return (self.angle,)


@irdl_op_definition
class AddAngleOp(IRDLOperation, HasFolderInterface):
    """
    Adds two angles.
    """

    name = "angle.add"

    lhs = operand_def(AngleType)

    rhs = operand_def(AngleType)

    out = result_def(AngleType)

    assembly_format = "$lhs `,` $rhs attr-dict"

    def __init__(self, lhs: SSAValue | Operation, rhs: SSAValue | Operation):
        super().__init__(operands=(lhs, rhs), result_types=(AngleType(),))

    def fold(self) -> Sequence[SSAValue | Attribute] | None:
        lhs = ConstantLike.get_constant_value(self.lhs)
        rhs = ConstantLike.get_constant_value(self.rhs)
        if lhs == AngleAttr(0):
            return (self.rhs,)
        if rhs == AngleAttr(0):
            return (self.lhs,)
        if isinstance(lhs, AngleAttr) and isinstance(rhs, AngleAttr):
            return (lhs + rhs,)


@irdl_op_definition
class ScalarMultOp(
    IRDLOperation, HasFolderInterface, HasCanonicalizationPatternsInterface
):
    """
    Scalar multiplication operation.
    Multiplies an angle by a scalar float value.
    """

    name = "angle.scalar_mult"

    scalar = prop_def(FloatAttr.constr(Float64Type()))
    angle = operand_def(AngleType)
    result = result_def(AngleType)

    assembly_format = "$scalar `,` $angle attr-dict"

    traits = traits_def(Pure())

    def __init__(self, scalar: float | FloatAttr[Float64Type], angle: SSAValue):
        if isinstance(scalar, int | float):
            scalar = FloatAttr(scalar, Float64Type())
        super().__init__(
            operands=[angle],
            properties={"scalar": scalar},
            result_types=[AngleType()],
        )

    @classmethod
    def get_canonicalization_patterns(cls) -> tuple[RewritePattern, ...]:
        from .canonicalize import ScalarMultCombinePattern

        return (ScalarMultCombinePattern(),)

    def fold(self) -> Sequence[SSAValue | Attribute] | None:
        scalar_value = self.scalar.value.data
        if scalar_value == 0:
            return (AngleAttr(0),)
        if scalar_value == 1.0:
            return (self.angle,)
        const_angle = ConstantLike.get_constant_value(self.angle)
        if isinstance(const_angle, AngleAttr):
            return (const_angle * scalar_value,)
