// RUN: XDSL_ROUNDTRIP
// RUN: XDSL_GENERIC_ROUNDTRIP

// CHECK: %a = angle.constant<pi/2>
// CHECK-GENERIC: %a = "angle.constant"() <{angle = #angle.attr<pi/2>}> : () -> !angle.type
%a = angle.constant<pi/2>

// CHECK-NEXT: %b = angle.add %a, %a
// CHECK-GENERIC-NEXT: %b = "angle.add"(%a, %a) : (!angle.type, !angle.type) -> !angle.type
%b = angle.add %a, %a
