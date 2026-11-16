from collections.abc import Callable

from xdsl.passes import ModulePass


def get_all_passes() -> dict[str, Callable[[], type[ModulePass]]]:
    """Return the list of all available passes."""

    def get_convert_qir_to_llvm():
        from xdsl_quantum.transforms import convert_qir_to_llvm

        return convert_qir_to_llvm.ConvertQIRTLLVMPass

    return {
        "convert-qir-to-llvm": get_convert_qir_to_llvm,
    }
