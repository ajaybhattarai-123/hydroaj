//! Pressurized Pipe Flow & Hydrodynamics Module
//! High-performance Rayon-parallelized computations for friction loss,
//! empirical equations, minor losses, and water hammer transients.

use rayon::prelude::*;
use std::f64::consts::PI;

/// Darcy-Weisbach head loss: h_f = f * (L / D) * (V^2 / (2 * g))
pub fn darcy_weisbach_kernel(
    f: &[f64],
    length: &[f64],
    diameter: &[f64],
    velocity: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = f.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let f_val = f[i];
            let l_val = length[i];
            let d_val = diameter[i];
            let v_val = velocity[i];

            if f_val <= 0.0 || l_val < 0.0 || d_val <= 0.0 || v_val < 0.0 || g <= 0.0
                || f_val.is_nan() || l_val.is_nan() || d_val.is_nan() || v_val.is_nan() {
                f64::NAN
            } else {
                f_val * (l_val / d_val) * (v_val * v_val / (2.0 * g))
            }
        })
        .collect()
}

/// Reynolds Number: Re = (V * D) / nu
pub fn reynolds_number_kernel(
    velocity: &[f64],
    diameter: &[f64],
    kinematic_viscosity: &[f64],
) -> Vec<f64> {
    let n = velocity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v = velocity[i];
            let d = diameter[i];
            let nu = kinematic_viscosity[i];

            if v < 0.0 || d <= 0.0 || nu <= 0.0 || v.is_nan() || d.is_nan() || nu.is_nan() {
                f64::NAN
            } else {
                (v * d) / nu
            }
        })
        .collect()
}

/// Laminar friction factor: f = 64 / Re
pub fn laminar_friction_kernel(
    reynolds: &[f64],
) -> Vec<f64> {
    let n = reynolds.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let re = reynolds[i];
            if re <= 0.0 || re.is_nan() {
                f64::NAN
            } else {
                64.0 / re
            }
        })
        .collect()
}

/// Vectorized Colebrook-White friction factor solver via parallel Newton-Raphson:
/// 1 / sqrt(f) = -2.0 * log10((epsilon / D) / 3.7 + 2.51 / (Re * sqrt(f)))
///
/// Uses Swamee-Jain approximation as initial seed for rapid convergence (< 3 iterations).
pub fn colebrook_white_kernel(
    eps_over_d: &[f64],
    reynolds: &[f64],
) -> Vec<f64> {
    let n = eps_over_d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ed = eps_over_d[i];
            let re = reynolds[i];

            if ed < 0.0 || re <= 0.0 || ed.is_nan() || re.is_nan() {
                return f64::NAN;
            }

            // Laminar flow regime
            if re < 2000.0 {
                return 64.0 / re;
            }

            // Swamee-Jain initial seed for x = 1 / sqrt(f)
            let ed_term = ed / 3.7;
            let sj_denom = (ed_term + 5.74 / re.powf(0.9)).log10();
            let mut x = if sj_denom.abs() > 1e-12 {
                // x = 1/sqrt(f) = -2 * log10(ed/3.7 + 5.74/Re^0.9)
                -2.0 * sj_denom
            } else {
                7.0 // typical default ~ f = 0.02
            };

            if x <= 0.0 {
                x = 7.0;
            }

            let ln10 = std::f64::consts::LN_10;

            // Newton-Raphson iteration on g(x) = x + 2.0 * log10(ed/3.7 + 2.51 * x / re) = 0
            for _ in 0..50 {
                let arg = ed_term + (2.51 * x) / re;
                if arg <= 0.0 {
                    return f64::NAN;
                }
                let gx = x + 2.0 * arg.log10();
                if gx.abs() < 1e-12 {
                    let f = 1.0 / (x * x);
                    return f;
                }

                // dg/dx = 1 + 2 * (2.51 / re) / (arg * ln(10))
                let dgx = 1.0 + (2.0 * 2.51 / (re * ln10 * arg));
                if dgx.abs() < 1e-20 {
                    return f64::NAN;
                }

                let x_next = x - gx / dgx;
                if (x_next - x).abs() < 1e-12 {
                    let f = 1.0 / (x_next * x_next);
                    return f;
                }
                x = x_next;
            }

            1.0 / (x * x)
        })
        .collect()
}

