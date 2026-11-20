// RUN: xdsl-opt -p canonicalize %s --split-input-file | filecheck %s

%a1 = angle.constant<pi>
%a2 = angle.constant<pi>

// CHECK: angle.constant<2pi>
%added = angle.add %a1, %a2

"test.op"(%added) : (!angle.type) -> ()

// -----

%a = angle.constant<pi>

// CHECK: angle.constant<0pi>
// CHECK-NOT: angle.scalar_mult
%mult = angle.scalar_mult 0.0, %a

"test.op"(%mult) : (!angle.type) -> ()

// -----

%a = angle.constant<pi>

// CHECK: angle.constant<pi>
// CHECK-NOT: angle.scalar_mult
%mult = angle.scalar_mult 1.0, %a

"test.op"(%mult) : (!angle.type) -> ()

// -----

%a = angle.constant<pi>

// CHECK: angle.constant<0.5pi>
%mult = angle.scalar_mult 0.5, %a

"test.op"(%mult) : (!angle.type) -> ()

// -----

%a = "test.op"() : () -> !angle.type

// CHECK: angle.scalar_mult 2.500000e-01, %{{.*}}
%inner = angle.scalar_mult 0.5, %a
%outer = angle.scalar_mult 0.5, %inner

"test.op"(%outer) : (!angle.type) -> ()

// -----

%a = "test.op"() : () -> !angle.type

// CHECK-NOT: angle.scalar_mult
%inner = angle.scalar_mult 0.5, %a
%outer = angle.scalar_mult 2.0, %inner

"test.op"(%outer) : (!angle.type) -> ()
