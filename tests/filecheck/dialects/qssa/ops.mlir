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

// CHECK-NEXT: %q0_4, %q1_2 = qssa.gate<#gate.control<#pauli.x>> %q0_3, %q1_1
// CHECK-GENERIC-NEXT: %q0_4, %q1_2 = "qssa.gate"(%q0_3, %q1_1) <{gate = #gate.control<#pauli.x>, operandSegmentSizes = array<i32: 0, 2>}> : (!qu.bit, !qu.bit) -> (!qu.bit, !qu.bit)
%q0_4, %q1_2 = qssa.gate<#gate.control<#pauli.x>> %q0_3, %q1_1

// CHECK-NEXT: %angle = "test.op"() : () -> !angle.type
%angle = "test.op"() : () -> !angle.type

// CHECK-NEXT: %q_rx = qssa.gate<#gate.rx>[%angle] %q0_3
// CHECK-GENERIC: %q_rx = "qssa.gate"(%angle, %q0_3) <{gate = #gate.rx, operandSegmentSizes = array<i32: 1, 1>}> : (!angle.type, !qu.bit) -> !qu.bit
%q_rx = qssa.gate<#gate.rx>[%angle] %q0_3

// CHECK-NEXT: %q_ry = qssa.gate<#gate.ry>[%angle] %q_rx
// CHECK-GENERIC-NEXT: %q_ry = "qssa.gate"(%angle, %q_rx) <{gate = #gate.ry, operandSegmentSizes = array<i32: 1, 1>}> : (!angle.type, !qu.bit) -> !qu.bit
%q_ry = qssa.gate<#gate.ry>[%angle] %q_rx

// CHECK-NEXT: %q_rz = qssa.gate<#gate.rz>[%angle] %q_ry
// CHECK-GENERIC-NEXT: %q_rz = "qssa.gate"(%angle, %q_ry) <{gate = #gate.rz, operandSegmentSizes = array<i32: 1, 1>}> : (!angle.type, !qu.bit) -> !qu.bit
%q_rz = qssa.gate<#gate.rz>[%angle] %q_ry

// CHECK-NEXT: %m0, %q_m0 = qssa.measure<#measure.x> %q0_4
// CHECK-GENERIC-NEXT: %m0, %q_m0 = "qssa.measure"(%q0_4) <{gate = #measure.x, operandSegmentSizes = array<i32: 0, 1>}> : (!qu.bit) -> (i1, !qu.bit)
%m0, %q_m0 = qssa.measure<#measure.x> %q0_4

// CHECK-NEXT: %m1, %q_m1 = qssa.measure<#measure.y> %q1_2
// CHECK-GENERIC-NEXT: %m1, %q_m1 = "qssa.measure"(%q1_2) <{gate = #measure.y, operandSegmentSizes = array<i32: 0, 1>}> : (!qu.bit) -> (i1, !qu.bit)
%m1, %q_m1 = qssa.measure<#measure.y> %q1_2

// CHECK-NEXT: %m2, %q_m2 = qssa.measure<#measure.z> %q_m0
// CHECK-GENERIC-NEXT: %m2, %q_m2 = "qssa.measure"(%q_m0) <{gate = #measure.z, operandSegmentSizes = array<i32: 0, 1>}> : (!qu.bit) -> (i1, !qu.bit)
%m2, %q_m2 = qssa.measure<#measure.z> %q_m0

// CHECK-NEXT: %m3, %q_m3 = qssa.measure<#measure.z> %q_m1
// CHECK-GENERIC-NEXT: %m3, %q_m3 = "qssa.measure"(%q_m1) <{gate = #measure.z, operandSegmentSizes = array<i32: 0, 1>}> : (!qu.bit) -> (i1, !qu.bit)
%m3, %q_m3 = qssa.measure<#measure.z> %q_m1