/// Swamee-Jain explicit friction factor:
/// f = 0.25 / (log10((epsilon / D) / 3.7 + 5.74 / (Re^0.9)))^2
pub fn swamee_jain_kernel(
    eps_over_d: &[f64],
    reynolds: &[f64],
) -> Vec<f64> {
    let n = eps_over_d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ed = eps_over_d[i];
            let re = reynolds[i];

            if ed < 0.0 || re <= 0.0 || ed.is_nan() || re.is_nan() {
                f64::NAN
            } else {
                let term = (ed / 3.7) + (5.74 / re.powf(0.9));
                let log_term = term.log10();
                0.25 / (log_term * log_term)
            }
        })
        .collect()
}

/// Haaland explicit friction factor:
/// 1 / sqrt(f) = -1.8 * log10(((epsilon / D) / 3.7)^1.11 + 6.9 / Re)
pub fn haaland_kernel(
    eps_over_d: &[f64],
    reynolds: &[f64],
) -> Vec<f64> {
    let n = eps_over_d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ed = eps_over_d[i];
            let re = reynolds[i];

            if ed < 0.0 || re <= 0.0 || ed.is_nan() || re.is_nan() {
                f64::NAN
            } else {
                let term = (ed / 3.7).powf(1.11) + (6.9 / re);
                let inv_sqrt_f = -1.8 * term.log10();
                if inv_sqrt_f <= 0.0 {
                    f64::NAN
                } else {
                    1.0 / (inv_sqrt_f * inv_sqrt_f)
                }
            }
        })
        .collect()
}

/// Churchill explicit friction factor (covers laminar, transition, turbulent):
/// f = 8 * ((8/Re)^12 + (A + B)^(-1.5))^(1/12)
/// A = (-2.457 * ln((7/Re)^0.9 + 0.27 * (eps/D)))^16
/// B = (37530 / Re)^16
pub fn churchill_kernel(
    eps_over_d: &[f64],
    reynolds: &[f64],
) -> Vec<f64> {
    let n = eps_over_d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ed = eps_over_d[i];
            let re = reynolds[i];

            if ed < 0.0 || re <= 0.0 || ed.is_nan() || re.is_nan() {
                f64::NAN
            } else {
                let theta1 = (8.0 / re).powi(12);
                let ln_arg = (7.0 / re).powf(0.9) + 0.27 * ed;
                if ln_arg <= 0.0 {
                    return f64::NAN;
                }
                let a = (-2.457 * ln_arg.ln()).powf(16.0);
                let b = (37530.0 / re).powf(16.0);
                let theta2 = (a + b).powf(-1.5);
                8.0 * (theta1 + theta2).powf(1.0 / 12.0)
            }
        })
        .collect()
}

/// Wood explicit friction factor approximation
pub fn wood_kernel(
    eps_over_d: &[f64],
    reynolds: &[f64],
) -> Vec<f64> {
    let n = eps_over_d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ed = eps_over_d[i];
            let re = reynolds[i];

            if ed < 0.0 || re <= 0.0 || ed.is_nan() || re.is_nan() {
                f64::NAN
            } else {
                let a = 0.094 * ed.powf(0.225) + 0.53 * ed;
                let b = 88.0 * ed.powf(0.44);
                let c = 1.62 * ed.powf(0.134);
                a + b * re.powf(-c)
            }
        })
        .collect()
}

/// Hazen-Williams head loss:
/// h_f = (k_hw * L * Q^1.852) / (C^1.852 * D^4.87)
/// k_hw = 10.67 (SI: Q m3/s, L m, D m, h_f m) or 4.727 (US: Q cfs, L ft, D ft, h_f ft)
pub fn hazen_williams_kernel(
    length: &[f64],
    discharge: &[f64],
    c_coeff: &[f64],
    diameter: &[f64],
    k_hw: f64,
) -> Vec<f64> {
    let n = length.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = length[i];
            let q = discharge[i];
            let c = c_coeff[i];
            let d = diameter[i];

            if l < 0.0 || q < 0.0 || c <= 0.0 || d <= 0.0 || l.is_nan() || q.is_nan() || c.is_nan() || d.is_nan() {
                f64::NAN
            } else {
                (k_hw * l * q.powf(1.852)) / (c.powf(1.852) * d.powf(4.87))
            }
        })
        .collect()
}

