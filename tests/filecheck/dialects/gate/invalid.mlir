// RUN: xdsl-opt %s --parsing-diagnostics --split-input-file | filecheck %s

// CHECK: Expected gate with no classical outputs
"test.op"() {bad = #gate.control<#measure.x>} : () -> ()

// -----

// CHECK: Expected gate with no classical outputs
"test.op"() {bad = #gate.cond<#measure.x>} : () -> ()
