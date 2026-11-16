// RUN: xdsl-opt %s --verify-diagnostics

// CHECK: Expected gate with no classical outputs
"test.op"() {bad = #gate.control<#measure.x>} : () -> ()