/// Hazen-Williams velocity: V = k_v * C * R_h^0.63 * S^0.54
/// k_v = 0.849 (SI) or 1.318 (US)
pub fn hazen_williams_velocity_kernel(
    c_coeff: &[f64],
    r_h: &[f64],
    slope: &[f64],
    k_v: f64,
) -> Vec<f64> {
    let n = c_coeff.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let c = c_coeff[i];
            let rh = r_h[i];
            let s = slope[i];

            if c <= 0.0 || rh < 0.0 || s < 0.0 || c.is_nan() || rh.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                k_v * c * rh.powf(0.63) * s.powf(0.54)
            }
        })
        .collect()
}

/// Minor head loss: h_m = K_L * V^2 / (2 * g)
pub fn minor_loss_kernel(
    k_l: &[f64],
    velocity: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = k_l.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let k = k_l[i];
            let v = velocity[i];

            if k < 0.0 || v < 0.0 || g <= 0.0 || k.is_nan() || v.is_nan() {
                f64::NAN
            } else {
                k * (v * v) / (2.0 * g)
            }
        })
        .collect()
}

/// Water hammer wave celerity: a = sqrt((K / rho) / (1 + (K / E) * (D / e)))
pub fn wave_celerity_kernel(
    bulk_modulus: &[f64],
    density: &[f64],
    elastic_modulus: &[f64],
    diameter: &[f64],
    wall_thickness: &[f64],
) -> Vec<f64> {
    let n = bulk_modulus.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let k = bulk_modulus[i];
            let rho = density[i];
            let e = elastic_modulus[i];
            let d = diameter[i];
            let t = wall_thickness[i];

            if k <= 0.0 || rho <= 0.0 || e <= 0.0 || d <= 0.0 || t <= 0.0
                || k.is_nan() || rho.is_nan() || e.is_nan() || d.is_nan() || t.is_nan() {
                f64::NAN
            } else {
                let den = 1.0 + (k / e) * (d / t);
                ((k / rho) / den).sqrt()
            }
        })
        .collect()
}

/// Joukowsky maximum pressure head rise: Delta_H = (a * Delta_V) / g
pub fn joukowsky_kernel(
    celerity: &[f64],
    delta_v: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = celerity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let a = celerity[i];
            let dv = delta_v[i];

            if a <= 0.0 || dv < 0.0 || g <= 0.0 || a.is_nan() || dv.is_nan() {
                f64::NAN
            } else {
                (a * dv) / g
            }
        })
        .collect()
}

/// Critical valve closure time: T_c = 2 * L / a
pub fn critical_closure_time_kernel(
    length: &[f64],
    celerity: &[f64],
) -> Vec<f64> {
    let n = length.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = length[i];
            let a = celerity[i];

            if l < 0.0 || a <= 0.0 || l.is_nan() || a.is_nan() {
                f64::NAN
            } else {
                (2.0 * l) / a
            }
        })
        .collect()
}

// ============================================================================
// EXPANSION FORMULAS: CULVERTS, PIPE NETWORKS & PUMP POWER
// ============================================================================

/// Culvert inlet control - unsubmerged flow:
/// HW_d = (H_c / D) + K * (Q / (A * sqrt(D)))^M - 0.5 * S
pub fn culvert_inlet_unsubmerged_kernel(
    q: &[f64],
    d: &[f64],
    a: &[f64],
    h_c: &[f64],
    s: &[f64],
    k_coeff: &[f64],
    m_exp: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_v = q[i];
            let d_v = d[i];
            let a_v = a[i];
            let hc_v = h_c[i];
            let s_v = s[i];
            let k_v = k_coeff[i];
            let m_v = m_exp[i];

            if q_v < 0.0 || d_v <= 0.0 || a_v <= 0.0 || hc_v < 0.0 || s_v < 0.0 || k_v <= 0.0
                || q_v.is_nan() || d_v.is_nan() || a_v.is_nan() || hc_v.is_nan() || s_v.is_nan() || k_v.is_nan() || m_v.is_nan() {
                f64::NAN
            } else {
                let f_flow = q_v / (a_v * d_v.sqrt());
                (hc_v / d_v) + k_v * f_flow.powf(m_v) - 0.5 * s_v
            }
        })
        .collect()
}

