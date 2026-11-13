// RUN: XDSL_ROUNDTRIP

// CHECK: "test.op"() {angle = #angle.attr<0pi>} : () -> ()
"test.op"() {angle = #angle.attr<0pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0pi>} : () -> ()
"test.op"() {angle = #angle.attr<0.0pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<1pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<1.0pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0pi>} : () -> ()
"test.op"() {angle = #angle.attr<2pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<-pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<-1pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0pi>} : () -> ()
"test.op"() {angle = #angle.attr<-2pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0.5pi>} : () -> ()
"test.op"() {angle = #angle.attr<0.5pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-0.5pi>} : () -> ()
"test.op"() {angle = #angle.attr<1.5pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-0.5pi>} : () -> ()
"test.op"() {angle = #angle.attr<-0.5pi>} : () -> ()
