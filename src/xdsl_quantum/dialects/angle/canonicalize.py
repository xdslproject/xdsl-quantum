"""Angle dialect canonicalization patterns."""

from xdsl.pattern_rewriter import (
    PatternRewriter,
    RewritePattern,
    op_type_rewrite_pattern,
)
from xdsl.traits import ConstantLike

from xdsl_quantum.dialects.angle.attrs import AngleAttr

from .ops import AddAngleOp, ScalarMultOp


class ScalarMultCombinePattern(RewritePattern):
    """
    Combine nested scalar multiplications: a * (b * angle) = (a * b) * angle.
    """

    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: ScalarMultOp, rewriter: PatternRewriter, /):
        # Check if the angle operand is itself a scalar_mult
        inner_op = op.angle.owner
        if not isinstance(inner_op, ScalarMultOp):
            return

        # Compute the product
        combined_scalar = op.scalar.value.data * inner_op.scalar.value.data

        # Otherwise, create new scalar_mult with combined scalar and inner angle
        new_op = ScalarMultOp(combined_scalar, inner_op.angle)
        rewriter.replace(op, new_op)


class AddCommutativePattern(RewritePattern):
    """
    Move constants to the right hand side.
    """

    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: AddAngleOp, rewriter: PatternRewriter, /):
        lhs = ConstantLike.get_constant_value(op.lhs)
        if not isinstance(lhs, AngleAttr):
            return
        # rhs should be non-constant, or folding would have happened
        assert ConstantLike.get_constant_value(op.rhs) is None
        rewriter.replace(op, AddAngleOp(op.rhs, op.lhs))


class AddAssocPattern(RewritePattern):
    """
    Reassociate (a + b) + c to a + (b + c)
    """

    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: AddAngleOp, rewriter: PatternRewriter, /):
        if not isinstance(op.lhs.owner, AddAngleOp):
            return
        rewriter.replace(
            op,
            (
                new_rhs := AddAngleOp(op.lhs.owner.rhs, op.rhs),
                AddAngleOp(op.lhs.owner.lhs, new_rhs),
            ),
        )
