// RUN: XDSL_ROUNDTRIP

// CHECK: "test.op"() {angle = #angle.attr<0>} : () -> ()
"test.op"() {angle = #angle.attr<0>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0>} : () -> ()
"test.op"() {angle = #angle.attr<0pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0>} : () -> ()
"test.op"() {angle = #angle.attr<0pi/1>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0>} : () -> ()
"test.op"() {angle = #angle.attr<0pi/2>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<1pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<pi/1>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<1pi/1>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0>} : () -> ()
"test.op"() {angle = #angle.attr<2pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<-pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi>} : () -> ()
"test.op"() {angle = #angle.attr<-1pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<0>} : () -> ()
"test.op"() {angle = #angle.attr<-2pi>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<pi/2>} : () -> ()
"test.op"() {angle = #angle.attr<pi/2>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<pi/2>} : () -> ()
"test.op"() {angle = #angle.attr<1pi/2>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi/2>} : () -> ()
"test.op"() {angle = #angle.attr<3pi/2>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi/2>} : () -> ()
"test.op"() {angle = #angle.attr<-pi/2>} : () -> ()

// CHECK-NEXT: "test.op"() {angle = #angle.attr<-pi/2>} : () -> ()
"test.op"() {angle = #angle.attr<-1pi/2>} : () -> ()
