// RUN: XDSL_ROUNDTRIP
// RUN: XDSL_GENERIC_ROUNDTRIP

// CHECK: "test.op"() {angle = #angle.attr<0>} : () -> ()
"test.op"() {angle = #angle.attr<0>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<pi>} : () -> ()
"test.op"() {angle = #angle.attr<pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0>} : () -> ()
"test.op"() {angle = #angle.attr<2pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0.5pi>} : () -> ()
"test.op"() {angle = #angle.attr<0.5pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<1.5pi>} : () -> ()
"test.op"() {angle = #angle.attr<1.5pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0.5pi>} : () -> ()
"test.op"() {angle = #angle.attr<2.5pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<1.5pi>} : () -> ()
"test.op"() {angle = #angle.attr<-0.5pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<pi>} : () -> ()
"test.op"() {angle = #angle.attr<-pi>} : () -> ()

// CHECK-NEXT: %a = angle.constant<pi>
// CHECK-GENERIC: %a = "angle.constant"() <{angle = #angle.attr<pi>}> : () -> !angle.type
%a = angle.constant<pi>
