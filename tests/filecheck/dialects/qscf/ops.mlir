// RUN: XDSL_ROUNDTRIP


  %0 = "test.op"() : () -> !qu.ref
  qscf.qif %0 {
    "test.op"() {gate = #gate.s} : () -> ()
  } else {
    "test.op"() {gate = #gate.id} : () -> ()
  }

  // CHECK:      %{{.*}} = "test.op"() : () -> !qu.ref
  // CHECK-NEXT: qscf.qif %{{.*}} {
  // CHECK-NEXT:   "test.op"() {gate = #gate.s} : () -> ()
  // CHECK-NEXT: } else {
  // CHECK-NEXT:   "test.op"() {gate = #gate.id} : () -> ()
  // CHECK-NEXT: }

  qscf.qif %0 {"test.op"() {gate = #gate.s} : () -> ()} else {}

  // CHECK: qscf.qif %{{.*}} {
  // CHECK-NEXT: }