/// Culvert inlet control - submerged flow:
/// HW_d = c * (Q / (A * sqrt(D)))^2 + Y - 0.5 * S
pub fn culvert_inlet_submerged_kernel(
    q: &[f64],
    d: &[f64],
    a: &[f64],
    s: &[f64],
    c_coeff: &[f64],
    y_const: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_v = q[i];
            let d_v = d[i];
            let a_v = a[i];
            let s_v = s[i];
            let c_v = c_coeff[i];
            let y_v = y_const[i];

            if q_v < 0.0 || d_v <= 0.0 || a_v <= 0.0 || s_v < 0.0 || c_v <= 0.0
                || q_v.is_nan() || d_v.is_nan() || a_v.is_nan() || s_v.is_nan() || c_v.is_nan() || y_v.is_nan() {
                f64::NAN
            } else {
                let f_flow = q_v / (a_v * d_v.sqrt());
                c_v * f_flow * f_flow + y_v - 0.5 * s_v
            }
        })
        .collect()
}

/// Culvert outlet control headwater elevation:
/// HW_o = h_o + H - L * S_0
pub fn culvert_outlet_control_head_kernel(
    h_o: &[f64],
    h_losses: &[f64],
    length: &[f64],
    slope: &[f64],
) -> Vec<f64> {
    let n = h_o.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ho = h_o[i];
            let h = h_losses[i];
            let l = length[i];
            let s0 = slope[i];

            if ho.is_nan() || h.is_nan() || l.is_nan() || s0.is_nan() || l < 0.0 || s0 < 0.0 {
                f64::NAN
            } else {
                ho + h - l * s0
            }
        })
        .collect()
}

/// Culvert entrance minor loss: h_e = K_e * V^2 / (2 * g)
pub fn culvert_entrance_loss_kernel(
    k_e: &[f64],
    velocity: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = k_e.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ke = k_e[i];
            let v = velocity[i];
            if ke < 0.0 || v < 0.0 || g <= 0.0 || ke.is_nan() || v.is_nan() {
                f64::NAN
            } else {
                ke * (v * v) / (2.0 * g)
            }
        })
        .collect()
}

/// Hardy Cross flow loop correction:
/// delta_Q = - sum_hf / (n_exp * sum_dhf_dq)
pub fn hardy_cross_correction_kernel(
    sum_hf: &[f64],
    sum_dhf_dq: &[f64],
    n_exp: &[f64],
) -> Vec<f64> {
    let n = sum_hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let shf = sum_hf[i];
            let sdhf = sum_dhf_dq[i];
            let n_val = n_exp[i];

            if shf.is_nan() || sdhf.is_nan() || n_val.is_nan() || sdhf.abs() < 1e-12 || n_val <= 0.0 {
                f64::NAN
            } else {
                -shf / (n_val * sdhf)
            }
        })
        .collect()
}

/// Equivalent pipe length for minor loss: L_e = (K_L * D) / f
pub fn equivalent_pipe_length_kernel(
    k_l: &[f64],
    diameter: &[f64],
    f: &[f64],
) -> Vec<f64> {
    let n = k_l.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let kl = k_l[i];
            let d = diameter[i];
            let f_val = f[i];

            if kl < 0.0 || d <= 0.0 || f_val <= 0.0 || kl.is_nan() || d.is_nan() || f_val.is_nan() {
                f64::NAN
            } else {
                (kl * d) / f_val
            }
        })
        .collect()
}

/// Equivalent diameter for pipes in series: D_e = (L_total / sum_l_d5)^(1/5)
pub fn equivalent_diameter_series_kernel(
    l_total: &[f64],
    sum_l_d5: &[f64],
) -> Vec<f64> {
    let n = l_total.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let lt = l_total[i];
            let sld = sum_l_d5[i];

            if lt <= 0.0 || sld <= 0.0 || lt.is_nan() || sld.is_nan() {
                f64::NAN
            } else {
                (lt / sld).powf(0.2)
            }
        })
        .collect()
}

