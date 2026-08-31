// RUN: XDSL_ROUNDTRIP
// RUN: XDSL_GENERIC_ROUNDTRIP

// CHECK: "test.op"() : () -> (!qu.bit, !qu.bit)
// CHECK-GENERIC: "test.op"() : () -> (!qu.bit, !qu.bit)
%q0, %q1 = "test.op"() : () -> (!qu.bit, !qu.bit)

// CHECK-NEXT: %q0_1 = qssa.gate<#pauli.x> %q0
// CHECK-GENERIC-NEXT: %q0_1 = "qssa.gate"(%q0) <{gate = #pauli.x}> : (!qu.bit) -> !qu.bit
%q0_1 = qssa.gate<#pauli.x> %q0

// CHECK-NEXT: %q0_2 = qssa.gate<#gate.id> %q0_1
// CHECK-GENERIC-NEXT: %q0_2 = "qssa.gate"(%q0_1) <{gate = #gate.id}> : (!qu.bit) -> !qu.bit
%q0_2 = qssa.gate<#gate.id> %q0_1

// CHECK-NEXT: %q0_3, %q1_1 = qssa.gate<#gate.id> %q0_2, %q1
// CHECK-GENERIC-NEXT: %q0_3, %q1_1 = "qssa.gate"(%q0_2, %q1) <{gate = #gate.id}> : (!qu.bit, !qu.bit) -> (!qu.bit, !qu.bit)
%q0_3, %q1_1 = qssa.gate<#gate.id> %q0_2, %q1
