// RUN: xdsl-opt -p canonicalize %s --split-input-file | filecheck %s

%a1 = angle.constant<pi>
%a2 = angle.constant<pi>

// CHECK: angle.constant<2pi>
%added = angle.add %a1, %a2

"test.op"(%added) : (!angle.type) -> ()

// -----

// CHECK: test.op
%a1 = "test.op"() : () -> !angle.type
%a2 = angle.constant<0pi>

// CHECK-NOT: angle.add
// CHECK-NOT: angle.constant
%added = angle.add %a1, %a2

// CHECK: test.op
"test.op"(%added) : (!angle.type) -> ()

// -----

%a1 = angle.constant<0pi>
// CHECK: test.op
%a2 = "test.op"() : () -> !angle.type

// CHECK-NOT: angle.add
// CHECK-NOT: angle.constant
%added = angle.add %a1, %a2

// CHECK: test.op
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

// CHECK: test.op
"test.op"(%mult) : (!angle.type) -> ()

// -----

%a = angle.constant<pi>

// CHECK: angle.constant<0.5pi>
%mult = angle.scalar_mult 0.5, %a

"test.op"(%mult) : (!angle.type) -> ()

// -----

// Test that two opaque operands are not swapped
// CHECK: %[[a:.*]] = "test.op"
%a = "test.op"() : () -> !angle.type
// CHECK: %[[b:.*]] = "test.op"
%b = "test.op"() : () -> !angle.type

// CHECK: angle.add %[[a]], %[[b]]
%add = angle.add %a, %b

"test.op"(%add) : (!angle.type) -> ()

// -----

// CHECK: %[[a:.*]] = angle.constant
%a = angle.constant<0.5pi>
// CHECK: %[[b:.*]] = "test.op"
%b = "test.op"() : () -> !angle.type

// CHECK: angle.add %[[b]], %[[a]]
%add = angle.add %a, %b

"test.op"(%add) : (!angle.type) -> ()

// -----

// CHECK: %[[a:.*]], %[[b:.*]], %[[c:.*]] = "test.op"
%a, %b, %c = "test.op"() : () -> (!angle.type, !angle.type, !angle.type)

%add_lhs = angle.add %a, %b

// CHECK: %[[d:.*]] = angle.add %[[b]], %[[c]]
// CHECK: angle.add %[[a]], %[[d]]
%add = angle.add %add_lhs, %c

"test.op"(%add) : (!angle.type) -> ()

// -----

// CHECK: %[[a:.*]], %[[c:.*]] = "test.op"
%a, %c = "test.op"() : () -> (!angle.type, !angle.type)
// CHECK: %[[b:.*]] = angle.constant
%b = angle.constant<pi>

%add_lhs = angle.add %a, %b

// CHECK: %[[d:.*]] = angle.add %[[c]], %[[b]]
// CHECK: angle.add %[[a]], %[[d]]
%add = angle.add %add_lhs, %c

"test.op"(%add) : (!angle.type) -> ()

// -----

// CHECK: %[[a:.*]] = angle.constant
%a = angle.constant<pi>
// CHECK: %[[b:.*]], %[[c:.*]] = "test.op"
%b, %c = "test.op"() : () -> (!angle.type, !angle.type)

%add_lhs = angle.add %a, %b

// CHECK: %[[d:.*]] = angle.add %[[c]], %[[a]]
// CHECK: angle.add %[[b]], %[[d]]
%add = angle.add %add_lhs, %c

"test.op"(%add) : (!angle.type) -> ()

// -----

%a = "test.op"() : () -> !angle.type

// CHECK: angle.scalar_mult 2.500000e-01, %{{.*}}
%inner = angle.scalar_mult 0.5, %a
%outer = angle.scalar_mult 0.5, %inner

"test.op"(%outer) : (!angle.type) -> ()

// -----

// CHECK: test.op
%a = "test.op"() : () -> !angle.type

// CHECK-NOT: angle.scalar_mult
%inner = angle.scalar_mult 0.5, %a
%outer = angle.scalar_mult 2.0, %inner

// CHECK: test.op
"test.op"(%outer) : (!angle.type) -> ()
