// RUN: XDSL_ROUNDTRIP

// CHECK: "test.op"() {gate = #gate.id} : () -> ()
"test.op"() {gate = #gate.id} : () -> ()

// CHECK: "test.op"() {gate = #gate.s} : () -> ()
"test.op"() {gate = #gate.s} : () -> ()

// CHECK: "test.op"() {gate = #gate.t} : () -> ()
"test.op"() {gate = #gate.t} : () -> ()

// CHECK: "test.op"() {gate = #gate.control<#gate.id>} : () -> ()
"test.op"() {gate = #gate.control<#gate.id>} : () -> ()

// CHECK: "test.op"() {gate = #gate.control<#gate.s>} : () -> ()
"test.op"() {gate = #gate.control<#gate.s>} : () -> ()

// CHECK: "test.op"() {gate = #gate.control<#gate.t>} : () -> ()
"test.op"() {gate = #gate.control<#gate.t>} : () -> ()
