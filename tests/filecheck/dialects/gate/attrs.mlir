// RUN: XDSL_ROUNDTRIP

// Test gate attributes
"test.op"() {
  // CHECK: id_gate = #gate.id
  id_gate = #gate.id,
  // CHECK-SAME: s_gate = #gate.s
  s_gate = #gate.s,
  // CHECK-SAME: t_gate = #gate.t
  t_gate = #gate.t,
  // CHECK-SAME: control_id = #gate.control<#gate.id>
  control_id = #gate.control<#gate.id>,
  // CHECK-SAME: control_s = #gate.control<#gate.s>
  control_s = #gate.control<#gate.s>,
  // CHECK-SAME: control_t = #gate.control<#gate.t>
  control_t = #gate.control<#gate.t>,
  // CHECK-SAME: cond_id = #gate.cond<#gate.id>
  cond_id = #gate.cond<#gate.id>,
  // CHECK-SAME: cond_s = #gate.cond<#gate.s>
  cond_s = #gate.cond<#gate.s>,
  // CHECK-SAME: cond_t = #gate.cond<#gate.t>
  cond_t = #gate.cond<#gate.t>,
  // CHECK-SAME: rx_gate = #gate.rx
  rx_gate = #gate.rx,
  // CHECK-SAME: ry_gate = #gate.ry
  ry_gate = #gate.ry,
  // CHECK-SAME: rz_gate = #gate.rz
  rz_gate = #gate.rz
} : () -> ()
