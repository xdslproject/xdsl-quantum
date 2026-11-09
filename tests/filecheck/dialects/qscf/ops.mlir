// RUN: XDSL_ROUNDTRIP


  %0 = "test.op"() : () -> !qu.bit
  qscf.qif %0 {
    "test.op"() {gate = #gate.s} : () -> ()
  } else {
    "test.op"() {gate = #gate.id} : () -> ()
  }

  // CHECK:      %{{.*}} = "test.op"() : () -> !qu.bit
  // CHECK-NEXT: qscf.qif %{{.*}} {
  // CHECK-NEXT:   "test.op"() {gate = #gate.s} : () -> ()
  // CHECK-NEXT: } else {
  // CHECK-NEXT:   "test.op"() {gate = #gate.id} : () -> ()
  // CHECK-NEXT: }


  %3 = qscf.qif %0 -> (!qu.bit) {
    %4 = "test.op"() : () -> !qu.bit
    qscf.yield %4 : !qu.bit
  } else {
    %5 = "test.op"() : () -> !qu.bit
    qscf.yield %5 : !qu.bit
  }

  // CHECK:      %{{.*}} = qscf.qif %{{.*}} -> (!qu.bit) {
  // CHECK-NEXT:   %{{.*}} = "test.op"() : () -> !qu.bit
  // CHECK-NEXT:   qscf.yield %{{.*}} : !qu.bit
  // CHECK-NEXT: } else {
  // CHECK-NEXT:   %{{.*}} = "test.op"() : () -> !qu.bit
  // CHECK-NEXT:   qscf.yield %{{.*}} : !qu.bit
  // CHECK-NEXT: }

  qscf.qif %0 {}

  // CHECK: qscf.qif %{{.*}} {
  // CHECK-NEXT: }
