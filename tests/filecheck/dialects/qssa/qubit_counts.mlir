// RUN: xdsl-opt %s --verify-diagnostics --split-input-file | filecheck %s

%q0 = "test.op"() : () -> !qu.bit

// CHECK: integer 1 expected from int variable 'Q', but got 2
%q1, %q2 = "qssa.gate"(%q0) <{"gate" = #pauli.x, "operandSegmentSizes" = array<i32: 0, 1>}> : (!qu.bit) -> (!qu.bit, !qu.bit)

// -----

%q0, %q1 = "test.op"() : () -> (!qu.bit, !qu.bit)

// CHECK: integer 2 expected from int variable 'Q', but got 1
%q2 = "qssa.gate"(%q0, %q1) <{"gate" = #pauli.x, "operandSegmentSizes" = array<i32: 0, 2>}> : (!qu.bit, !qu.bit) -> !qu.bit

// -----

%q0, %q1 = "test.op"() : () -> (!qu.bit, !qu.bit)

// CHECK: integer 2 expected from int variable 'Q', but got 1
%q2, %q3 = "qssa.gate"(%q0, %q1) <{"gate" = #pauli.x, "operandSegmentSizes" = array<i32: 0, 2>}> : (!qu.bit, !qu.bit) -> (!qu.bit, !qu.bit)
