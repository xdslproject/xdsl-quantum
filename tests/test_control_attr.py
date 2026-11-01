import pytest
from xdsl.ir import VerifyException

from xdsl_quantum.dialects.gate import ControlGate
from xdsl_quantum.dialects.measure import XMeasure


def test_controlled_gate() -> None:

    with pytest.raises(
        VerifyException,
        match="""parameter 'inner' does not verify:\nincorrect length for
              range variable:\nInvalid value 1, expected 0""",
    ):
        ControlGate(XMeasure())
