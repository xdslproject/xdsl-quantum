// RUN: XDSL_ROUNDTRIP
// RUN: XDSL_GENERIC_ROUNDTRIP

// CHECK: %ref = "test.op"() : () -> !qu.ref
// CHECK-GENERIC: %ref = "test.op"() : () -> !qu.ref
%ref = "test.op"() : () -> !qu.ref

// CHECK-NEXT: %qubit = qu.load %ref
// CHECK-GENERIC-NEXT: %qubit = "qu.load"(%ref) : (!qu.ref) -> !qu.bit
%qubit = qu.load %ref