/// Parallel pipe flow distribution: Q_i = Q_total * (k_i / sum_k)
pub fn parallel_pipes_distribution_kernel(
    q_total: &[f64],
    k_i: &[f64],
    sum_k: &[f64],
) -> Vec<f64> {
    let n = q_total.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let qt = q_total[i];
            let ki = k_i[i];
            let sk = sum_k[i];

            if qt < 0.0 || ki < 0.0 || sk <= 0.0 || qt.is_nan() || ki.is_nan() || sk.is_nan() {
                f64::NAN
            } else {
                qt * (ki / sk)
            }
        })
        .collect()
}

/// Water power (hydraulic power):
/// SI: P_w = (gamma * Q * H) / 1000.0 (kW)
/// US: P_w = (gamma * Q * H) / 550.0 (hp)
pub fn water_power_kernel(
    discharge: &[f64],
    head: &[f64],
    gamma: &[f64],
    divisor: f64,
) -> Vec<f64> {
    let n = discharge.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q = discharge[i];
            let h = head[i];
            let gam = gamma[i];

            if q < 0.0 || h < 0.0 || gam <= 0.0 || divisor <= 0.0 || q.is_nan() || h.is_nan() || gam.is_nan() {
                f64::NAN
            } else {
                (gam * q * h) / divisor
            }
        })
        .collect()
}

/// Pump brake power: P_b = P_w / eta
pub fn pump_brake_power_kernel(
    p_w: &[f64],
    eta: &[f64],
) -> Vec<f64> {
    let n = p_w.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let pw = p_w[i];
            let e = eta[i];

            if pw < 0.0 || e <= 0.0 || e > 1.0 || pw.is_nan() || e.is_nan() {
                f64::NAN
            } else {
                pw / e
            }
        })
        .collect()
}

// ============================================================================
// DEDICATED BIDIRECTIONAL ALGEBRAIC INVERSIONS (APPROACH 1)
// ============================================================================

/// Inversion: Darcy-Weisbach friction factor f = (2 * g * D * h_f) / (L * V^2)
pub fn darcy_weisbach_f_kernel(
    hf: &[f64],
    length: &[f64],
    diameter: &[f64],
    velocity: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let l_val = length[i];
            let d_val = diameter[i];
            let v_val = velocity[i];
            if h_val < 0.0 || l_val <= 0.0 || d_val <= 0.0 || v_val <= 0.0 || g <= 0.0
                || h_val.is_nan() || l_val.is_nan() || d_val.is_nan() || v_val.is_nan() {
                f64::NAN
            } else {
                (2.0 * g * d_val * h_val) / (l_val * v_val * v_val)
            }
        })
        .collect()
}

/// Inversion: Darcy-Weisbach diameter D = f * (L / h_f) * (V^2 / (2 * g))
pub fn darcy_weisbach_d_kernel(
    hf: &[f64],
    f: &[f64],
    length: &[f64],
    velocity: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let f_val = f[i];
            let l_val = length[i];
            let v_val = velocity[i];
            if h_val <= 0.0 || f_val <= 0.0 || l_val <= 0.0 || v_val < 0.0 || g <= 0.0
                || h_val.is_nan() || f_val.is_nan() || l_val.is_nan() || v_val.is_nan() {
                f64::NAN
            } else {
                f_val * (l_val / h_val) * (v_val * v_val / (2.0 * g))
            }
        })
        .collect()
}

/// Inversion: Darcy-Weisbach length L = (2 * g * D * h_f) / (f * V^2)
pub fn darcy_weisbach_l_kernel(
    hf: &[f64],
    f: &[f64],
    diameter: &[f64],
    velocity: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let f_val = f[i];
            let d_val = diameter[i];
            let v_val = velocity[i];
            if h_val < 0.0 || f_val <= 0.0 || d_val <= 0.0 || v_val <= 0.0 || g <= 0.0
                || h_val.is_nan() || f_val.is_nan() || d_val.is_nan() || v_val.is_nan() {
                f64::NAN
            } else {
                (2.0 * g * d_val * h_val) / (f_val * v_val * v_val)
            }
        })
        .collect()
}

/// Inversion: Darcy-Weisbach velocity V = sqrt((2 * g * D * h_f) / (f * L))
pub fn darcy_weisbach_v_kernel(
    hf: &[f64],
    f: &[f64],
    length: &[f64],
    diameter: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let f_val = f[i];
            let l_val = length[i];
            let d_val = diameter[i];
            if h_val < 0.0 || f_val <= 0.0 || l_val <= 0.0 || d_val <= 0.0 || g <= 0.0
                || h_val.is_nan() || f_val.is_nan() || l_val.is_nan() || d_val.is_nan() {
                f64::NAN
            } else {
                ((2.0 * g * d_val * h_val) / (f_val * l_val)).sqrt()
            }
        })
        .collect()
}

