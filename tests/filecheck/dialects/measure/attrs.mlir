// RUN: XDSL_ROUNDTRIP

// CHECK: "test.op"() {measure = #measure.x} : () -> ()
"test.op"() {measure = #measure.x} : () -> ()

// CHECK-NEXT: "test.op"() {measure = #measure.y} : () -> ()
"test.op"() {measure = #measure.y} : () -> ()

// CHECK-NEXT: "test.op"() {measure = #measure.z} : () -> ()
"test.op"() {measure = #measure.z} : () -> ()
