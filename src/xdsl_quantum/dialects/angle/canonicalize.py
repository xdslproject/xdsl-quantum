"""Angle dialect canonicalization patterns."""

from xdsl.pattern_rewriter import (
    PatternRewriter,
    RewritePattern,
    op_type_rewrite_pattern,
)

from .ops import ScalarMultOp


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