/// Inversion: Darcy-Weisbach discharge Q = (pi * D^2 / 4) * sqrt((2 * g * D * h_f) / (f * L))
pub fn darcy_weisbach_q_kernel(
    hf: &[f64],
    f: &[f64],
    length: &[f64],
    diameter: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let f_val = f[i];
            let l_val = length[i];
            let d_val = diameter[i];
            if h_val < 0.0 || f_val <= 0.0 || l_val <= 0.0 || d_val <= 0.0 || g <= 0.0
                || h_val.is_nan() || f_val.is_nan() || l_val.is_nan() || d_val.is_nan() {
                f64::NAN
            } else {
                let v = ((2.0 * g * d_val * h_val) / (f_val * l_val)).sqrt();
                let area = 0.25 * PI * d_val * d_val;
                area * v
            }
        })
        .collect()
}

/// Inversion: Hazen-Williams discharge Q = ((h_f * C^1.852 * D^4.87) / (k_L * L))^(1 / 1.852)
pub fn hazen_williams_q_kernel(
    hf: &[f64],
    c: &[f64],
    diameter: &[f64],
    length: &[f64],
    k_l: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let c_val = c[i];
            let d_val = diameter[i];
            let l_val = length[i];
            if h_val < 0.0 || c_val <= 0.0 || d_val <= 0.0 || l_val <= 0.0 || k_l <= 0.0
                || h_val.is_nan() || c_val.is_nan() || d_val.is_nan() || l_val.is_nan() {
                f64::NAN
            } else {
                let num = h_val * c_val.powf(1.852) * d_val.powf(4.87);
                let denom = k_l * l_val;
                (num / denom).powf(1.0 / 1.852)
            }
        })
        .collect()
}

/// Inversion: Hazen-Williams diameter D = ((k_L * L * Q^1.852) / (h_f * C^1.852))^(1 / 4.87)
pub fn hazen_williams_d_kernel(
    hf: &[f64],
    q: &[f64],
    c: &[f64],
    length: &[f64],
    k_l: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let q_val = q[i];
            let c_val = c[i];
            let l_val = length[i];
            if h_val <= 0.0 || q_val <= 0.0 || c_val <= 0.0 || l_val <= 0.0 || k_l <= 0.0
                || h_val.is_nan() || q_val.is_nan() || c_val.is_nan() || l_val.is_nan() {
                f64::NAN
            } else {
                let num = k_l * l_val * q_val.powf(1.852);
                let denom = h_val * c_val.powf(1.852);
                (num / denom).powf(1.0 / 4.87)
            }
        })
        .collect()
}

/// Inversion: Hazen-Williams length L = (h_f * C^1.852 * D^4.87) / (k_L * Q^1.852)
pub fn hazen_williams_l_kernel(
    hf: &[f64],
    q: &[f64],
    c: &[f64],
    diameter: &[f64],
    k_l: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let q_val = q[i];
            let c_val = c[i];
            let d_val = diameter[i];
            if h_val < 0.0 || q_val <= 0.0 || c_val <= 0.0 || d_val <= 0.0 || k_l <= 0.0
                || h_val.is_nan() || q_val.is_nan() || c_val.is_nan() || d_val.is_nan() {
                f64::NAN
            } else {
                let num = h_val * c_val.powf(1.852) * d_val.powf(4.87);
                let denom = k_l * q_val.powf(1.852);
                num / denom
            }
        })
        .collect()
}

/// Inversion: Hazen-Williams roughness C = ((k_L * L * Q^1.852) / (h_f * D^4.87))^(1 / 1.852)
pub fn hazen_williams_c_kernel(
    hf: &[f64],
    q: &[f64],
    diameter: &[f64],
    length: &[f64],
    k_l: f64,
) -> Vec<f64> {
    let n = hf.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h_val = hf[i];
            let q_val = q[i];
            let d_val = diameter[i];
            let l_val = length[i];
            if h_val <= 0.0 || q_val <= 0.0 || d_val <= 0.0 || l_val <= 0.0 || k_l <= 0.0
                || h_val.is_nan() || q_val.is_nan() || d_val.is_nan() || l_val.is_nan() {
                f64::NAN
            } else {
                let num = k_l * l_val * q_val.powf(1.852);
                let denom = h_val * d_val.powf(4.87);
                (num / denom).powf(1.0 / 1.852)
            }
        })
        .collect()
}

