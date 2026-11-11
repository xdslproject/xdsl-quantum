// RUN: XDSL_ROUNDTRIP
// RUN: XDSL_GENERIC_ROUNDTRIP

// CHECK: %a = angle.constant<0.5pi>
// CHECK-GENERIC: %a = "angle.constant"() <{angle = #angle.attr<0.5pi>}> : () -> !angle.type
%a = angle.constant<0.5pi>

// CHECK-NEXT: %b = angle.add %a, %a
// CHECK-GENERIC-NEXT: %b = "angle.add"(%a, %a) : (!angle.type, !angle.type) -> !angle.type
%b = angle.add %a, %a
