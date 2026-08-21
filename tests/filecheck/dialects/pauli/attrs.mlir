// RUN: XDSL_ROUNDTRIP

// CHECK: "test.op"() {gate = #pauli.x} : () -> ()
"test.op"() {gate = #pauli.x} : () -> ()

// CHECK-NEXT: "test.op"() {gate = #pauli.y} : () -> ()
"test.op"() {gate = #pauli.y} : () -> ()

// CHECK-NEXT: "test.op"() {gate = #pauli.z} : () -> ()
"test.op"() {gate = #pauli.z} : () -> ()