/// Inversion: Hazen-Williams slope S = (V / (k_v * C * R_h^0.63))^(1 / 0.54)
pub fn hazen_williams_s_kernel(
    velocity: &[f64],
    c: &[f64],
    r_h: &[f64],
    k_v: f64,
) -> Vec<f64> {
    let n = velocity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v = velocity[i];
            let c_val = c[i];
            let rh = r_h[i];
            if v < 0.0 || c_val <= 0.0 || rh <= 0.0 || k_v <= 0.0
                || v.is_nan() || c_val.is_nan() || rh.is_nan() {
                f64::NAN
            } else {
                let ratio = v / (k_v * c_val * rh.powf(0.63));
                ratio.powf(1.0 / 0.54)
            }
        })
        .collect()
}

/// Inversion: Reynolds velocity V = (Re * nu) / D
pub fn reynolds_v_kernel(
    re: &[f64],
    diameter: &[f64],
    kinematic_viscosity: &[f64],
) -> Vec<f64> {
    let n = re.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let r = re[i];
            let d = diameter[i];
            let nu = kinematic_viscosity[i];
            if r < 0.0 || d <= 0.0 || nu <= 0.0 || r.is_nan() || d.is_nan() || nu.is_nan() {
                f64::NAN
            } else {
                (r * nu) / d
            }
        })
        .collect()
}

/// Inversion: Reynolds diameter D = (Re * nu) / V
pub fn reynolds_d_kernel(
    re: &[f64],
    velocity: &[f64],
    kinematic_viscosity: &[f64],
) -> Vec<f64> {
    let n = re.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let r = re[i];
            let v = velocity[i];
            let nu = kinematic_viscosity[i];
            if r < 0.0 || v <= 0.0 || nu <= 0.0 || r.is_nan() || v.is_nan() || nu.is_nan() {
                f64::NAN
            } else {
                (r * nu) / v
            }
        })
        .collect()
}

/// Inversion: Minor loss coefficient K_L = (2 * g * h_m) / V^2
pub fn minor_loss_kl_kernel(
    hm: &[f64],
    velocity: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = hm.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h = hm[i];
            let v = velocity[i];
            if h < 0.0 || v <= 0.0 || g <= 0.0 || h.is_nan() || v.is_nan() {
                f64::NAN
            } else {
                (2.0 * g * h) / (v * v)
            }
        })
        .collect()
}

/// Inversion: Minor loss velocity V = sqrt((2 * g * h_m) / K_L)
pub fn minor_loss_v_kernel(
    hm: &[f64],
    kl: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = hm.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let h = hm[i];
            let k = kl[i];
            if h < 0.0 || k <= 0.0 || g <= 0.0 || h.is_nan() || k.is_nan() {
                f64::NAN
            } else {
                ((2.0 * g * h) / k).sqrt()
            }
        })
        .collect()
}

/// Inversion: Joukowsky velocity change delta_V = delta_P / (rho * a)
pub fn joukowsky_dv_kernel(
    dp: &[f64],
    a: &[f64],
    rho: &[f64],
) -> Vec<f64> {
    let n = dp.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = dp[i];
            let a_val = a[i];
            let r = rho[i];
            if p < 0.0 || a_val <= 0.0 || r <= 0.0 || p.is_nan() || a_val.is_nan() || r.is_nan() {
                f64::NAN
            } else {
                p / (r * a_val)
            }
        })
        .collect()
}

/// Inversion: Joukowsky wave celerity a = delta_P / (rho * delta_V)
pub fn joukowsky_a_kernel(
    dp: &[f64],
    dv: &[f64],
    rho: &[f64],
) -> Vec<f64> {
    let n = dp.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = dp[i];
            let v = dv[i];
            let r = rho[i];
            if p < 0.0 || v <= 0.0 || r <= 0.0 || p.is_nan() || v.is_nan() || r.is_nan() {
                f64::NAN
            } else {
                p / (r * v)
            }
        })
        .collect()
}

