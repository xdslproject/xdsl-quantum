#!/usr/bin/env python3
"""A template for compilers using xDSL."""

from xdsl.context import Context
from xdsl.dialects import arith, builtin


def get_context() -> Context:
    """Get a context with the dialects required by the compiler."""
    ctx = Context()
    ctx.load_dialect(arith.Arith)
    ctx.load_dialect(builtin.Builtin)
    return ctx


if __name__ == "__main__":
    raise NotImplementedError("Template doesn't implement anything!")
