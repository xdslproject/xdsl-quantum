// RUN: XDSL_ROUNDTRIP

// CHECK: "test.op"() {gate = #gate.id} : () -> ()
"test.op"() {gate = #gate.id} : () -> ()

// CHECK: "test.op"() {gate = #gate.s} : () -> ()
"test.op"() {gate = #gate.s} : () -> ()

// CHECK: "test.op"() {gate = #gate.t} : () -> ()
"test.op"() {gate = #gate.t} : () -> ()

// CHECK: "test.op"() {gate = #gate.rx} : () -> ()
"test.op"() {gate = #gate.rx} : () -> ()

// CHECK: "test.op"() {gate = #gate.ry} : () -> ()
"test.op"() {gate = #gate.ry} : () -> ()

// CHECK: "test.op"() {gate = #gate.rz} : () -> ()
"test.op"() {gate = #gate.rz} : () -> ()
