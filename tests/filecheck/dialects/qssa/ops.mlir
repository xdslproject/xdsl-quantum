// RUN: XDSL_ROUNDTRIP
// RUN: XDSL_GENERIC_ROUNDTRIP

// CHECK: "test.op"() : () -> (!qu.bit, !qu.bit)
// CHECK-GENERIC: "test.op"() : () -> (!qu.bit, !qu.bit)
%q0, %q1 = "test.op"() : () -> (!qu.bit, !qu.bit)

// CHECK-NEXT: %q0_1 = qssa.gate<#pauli.x> %q0
// CHECK-GENERIC-NEXT: %q0_1 = "qssa.gate"(%q0) <{gate = #pauli.x, operandSegmentSizes = array<i32: 0, 1>}> : (!qu.bit) -> !qu.bit
%q0_1 = qssa.gate<#pauli.x> %q0

// CHECK-NEXT: %q0_2 = qssa.gate<#gate.id> %q0_1
// CHECK-GENERIC-NEXT: %q0_2 = "qssa.gate"(%q0_1) <{gate = #gate.id, operandSegmentSizes = array<i32: 0, 1>}> : (!qu.bit) -> !qu.bit
%q0_2 = qssa.gate<#gate.id> %q0_1

// CHECK-NEXT: %q0_3, %q1_1 = qssa.gate<#gate.id> %q0_2, %q1
// CHECK-GENERIC-NEXT: %q0_3, %q1_1 = "qssa.gate"(%q0_2, %q1) <{gate = #gate.id, operandSegmentSizes = array<i32: 0, 2>}> : (!qu.bit, !qu.bit) -> (!qu.bit, !qu.bit)
%q0_3, %q1_1 = qssa.gate<#gate.id> %q0_2, %q1

// Test rotation gates with angle parameters
// CHECK: %angle = "test.op"() : () -> !angle.type
%angle = "test.op"() : () -> !angle.type

// CHECK: %q_rx = qssa.gate<#gate.rx>[%angle] %q0_3
// CHECK-GENERIC: %q_rx = "qssa.gate"(%angle, %q0_3) <{gate = #gate.rx, operandSegmentSizes = array<i32: 1, 1>}> : (!angle.type, !qu.bit) -> !qu.bit
%q_rx = qssa.gate<#gate.rx>[%angle] %q0_3

// CHECK: %q_ry = qssa.gate<#gate.ry>[%angle] %q_rx
// CHECK-GENERIC: %q_ry = "qssa.gate"(%angle, %q_rx) <{gate = #gate.ry, operandSegmentSizes = array<i32: 1, 1>}> : (!angle.type, !qu.bit) -> !qu.bit
%q_ry = qssa.gate<#gate.ry>[%angle] %q_rx

// CHECK: %q_rz = qssa.gate<#gate.rz>[%angle] %q_ry
// CHECK-GENERIC: %q_rz = "qssa.gate"(%angle, %q_ry) <{gate = #gate.rz, operandSegmentSizes = array<i32: 1, 1>}> : (!angle.type, !qu.bit) -> !qu.bit
%q_rz = qssa.gate<#gate.rz>[%angle] %q_ry
