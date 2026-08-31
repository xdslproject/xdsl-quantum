// RUN: XDSL_ROUNDTRIP
// RUN: XDSL_GENERIC_ROUNDTRIP

// CHECK: "test.op"() : () -> !qu.bit
// CHECK-GENERIC: "test.op"() : () -> !qu.bit
%q0 = "test.op"() : () -> !qu.bit

// CHECK-NEXT: %q1 = qssa.gate<#pauli.x> %q0
// CHECK-GENERIC-NEXT: %q1 = "qssa.gate"(%q0) <{gate = #pauli.x}> : (!qu.bit) -> !qu.bit
%q1 = qssa.gate<#pauli.x> %q0