/// Inversion: Critical closure pipe length L = (T_c * a) / 2
pub fn critical_closure_l_kernel(
    tc: &[f64],
    a: &[f64],
) -> Vec<f64> {
    let n = tc.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = tc[i];
            let a_val = a[i];
            if t < 0.0 || a_val <= 0.0 || t.is_nan() || a_val.is_nan() {
                f64::NAN
            } else {
                (t * a_val) / 2.0
            }
        })
        .collect()
}

/// Inversion: Critical closure wave celerity a = (2 * L) / T_c
pub fn critical_closure_a_kernel(
    tc: &[f64],
    length: &[f64],
) -> Vec<f64> {
    let n = tc.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = tc[i];
            let l = length[i];
            if t <= 0.0 || l < 0.0 || t.is_nan() || l.is_nan() {
                f64::NAN
            } else {
                (2.0 * l) / t
            }
        })
        .collect()
}

/// Inversion: Equivalent pipe loss coefficient K_L = (f * L_e) / D
pub fn equivalent_pipe_kl_kernel(
    le: &[f64],
    diameter: &[f64],
    f: &[f64],
) -> Vec<f64> {
    let n = le.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = le[i];
            let d = diameter[i];
            let f_val = f[i];
            if l < 0.0 || d <= 0.0 || f_val <= 0.0 || l.is_nan() || d.is_nan() || f_val.is_nan() {
                f64::NAN
            } else {
                (f_val * l) / d
            }
        })
        .collect()
}

/// Inversion: Equivalent pipe friction factor f = (K_L * D) / L_e
pub fn equivalent_pipe_f_kernel(
    le: &[f64],
    kl: &[f64],
    diameter: &[f64],
) -> Vec<f64> {
    let n = le.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = le[i];
            let k = kl[i];
            let d = diameter[i];
            if l <= 0.0 || k < 0.0 || d <= 0.0 || l.is_nan() || k.is_nan() || d.is_nan() {
                f64::NAN
            } else {
                (k * d) / l
            }
        })
        .collect()
}

/// Inversion: Water power discharge Q = (P_w * divisor) / (gamma * H)
pub fn water_power_q_kernel(
    pw: &[f64],
    head: &[f64],
    gamma: &[f64],
    divisor: f64,
) -> Vec<f64> {
    let n = pw.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = pw[i];
            let h = head[i];
            let gam = gamma[i];
            if p < 0.0 || h <= 0.0 || gam <= 0.0 || divisor <= 0.0
                || p.is_nan() || h.is_nan() || gam.is_nan() {
                f64::NAN
            } else {
                (p * divisor) / (gam * h)
            }
        })
        .collect()
}

/// Inversion: Water power head H = (P_w * divisor) / (gamma * Q)
pub fn water_power_h_kernel(
    pw: &[f64],
    q: &[f64],
    gamma: &[f64],
    divisor: f64,
) -> Vec<f64> {
    let n = pw.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = pw[i];
            let q_val = q[i];
            let gam = gamma[i];
            if p < 0.0 || q_val <= 0.0 || gam <= 0.0 || divisor <= 0.0
                || p.is_nan() || q_val.is_nan() || gam.is_nan() {
                f64::NAN
            } else {
                (p * divisor) / (gam * q_val)
            }
        })
        .collect()
}

/// Inversion: Pump water power P_w = P_b * eta
pub fn pump_power_pw_kernel(
    pb: &[f64],
    eta: &[f64],
) -> Vec<f64> {
    let n = pb.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = pb[i];
            let e = eta[i];
            if p < 0.0 || e <= 0.0 || e > 1.0 || p.is_nan() || e.is_nan() {
                f64::NAN
            } else {
                p * e
            }
        })
        .collect()
}

/// Inversion: Pump efficiency eta = P_w / P_b
pub fn pump_power_eta_kernel(
    pw: &[f64],
    pb: &[f64],
) -> Vec<f64> {
    let n = pw.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let w = pw[i];
            let b = pb[i];
            if w < 0.0 || b <= 0.0 || w > b || w.is_nan() || b.is_nan() {
                f64::NAN
            } else {
                w / b
            }
        })
        .collect()
}

