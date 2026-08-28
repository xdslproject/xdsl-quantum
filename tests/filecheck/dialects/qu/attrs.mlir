// RUN: XDSL_ROUNDTRIP

// CHECK: "test.op"() : () -> !qu.bit
%0 = "test.op"() : () -> !qu.bit
