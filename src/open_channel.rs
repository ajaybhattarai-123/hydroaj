//! Open Channel Hydraulics Module
//! High-performance Rayon-parallelized computations for uniform flow,
//! channel geometry, energy/momentum, hydraulic jumps, and non-uniform flow.

use rayon::prelude::*;
use std::f64::consts::PI;

/// Manning discharge: Q = (k / n) * A * R_h^(2/3) * S_0^(1/2)
pub fn manning_discharge_kernel(
    area: &[f64],
    r_h: &[f64],
    slope: &[f64],
    roughness: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = area.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let a = area[i];
            let rh = r_h[i];
            let s = slope[i];
            let n_val = roughness[i];

            if a < 0.0 || rh < 0.0 || s < 0.0 || n_val <= 0.0 || a.is_nan() || rh.is_nan() || s.is_nan() || n_val.is_nan() {
                f64::NAN
            } else {
                (k / n_val) * a * rh.powf(2.0 / 3.0) * s.sqrt()
            }
        })
        .collect()
}

/// Manning velocity: V = (k / n) * R_h^(2/3) * S_0^(1/2)
pub fn manning_velocity_kernel(
    r_h: &[f64],
    slope: &[f64],
    roughness: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = r_h.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let rh = r_h[i];
            let s = slope[i];
            let n_val = roughness[i];

            if rh < 0.0 || s < 0.0 || n_val <= 0.0 || rh.is_nan() || s.is_nan() || n_val.is_nan() {
                f64::NAN
            } else {
                (k / n_val) * rh.powf(2.0 / 3.0) * s.sqrt()
            }
        })
        .collect()
}

/// Strickler velocity: V = k_st * R_h^(2/3) * S_0^(1/2)
pub fn strickler_velocity_kernel(
    r_h: &[f64],
    slope: &[f64],
    k_st: &[f64],
) -> Vec<f64> {
    let n = r_h.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let rh = r_h[i];
            let s = slope[i];
            let k_val = k_st[i];

            if rh < 0.0 || s < 0.0 || k_val <= 0.0 || rh.is_nan() || s.is_nan() || k_val.is_nan() {
                f64::NAN
            } else {
                k_val * rh.powf(2.0 / 3.0) * s.sqrt()
            }
        })
        .collect()
}

/// Chézy velocity: V = C * sqrt(R_h * S_0)
pub fn chezy_velocity_kernel(
    c: &[f64],
    r_h: &[f64],
    slope: &[f64],
) -> Vec<f64> {
    let n = c.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let c_val = c[i];
            let rh = r_h[i];
            let s = slope[i];

            if c_val < 0.0 || rh < 0.0 || s < 0.0 || c_val.is_nan() || rh.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                c_val * (rh * s).sqrt()
            }
        })
        .collect()
}

/// Kutter's formula for Chézy C:
/// C = (23.0 + 0.00155/S_0 + 1.0/n) / (1.0 + (23.0 + 0.00155/S_0) * (n / sqrt(R_h)))
pub fn kutter_chezy_c_kernel(
    r_h: &[f64],
    slope: &[f64],
    roughness: &[f64],
) -> Vec<f64> {
    let n_len = r_h.len();
    (0..n_len)
        .into_par_iter()
        .map(|i| {
            let rh = r_h[i];
            let s = slope[i];
            let n_val = roughness[i];

            if rh <= 0.0 || s <= 0.0 || n_val <= 0.0 || rh.is_nan() || s.is_nan() || n_val.is_nan() {
                f64::NAN
            } else {
                let term = 23.0 + 0.00155 / s;
                let num = term + 1.0 / n_val;
                let den = 1.0 + term * (n_val / rh.sqrt());
                if den.abs() < 1e-15 {
                    f64::NAN
                } else {
                    num / den
                }
            }
        })
        .collect()
}

/// Bazin's formula for Chézy C: C = 87.0 / (1.0 + gamma / sqrt(R_h))
pub fn bazin_chezy_c_kernel(
    r_h: &[f64],
    gamma: &[f64],
) -> Vec<f64> {
    let n = r_h.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let rh = r_h[i];
            let g = gamma[i];

            if rh <= 0.0 || g < 0.0 || rh.is_nan() || g.is_nan() {
                f64::NAN
            } else {
                let den = 1.0 + g / rh.sqrt();
                if den.abs() < 1e-15 {
                    f64::NAN
                } else {
                    87.0 / den
                }
            }
        })
        .collect()
}

/// Rectangular channel geometry: (A, P, R_h, T, D_h, y_bar)
pub fn geom_rectangular_kernel(
    b: &[f64],
    y: &[f64],
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = b.len();
    let mut area = vec![0.0; n];
    let mut perim = vec![0.0; n];
    let mut rh = vec![0.0; n];
    let mut top_w = vec![0.0; n];
    let mut hyd_d = vec![0.0; n];
    let mut y_b = vec![0.0; n];

    (0..n)
        .into_par_iter()
        .map(|i| {
            let b_val = b[i];
            let y_val = y[i];
            if b_val <= 0.0 || y_val < 0.0 || b_val.is_nan() || y_val.is_nan() {
                (f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN)
            } else {
                let a = b_val * y_val;
                let p = b_val + 2.0 * y_val;
                let r = if p > 0.0 { a / p } else { 0.0 };
                let t = b_val;
                let d = y_val;
                let yb = y_val / 2.0;
                (a, p, r, t, d, yb)
            }
        })
        .collect::<Vec<_>>()
        .into_iter()
        .enumerate()
        .for_each(|(i, (a, p, r, t, d, yb))| {
            area[i] = a;
            perim[i] = p;
            rh[i] = r;
            top_w[i] = t;
            hyd_d[i] = d;
            y_b[i] = yb;
        });

    (area, perim, rh, top_w, hyd_d, y_b)
}

/// Trapezoidal channel geometry: (A, P, R_h, T, D_h, y_bar)
pub fn geom_trapezoidal_kernel(
    b: &[f64],
    m: &[f64],
    y: &[f64],
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = b.len();
    let mut area = vec![0.0; n];
    let mut perim = vec![0.0; n];
    let mut rh = vec![0.0; n];
    let mut top_w = vec![0.0; n];
    let mut hyd_d = vec![0.0; n];
    let mut y_b = vec![0.0; n];

    (0..n)
        .into_par_iter()
        .map(|i| {
            let b_val = b[i];
            let m_val = m[i];
            let y_val = y[i];
            if b_val < 0.0 || m_val < 0.0 || y_val < 0.0 || (b_val == 0.0 && m_val == 0.0) || b_val.is_nan() || m_val.is_nan() || y_val.is_nan() {
                (f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN)
            } else {
                let a = (b_val + m_val * y_val) * y_val;
                let p = b_val + 2.0 * y_val * (1.0 + m_val * m_val).sqrt();
                let r = if p > 0.0 { a / p } else { 0.0 };
                let t = b_val + 2.0 * m_val * y_val;
                let d = if t > 0.0 { a / t } else { 0.0 };
                let yb = if (b_val + m_val * y_val) > 0.0 {
                    y_val * (2.0 * b_val + m_val * y_val) / (3.0 * (b_val + m_val * y_val))
                } else {
                    0.0
                };
                (a, p, r, t, d, yb)
            }
        })
        .collect::<Vec<_>>()
        .into_iter()
        .enumerate()
        .for_each(|(i, (a, p, r, t, d, yb))| {
            area[i] = a;
            perim[i] = p;
            rh[i] = r;
            top_w[i] = t;
            hyd_d[i] = d;
            y_b[i] = yb;
        });

    (area, perim, rh, top_w, hyd_d, y_b)
}

/// Triangular channel geometry: (A, P, R_h, T, D_h, y_bar)
pub fn geom_triangular_kernel(
    m: &[f64],
    y: &[f64],
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = m.len();
    let mut area = vec![0.0; n];
    let mut perim = vec![0.0; n];
    let mut rh = vec![0.0; n];
    let mut top_w = vec![0.0; n];
    let mut hyd_d = vec![0.0; n];
    let mut y_b = vec![0.0; n];

    (0..n)
        .into_par_iter()
        .map(|i| {
            let m_val = m[i];
            let y_val = y[i];
            if m_val <= 0.0 || y_val < 0.0 || m_val.is_nan() || y_val.is_nan() {
                (f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN)
            } else {
                let a = m_val * y_val * y_val;
                let p = 2.0 * y_val * (1.0 + m_val * m_val).sqrt();
                let r = if p > 0.0 { a / p } else { 0.0 };
                let t = 2.0 * m_val * y_val;
                let d = y_val / 2.0;
                let yb = y_val / 3.0;
                (a, p, r, t, d, yb)
            }
        })
        .collect::<Vec<_>>()
        .into_iter()
        .enumerate()
        .for_each(|(i, (a, p, r, t, d, yb))| {
            area[i] = a;
            perim[i] = p;
            rh[i] = r;
            top_w[i] = t;
            hyd_d[i] = d;
            y_b[i] = yb;
        });

    (area, perim, rh, top_w, hyd_d, y_b)
}

/// Circular channel geometry: (A, P, R_h, T, D_h)
pub fn geom_circular_kernel(
    d: &[f64],
    y: &[f64],
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = d.len();
    let mut area = vec![0.0; n];
    let mut perim = vec![0.0; n];
    let mut rh = vec![0.0; n];
    let mut top_w = vec![0.0; n];
    let mut hyd_d = vec![0.0; n];

    (0..n)
        .into_par_iter()
        .map(|i| {
            let diam = d[i];
            let depth = y[i];
            if diam <= 0.0 || depth < 0.0 || depth > diam || diam.is_nan() || depth.is_nan() {
                (f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN)
            } else if depth == 0.0 {
                (0.0, 0.0, 0.0, 0.0, 0.0)
            } else if (depth - diam).abs() < 1e-12 {
                let a = PI * diam * diam / 4.0;
                let p = PI * diam;
                (a, p, diam / 4.0, 0.0, f64::INFINITY)
            } else {
                let cos_val = (1.0 - 2.0 * depth / diam).clamp(-1.0, 1.0);
                let theta = 2.0 * cos_val.acos();
                let a = (diam * diam / 8.0) * (theta - theta.sin());
                let p = diam * theta / 2.0;
                let r = if p > 0.0 { a / p } else { 0.0 };
                let t = diam * (theta / 2.0).sin();
                let hyd = if t > 0.0 { a / t } else { 0.0 };
                (a, p, r, t, hyd)
            }
        })
        .collect::<Vec<_>>()
        .into_iter()
        .enumerate()
        .for_each(|(i, (a, p, r, t, hyd))| {
            area[i] = a;
            perim[i] = p;
            rh[i] = r;
            top_w[i] = t;
            hyd_d[i] = hyd;
        });

    (area, perim, rh, top_w, hyd_d)
}

/// Parabolic channel geometry: (A, P, R_h, D_h, y_bar)
pub fn geom_parabolic_kernel(
    t: &[f64],
    y: &[f64],
) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = t.len();
    let mut area = vec![0.0; n];
    let mut perim = vec![0.0; n];
    let mut rh = vec![0.0; n];
    let mut hyd_d = vec![0.0; n];
    let mut y_b = vec![0.0; n];

    (0..n)
        .into_par_iter()
        .map(|i| {
            let t_val = t[i];
            let y_val = y[i];
            if t_val <= 0.0 || y_val < 0.0 || t_val.is_nan() || y_val.is_nan() {
                (f64::NAN, f64::NAN, f64::NAN, f64::NAN, f64::NAN)
            } else {
                let a = (2.0 / 3.0) * t_val * y_val;
                let p = t_val + (8.0 / 3.0) * (y_val * y_val / t_val);
                let r = if p > 0.0 { a / p } else { 0.0 };
                let d = (2.0 / 3.0) * y_val;
                let yb = (2.0 / 5.0) * y_val;
                (a, p, r, d, yb)
            }
        })
        .collect::<Vec<_>>()
        .into_iter()
        .enumerate()
        .for_each(|(i, (a, p, r, d, yb))| {
            area[i] = a;
            perim[i] = p;
            rh[i] = r;
            hyd_d[i] = d;
            y_b[i] = yb;
        });

    (area, perim, rh, hyd_d, y_b)
}

/// Specific Energy: E = y + Q^2 / (2 * g * A^2)
pub fn specific_energy_kernel(
    y: &[f64],
    q: &[f64],
    area: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = y.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y_val = y[i];
            let q_val = q[i];
            let a = area[i];

            if y_val < 0.0 || q_val < 0.0 || a <= 0.0 || g <= 0.0 || y_val.is_nan() || q_val.is_nan() || a.is_nan() {
                f64::NAN
            } else {
                y_val + (q_val * q_val) / (2.0 * g * a * a)
            }
        })
        .collect()
}

/// Froude Number: Fr = (Q / A) / sqrt(g * (A / T))
pub fn froude_number_kernel(
    q: &[f64],
    area: &[f64],
    top_w: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let a = area[i];
            let t = top_w[i];

            if q_val < 0.0 || a <= 0.0 || t <= 0.0 || g <= 0.0 || q_val.is_nan() || a.is_nan() || t.is_nan() {
                f64::NAN
            } else {
                let v = q_val / a;
                let d_h = a / t;
                v / (g * d_h).sqrt()
            }
        })
        .collect()
}

/// Specific Force (Momentum): M = Q^2 / (g * A) + y_bar * A
pub fn specific_force_kernel(
    q: &[f64],
    area: &[f64],
    y_bar: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let a = area[i];
            let yb = y_bar[i];

            if q_val < 0.0 || a <= 0.0 || yb < 0.0 || g <= 0.0 || q_val.is_nan() || a.is_nan() || yb.is_nan() {
                f64::NAN
            } else {
                (q_val * q_val) / (g * a) + yb * a
            }
        })
        .collect()
}

/// Critical depth for rectangular channel: y_c = (q^2 / g)^(1/3)
pub fn critical_depth_rectangular_kernel(
    unit_q: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = unit_q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q = unit_q[i];
            if q < 0.0 || g <= 0.0 || q.is_nan() {
                f64::NAN
            } else {
                (q * q / g).cbrt()
            }
        })
        .collect()
}

/// Normal depth for trapezoidal channel using parallel Newton-Raphson:
/// f(y) = (k/n) * A(y) * R_h(y)^(2/3) * S_0^(1/2) - Q = 0
pub fn normal_depth_trapezoidal_kernel(
    q: &[f64],
    b: &[f64],
    m: &[f64],
    s0: &[f64],
    roughness: &[f64],
    k: f64,
) -> Vec<f64> {
    let n_len = q.len();
    (0..n_len)
        .into_par_iter()
        .map(|i| {
            let q_target = q[i];
            let b_val = b[i];
            let m_val = m[i];
            let s_val = s0[i];
            let n_val = roughness[i];

            if q_target <= 0.0 || b_val <= 0.0 || m_val < 0.0 || s_val <= 0.0 || n_val <= 0.0
                || q_target.is_nan() || b_val.is_nan() || m_val.is_nan() || s_val.is_nan() || n_val.is_nan() {
                return f64::NAN;
            }

            // Initial guess via wide rectangular approximation
            let mut y = (q_target * n_val / (k * b_val * s_val.sqrt())).powf(0.6).max(0.01);

            for _ in 0..100 {
                let a = (b_val + m_val * y) * y;
                let p = b_val + 2.0 * y * (1.0 + m_val * m_val).sqrt();
                let dp_dy = 2.0 * (1.0 + m_val * m_val).sqrt();
                let da_dy = b_val + 2.0 * m_val * y;

                if p <= 0.0 || a <= 0.0 {
                    return f64::NAN;
                }

                let rh = a / p;
                let q_calc = (k / n_val) * a * rh.powf(2.0 / 3.0) * s_val.sqrt();
                let f_val = q_calc - q_target;

                if f_val.abs() < 1e-9 {
                    return y;
                }

                // Analytical derivative dQ/dy
                let drh_dy = (da_dy * p - a * dp_dy) / (p * p);
                let dq_dy = (k / n_val) * s_val.sqrt() * (da_dy * rh.powf(2.0 / 3.0) + a * (2.0 / 3.0) * rh.powf(-1.0 / 3.0) * drh_dy);

                if dq_dy.abs() < 1e-20 {
                    return f64::NAN;
                }

                let y_next = y - f_val / dq_dy;
                if y_next <= 0.0 {
                    y = y / 2.0;
                } else if (y_next - y).abs() < 1e-9 {
                    return y_next;
                } else {
                    y = y_next;
                }
            }
            y
        })
        .collect()
}

/// Bélanger conjugate depth for rectangular channel:
/// y_2 = (y_1 / 2) * (sqrt(1 + 8 * Fr_1^2) - 1)
pub fn belanger_conjugate_depth_kernel(
    y1: &[f64],
    fr1: &[f64],
) -> Vec<f64> {
    let n = y1.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y = y1[i];
            let fr = fr1[i];

            if y <= 0.0 || fr < 1.0 || y.is_nan() || fr.is_nan() {
                f64::NAN
            } else {
                (y / 2.0) * ((1.0 + 8.0 * fr * fr).sqrt() - 1.0)
            }
        })
        .collect()
}

/// Hydraulic jump energy loss: Delta_E = (y_2 - y_1)^3 / (4 * y_1 * y_2)
pub fn hydraulic_jump_head_loss_kernel(
    y1: &[f64],
    y2: &[f64],
) -> Vec<f64> {
    let n = y1.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y_1 = y1[i];
            let y_2 = y2[i];

            if y_1 <= 0.0 || y_2 <= 0.0 || y_2 < y_1 || y_1.is_nan() || y_2.is_nan() {
                f64::NAN
            } else {
                let dy = y_2 - y_1;
                (dy * dy * dy) / (4.0 * y_1 * y_2)
            }
        })
        .collect()
}

/// Hydraulic jump length: L_j = 6.0 * (y_2 - y_1)
pub fn hydraulic_jump_length_kernel(
    y1: &[f64],
    y2: &[f64],
) -> Vec<f64> {
    let n = y1.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y_1 = y1[i];
            let y_2 = y2[i];

            if y_1 <= 0.0 || y_2 <= 0.0 || y_2 < y_1 || y_1.is_nan() || y_2.is_nan() {
                f64::NAN
            } else {
                6.0 * (y_2 - y_1)
            }
        })
        .collect()
}

/// Gradually Varied Flow water surface gradient: dy/dx = (S_0 - S_f) / (1 - Fr^2)
pub fn gvf_gradient_kernel(
    s0: &[f64],
    sf: &[f64],
    fr: &[f64],
) -> Vec<f64> {
    let n = s0.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let s_0 = s0[i];
            let s_f = sf[i];
            let froude = fr[i];

            if s_0.is_nan() || s_f.is_nan() || froude.is_nan() || (1.0 - froude * froude).abs() < 1e-12 {
                f64::NAN
            } else {
                (s_0 - s_f) / (1.0 - froude * froude)
            }
        })
        .collect()
}

/// Friction slope from Manning equation: S_f = (n^2 * Q^2) / (k^2 * A^2 * R_h^(4/3))
pub fn manning_friction_slope_kernel(
    q: &[f64],
    roughness: &[f64],
    area: &[f64],
    r_h: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let n_val = roughness[i];
            let a = area[i];
            let rh = r_h[i];

            if q_val < 0.0 || n_val <= 0.0 || a <= 0.0 || rh <= 0.0 || q_val.is_nan() || n_val.is_nan() || a.is_nan() || rh.is_nan() {
                f64::NAN
            } else {
                let num = n_val * n_val * q_val * q_val;
                let den = k * k * a * a * rh.powf(4.0 / 3.0);
                if den <= 0.0 { f64::NAN } else { num / den }
            }
        })
        .collect()
}

/// Direct Step Method distance between two sections:
/// Delta_x = (E_2 - E_1) / (S_0 - 0.5 * (S_f1 + S_f2))
pub fn direct_step_kernel(
    e1: &[f64],
    e2: &[f64],
    s0: &[f64],
    sf1: &[f64],
    sf2: &[f64],
) -> Vec<f64> {
    let n = e1.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let e_1 = e1[i];
            let e_2 = e2[i];
            let s_0 = s0[i];
            let s_f1 = sf1[i];
            let s_f2 = sf2[i];

            if e_1.is_nan() || e_2.is_nan() || s_0.is_nan() || s_f1.is_nan() || s_f2.is_nan() {
                f64::NAN
            } else {
                let s_f_avg = 0.5 * (s_f1 + s_f2);
                let den = s_0 - s_f_avg;
                if den.abs() < 1e-15 {
                    f64::NAN
                } else {
                    (e_2 - e_1) / den
                }
            }
        })
        .collect()
}

// ============================================================================
// EXPANSION FORMULAS: OPTIMAL SECTIONS, JUMP DYNAMICS & SEDIMENT MECHANICS
// ============================================================================

/// Optimal Rectangular Section: b = 2*y, A = 2*y^2, P = 4*y, R_h = y/2
pub fn optimal_rectangular_section_kernel(y: &[f64]) -> (Vec<f64>, Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = y.len();
    let mut b_res = vec![0.0; n];
    let mut a_res = vec![0.0; n];
    let mut p_res = vec![0.0; n];
    let mut rh_res = vec![0.0; n];

    b_res.par_iter_mut()
        .zip(a_res.par_iter_mut())
        .zip(p_res.par_iter_mut())
        .zip(rh_res.par_iter_mut())
        .enumerate()
        .for_each(|(i, (((b, a), p), rh))| {
            let y_val = y[i];
            if y_val < 0.0 || y_val.is_nan() {
                *b = f64::NAN;
                *a = f64::NAN;
                *p = f64::NAN;
                *rh = f64::NAN;
            } else {
                *b = 2.0 * y_val;
                *a = 2.0 * y_val * y_val;
                *p = 4.0 * y_val;
                *rh = y_val / 2.0;
            }
        });

    (b_res, a_res, p_res, rh_res)
}

/// Optimal Trapezoidal Section (Best Hydraulic Trapezoid): m = 1/sqrt(3) (~0.57735), b = 2*y/sqrt(3), R_h = y/2
pub fn optimal_trapezoidal_section_kernel(y: &[f64]) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = y.len();
    let mut b_res = vec![0.0; n];
    let mut m_res = vec![0.0; n];
    let mut rh_res = vec![0.0; n];
    let sqrt3 = 3.0_f64.sqrt();
    let m_opt = 1.0 / sqrt3;

    b_res.par_iter_mut()
        .zip(m_res.par_iter_mut())
        .zip(rh_res.par_iter_mut())
        .enumerate()
        .for_each(|(i, ((b, m), rh))| {
            let y_val = y[i];
            if y_val < 0.0 || y_val.is_nan() {
                *b = f64::NAN;
                *m = f64::NAN;
                *rh = f64::NAN;
            } else {
                *b = 2.0 * y_val / sqrt3;
                *m = m_opt;
                *rh = y_val / 2.0;
            }
        });

    (b_res, m_res, rh_res)
}

/// Optimal Triangular Section: m = 1.0 (90 deg apex), A = y^2, P = 2*sqrt(2)*y, R_h = y/(2*sqrt(2))
pub fn optimal_triangular_section_kernel(y: &[f64]) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = y.len();
    let mut a_res = vec![0.0; n];
    let mut p_res = vec![0.0; n];
    let mut rh_res = vec![0.0; n];
    let sqrt2 = 2.0_f64.sqrt();

    a_res.par_iter_mut()
        .zip(p_res.par_iter_mut())
        .zip(rh_res.par_iter_mut())
        .enumerate()
        .for_each(|(i, ((a, p), rh))| {
            let y_val = y[i];
            if y_val < 0.0 || y_val.is_nan() {
                *a = f64::NAN;
                *p = f64::NAN;
                *rh = f64::NAN;
            } else {
                *a = y_val * y_val;
                *p = 2.0 * sqrt2 * y_val;
                *rh = y_val / (2.0 * sqrt2);
            }
        });

    (a_res, p_res, rh_res)
}

/// Critical velocity: V_c = sqrt(g * D_h)
pub fn critical_velocity_kernel(d_h: &[f64], g: f64) -> Vec<f64> {
    let n = d_h.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let dh = d_h[i];
            if dh < 0.0 || dh.is_nan() || g <= 0.0 {
                f64::NAN
            } else {
                (g * dh).sqrt()
            }
        })
        .collect()
}

/// Critical slope: S_c = (g * n^2) / (k^2 * R_hc^(4/3))
pub fn critical_slope_kernel(roughness: &[f64], r_hc: &[f64], g: f64, k: f64) -> Vec<f64> {
    let n = roughness.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let n_val = roughness[i];
            let rh = r_hc[i];
            if n_val <= 0.0 || rh <= 0.0 || g <= 0.0 || k <= 0.0 || n_val.is_nan() || rh.is_nan() {
                f64::NAN
            } else {
                (g * n_val * n_val) / (k * k * rh.powf(4.0 / 3.0))
            }
        })
        .collect()
}

/// Gravity wave celerity: c = sqrt(g * D_h)
pub fn gravity_wave_celerity_kernel(d_h: &[f64], g: f64) -> Vec<f64> {
    critical_velocity_kernel(d_h, g)
}

/// Hydraulic jump efficiency: E_2 / E_1 = ((1 + 8*Fr_1^2)^1.5 - 4*Fr_1^2 + 1) / (8 * Fr_1^2 * (2 + Fr_1^2))
pub fn hydraulic_jump_efficiency_kernel(fr1: &[f64]) -> Vec<f64> {
    let n = fr1.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let f = fr1[i];
            if f < 1.0 || f.is_nan() {
                f64::NAN
            } else {
                let f2 = f * f;
                let num = (1.0 + 8.0 * f2).powf(1.5) - 4.0 * f2 + 1.0;
                let den = 8.0 * f2 * (2.0 + f2);
                if den <= 0.0 { f64::NAN } else { num / den }
            }
        })
        .collect()
}

/// Hydraulic jump height: h_j = y_2 - y_1
pub fn hydraulic_jump_height_kernel(y1: &[f64], y2: &[f64]) -> Vec<f64> {
    let n = y1.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y_1 = y1[i];
            let y_2 = y2[i];
            if y_1 < 0.0 || y_2 < 0.0 || y_1.is_nan() || y_2.is_nan() {
                f64::NAN
            } else {
                y_2 - y_1
            }
        })
        .collect()
}

/// Critical depth in triangular channel: y_c = (2 * Q^2 / (g * m^2))^(1/5)
pub fn critical_depth_triangular_kernel(q: &[f64], m: &[f64], g: f64) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let m_val = m[i];
            if q_val < 0.0 || m_val <= 0.0 || g <= 0.0 || q_val.is_nan() || m_val.is_nan() {
                f64::NAN
            } else {
                (2.0 * q_val * q_val / (g * m_val * m_val)).powf(0.2)
            }
        })
        .collect()
}

/// Horton-Einstein composite Manning n: n_bar = (sum(P_i * n_i^1.5) / sum(P_i))^(2/3)
pub fn horton_einstein_composite_n_kernel(p: &[f64], n_rough: &[f64]) -> f64 {
    let n = p.len();
    let (num, den) = (0..n)
        .into_par_iter()
        .map(|i| {
            let p_val = p[i];
            let n_val = n_rough[i];
            if p_val <= 0.0 || n_val <= 0.0 || p_val.is_nan() || n_val.is_nan() {
                (0.0, 0.0)
            } else {
                (p_val * n_val.powf(1.5), p_val)
            }
        })
        .reduce(|| (0.0, 0.0), |a, b| (a.0 + b.0, a.1 + b.1));

    if den > 0.0 {
        (num / den).powf(2.0 / 3.0)
    } else {
        f64::NAN
    }
}

/// Pavlovskii composite Manning n: n_bar = (sum(P_i * n_i^2) / sum(P_i))^(1/2)
pub fn pavlovskii_composite_n_kernel(p: &[f64], n_rough: &[f64]) -> f64 {
    let n = p.len();
    let (num, den) = (0..n)
        .into_par_iter()
        .map(|i| {
            let p_val = p[i];
            let n_val = n_rough[i];
            if p_val <= 0.0 || n_val <= 0.0 || p_val.is_nan() || n_val.is_nan() {
                (0.0, 0.0)
            } else {
                (p_val * n_val * n_val, p_val)
            }
        })
        .reduce(|| (0.0, 0.0), |a, b| (a.0 + b.0, a.1 + b.1));

    if den > 0.0 {
        (num / den).sqrt()
    } else {
        f64::NAN
    }
}

/// Boundary shear stress: tau_0 = gamma * R_h * S_0
pub fn boundary_shear_stress_kernel(gamma: &[f64], r_h: &[f64], slope: &[f64]) -> Vec<f64> {
    let n = gamma.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let g_val = gamma[i];
            let rh = r_h[i];
            let s = slope[i];
            if g_val <= 0.0 || rh < 0.0 || s < 0.0 || g_val.is_nan() || rh.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                g_val * rh * s
            }
        })
        .collect()
}

/// Shear velocity: u_star = sqrt(g * R_h * S_0)
pub fn shear_velocity_kernel(r_h: &[f64], slope: &[f64], g: f64) -> Vec<f64> {
    let n = r_h.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let rh = r_h[i];
            let s = slope[i];
            if rh < 0.0 || s < 0.0 || g <= 0.0 || rh.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                (g * rh * s).sqrt()
            }
        })
        .collect()
}

/// Shields parameter: theta_star = tau_0 / (delta_gamma * d_50)
pub fn shields_parameter_kernel(tau_0: &[f64], delta_gamma: &[f64], d_50: &[f64]) -> Vec<f64> {
    let n = tau_0.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = tau_0[i];
            let dg = delta_gamma[i];
            let d = d_50[i];
            if t < 0.0 || dg <= 0.0 || d <= 0.0 || t.is_nan() || dg.is_nan() || d.is_nan() {
                f64::NAN
            } else {
                t / (dg * d)
            }
        })
        .collect()
}

/// Critical shear stress: tau_c = theta_c * delta_gamma * d_50
pub fn critical_shear_stress_kernel(theta_c: &[f64], delta_gamma: &[f64], d_50: &[f64]) -> Vec<f64> {
    let n = theta_c.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let tc = theta_c[i];
            let dg = delta_gamma[i];
            let d = d_50[i];
            if tc <= 0.0 || dg <= 0.0 || d <= 0.0 || tc.is_nan() || dg.is_nan() || d.is_nan() {
                f64::NAN
            } else {
                tc * dg * d
            }
        })
        .collect()
}

/// Lane sediment balance index: Q_s_ratio = (Q * S) / d_50
pub fn lane_sediment_balance_kernel(q: &[f64], slope: &[f64], d_50: &[f64]) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let s = slope[i];
            let d = d_50[i];
            if q_val < 0.0 || s < 0.0 || d <= 0.0 || q_val.is_nan() || s.is_nan() || d.is_nan() {
                f64::NAN
            } else {
                (q_val * s) / d
            }
        })
        .collect()
}

/// Meyer-Peter & Müller bedload intensity: q_b_star = 8.0 * (theta_star - 0.047)^1.5 if theta_star > 0.047 else 0.0
pub fn meyer_peter_muller_bedload_kernel(theta_star: &[f64]) -> Vec<f64> {
    let n = theta_star.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let th = theta_star[i];
            if th < 0.0 || th.is_nan() {
                f64::NAN
            } else if th <= 0.047 {
                0.0
            } else {
                8.0 * (th - 0.047).powf(1.5)
            }
        })
        .collect()
}

/// Rubey settling velocity: w_s = sqrt((2/3)*g*(S_s - 1)*d + 36*nu^2/d^2) - (6*nu/d)
pub fn rubey_settling_velocity_kernel(d: &[f64], s_s: &[f64], nu: &[f64], g: f64) -> Vec<f64> {
    let n = d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let d_val = d[i];
            let ss = s_s[i];
            let nu_val = nu[i];
            if d_val <= 0.0 || ss <= 1.0 || nu_val <= 0.0 || g <= 0.0 || d_val.is_nan() || ss.is_nan() || nu_val.is_nan() {
                f64::NAN
            } else {
                let term1 = (2.0 / 3.0) * g * (ss - 1.0) * d_val;
                let term2 = (36.0 * nu_val * nu_val) / (d_val * d_val);
                (term1 + term2).sqrt() - (6.0 * nu_val / d_val)
            }
        })
        .collect()
}

/// Stokes settling velocity: w_s = (g * (S_s - 1) * d^2) / (18 * nu)
pub fn stokes_settling_velocity_kernel(d: &[f64], s_s: &[f64], nu: &[f64], g: f64) -> Vec<f64> {
    let n = d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let d_val = d[i];
            let ss = s_s[i];
            let nu_val = nu[i];
            if d_val <= 0.0 || ss <= 1.0 || nu_val <= 0.0 || g <= 0.0 || d_val.is_nan() || ss.is_nan() || nu_val.is_nan() {
                f64::NAN
            } else {
                (g * (ss - 1.0) * d_val * d_val) / (18.0 * nu_val)
            }
        })
        .collect()
}

// ============================================================================
// DEDICATED BIDIRECTIONAL ALGEBRAIC INVERSIONS (APPROACH 1)
// ============================================================================

/// Inversion: Manning roughness n = (k / Q) * A * R_h^(2/3) * S_0^(1/2)
pub fn manning_n_kernel(
    q: &[f64],
    area: &[f64],
    r_h: &[f64],
    slope: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let a = area[i];
            let rh = r_h[i];
            let s = slope[i];
            if q_val <= 0.0 || a <= 0.0 || rh <= 0.0 || s <= 0.0 || k <= 0.0
                || q_val.is_nan() || a.is_nan() || rh.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                (k / q_val) * a * rh.powf(2.0 / 3.0) * s.sqrt()
            }
        })
        .collect()
}

/// Inversion: Manning slope S_0 = ((Q * n) / (k * A * R_h^(2/3)))^2
pub fn manning_s0_kernel(
    q: &[f64],
    area: &[f64],
    r_h: &[f64],
    roughness: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let a = area[i];
            let rh = r_h[i];
            let n_val = roughness[i];
            if q_val < 0.0 || a <= 0.0 || rh <= 0.0 || n_val <= 0.0 || k <= 0.0
                || q_val.is_nan() || a.is_nan() || rh.is_nan() || n_val.is_nan() {
                f64::NAN
            } else {
                let denom = k * a * rh.powf(2.0 / 3.0);
                let ratio = (q_val * n_val) / denom;
                ratio * ratio
            }
        })
        .collect()
}

/// Inversion: Manning hydraulic radius R_h = ((Q * n) / (k * A * S_0^(1/2)))^(3/2)
pub fn manning_rh_kernel(
    q: &[f64],
    area: &[f64],
    slope: &[f64],
    roughness: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let a = area[i];
            let s = slope[i];
            let n_val = roughness[i];
            if q_val <= 0.0 || a <= 0.0 || s <= 0.0 || n_val <= 0.0 || k <= 0.0
                || q_val.is_nan() || a.is_nan() || s.is_nan() || n_val.is_nan() {
                f64::NAN
            } else {
                let denom = k * a * s.sqrt();
                let ratio = (q_val * n_val) / denom;
                ratio.powf(1.5)
            }
        })
        .collect()
}

/// Inversion: Manning cross-sectional area A = (Q * n) / (k * R_h^(2/3) * S_0^(1/2))
pub fn manning_a_kernel(
    q: &[f64],
    r_h: &[f64],
    slope: &[f64],
    roughness: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let rh = r_h[i];
            let s = slope[i];
            let n_val = roughness[i];
            if q_val < 0.0 || rh <= 0.0 || s <= 0.0 || n_val <= 0.0 || k <= 0.0
                || q_val.is_nan() || rh.is_nan() || s.is_nan() || n_val.is_nan() {
                f64::NAN
            } else {
                (q_val * n_val) / (k * rh.powf(2.0 / 3.0) * s.sqrt())
            }
        })
        .collect()
}

/// Inversion: Chézy coefficient C = V / sqrt(R_h * S_0)
pub fn chezy_c_kernel(
    velocity: &[f64],
    r_h: &[f64],
    slope: &[f64],
) -> Vec<f64> {
    let n = velocity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v = velocity[i];
            let rh = r_h[i];
            let s = slope[i];
            if v < 0.0 || rh <= 0.0 || s <= 0.0 || v.is_nan() || rh.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                v / (rh * s).sqrt()
            }
        })
        .collect()
}

/// Inversion: Chézy slope S_0 = V^2 / (C^2 * R_h)
pub fn chezy_s0_kernel(
    velocity: &[f64],
    c: &[f64],
    r_h: &[f64],
) -> Vec<f64> {
    let n = velocity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v = velocity[i];
            let c_val = c[i];
            let rh = r_h[i];
            if v < 0.0 || c_val <= 0.0 || rh <= 0.0 || v.is_nan() || c_val.is_nan() || rh.is_nan() {
                f64::NAN
            } else {
                (v * v) / (c_val * c_val * rh)
            }
        })
        .collect()
}

/// Inversion: Chézy hydraulic radius R_h = V^2 / (C^2 * S_0)
pub fn chezy_rh_kernel(
    velocity: &[f64],
    c: &[f64],
    slope: &[f64],
) -> Vec<f64> {
    let n = velocity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v = velocity[i];
            let c_val = c[i];
            let s = slope[i];
            if v < 0.0 || c_val <= 0.0 || s <= 0.0 || v.is_nan() || c_val.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                (v * v) / (c_val * c_val * s)
            }
        })
        .collect()
}

/// Inversion: Strickler coefficient k_st = V / (R_h^(2/3) * S_0^(1/2))
pub fn strickler_kst_kernel(
    velocity: &[f64],
    r_h: &[f64],
    slope: &[f64],
) -> Vec<f64> {
    let n = velocity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v = velocity[i];
            let rh = r_h[i];
            let s = slope[i];
            if v < 0.0 || rh <= 0.0 || s <= 0.0 || v.is_nan() || rh.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                v / (rh.powf(2.0 / 3.0) * s.sqrt())
            }
        })
        .collect()
}

/// Inversion: Strickler slope S_0 = (V / (k_st * R_h^(2/3)))^2
pub fn strickler_s0_kernel(
    velocity: &[f64],
    k_st: &[f64],
    r_h: &[f64],
) -> Vec<f64> {
    let n = velocity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v = velocity[i];
            let kst = k_st[i];
            let rh = r_h[i];
            if v < 0.0 || kst <= 0.0 || rh <= 0.0 || v.is_nan() || kst.is_nan() || rh.is_nan() {
                f64::NAN
            } else {
                let ratio = v / (kst * rh.powf(2.0 / 3.0));
                ratio * ratio
            }
        })
        .collect()
}

/// Inversion: Froude velocity V = Fr * sqrt(g * D_h)
pub fn froude_v_kernel(
    fr: &[f64],
    d_h: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = fr.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let f = fr[i];
            let dh = d_h[i];
            if f < 0.0 || dh <= 0.0 || g <= 0.0 || f.is_nan() || dh.is_nan() {
                f64::NAN
            } else {
                f * (g * dh).sqrt()
            }
        })
        .collect()
}

/// Inversion: Froude hydraulic depth D_h = V^2 / (g * Fr^2)
pub fn froude_dh_kernel(
    fr: &[f64],
    velocity: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = fr.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let f = fr[i];
            let v = velocity[i];
            if f <= 0.0 || v < 0.0 || g <= 0.0 || f.is_nan() || v.is_nan() {
                f64::NAN
            } else {
                (v * v) / (g * f * f)
            }
        })
        .collect()
}

/// Inversion: Specific energy velocity V = sqrt(2 * g * (E - y))
pub fn specific_energy_v_kernel(
    e: &[f64],
    y: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = e.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let e_val = e[i];
            let y_val = y[i];
            if e_val < y_val || y_val <= 0.0 || g <= 0.0 || e_val.is_nan() || y_val.is_nan() {
                f64::NAN
            } else {
                (2.0 * g * (e_val - y_val)).sqrt()
            }
        })
        .collect()
}

/// Inversion: Hydraulic Jump Froude number Fr_1 = sqrt(0.125 * ((2 * y_2 / y_1 + 1)^2 - 1))
pub fn hydraulic_jump_fr1_kernel(
    y1: &[f64],
    y2: &[f64],
) -> Vec<f64> {
    let n = y1.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y1_val = y1[i];
            let y2_val = y2[i];
            if y1_val <= 0.0 || y2_val < y1_val || y1_val.is_nan() || y2_val.is_nan() {
                f64::NAN
            } else {
                let term = 2.0 * y2_val / y1_val + 1.0;
                let inside = 0.125 * (term * term - 1.0);
                if inside < 0.0 {
                    0.0
                } else {
                    inside.sqrt()
                }
            }
        })
        .collect()
}

/// Inversion: Initial depth y_1 from sequent depth y_2 and Fr_1: y_1 = y_2 / (0.5 * (sqrt(1 + 8*Fr_1^2) - 1))
pub fn hydraulic_jump_y1_kernel(
    y2: &[f64],
    fr1: &[f64],
) -> Vec<f64> {
    let n = y2.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y2_val = y2[i];
            let fr = fr1[i];
            if y2_val <= 0.0 || fr <= 1.0 || y2_val.is_nan() || fr.is_nan() {
                f64::NAN
            } else {
                let denom = 0.5 * ((1.0 + 8.0 * fr * fr).sqrt() - 1.0);
                y2_val / denom
            }
        })
        .collect()
}

/// Inversion: Critical depth rectangular channel discharge Q = b * sqrt(g * y_c^3)
pub fn critical_depth_rect_q_kernel(
    yc: &[f64],
    b: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = yc.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let yc_val = yc[i];
            let b_val = b[i];
            if yc_val <= 0.0 || b_val <= 0.0 || g <= 0.0 || yc_val.is_nan() || b_val.is_nan() {
                f64::NAN
            } else {
                b_val * (g * yc_val.powi(3)).sqrt()
            }
        })
        .collect()
}

/// Inversion: Critical depth triangular channel discharge Q = sqrt(0.5 * g * z^2 * y_c^5)
pub fn critical_depth_tri_q_kernel(
    yc: &[f64],
    z: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = yc.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let yc_val = yc[i];
            let z_val = z[i];
            if yc_val <= 0.0 || z_val <= 0.0 || g <= 0.0 || yc_val.is_nan() || z_val.is_nan() {
                f64::NAN
            } else {
                (0.5 * g * z_val * z_val * yc_val.powi(5)).sqrt()
            }
        })
        .collect()
}

/// Inversion: Critical velocity hydraulic depth D_h = V_c^2 / g
pub fn critical_velocity_dh_kernel(
    vc: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = vc.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let vc_val = vc[i];
            if vc_val < 0.0 || g <= 0.0 || vc_val.is_nan() {
                f64::NAN
            } else {
                (vc_val * vc_val) / g
            }
        })
        .collect()
}

/// Inversion: Critical slope roughness n = (k / Q) * A_c * R_c^(2/3) * S_c^(1/2) for rectangular section
pub fn critical_slope_n_kernel(
    sc: &[f64],
    q: &[f64],
    b: &[f64],
    g: f64,
    k: f64,
) -> Vec<f64> {
    let n = sc.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let s = sc[i];
            let q_val = q[i];
            let b_val = b[i];
            if s <= 0.0 || q_val <= 0.0 || b_val <= 0.0 || g <= 0.0 || k <= 0.0
                || s.is_nan() || q_val.is_nan() || b_val.is_nan() {
                f64::NAN
            } else {
                let q_unit = q_val / b_val;
                let yc = (q_unit * q_unit / g).powf(1.0 / 3.0);
                let ac = b_val * yc;
                let rc = ac / (b_val + 2.0 * yc);
                (k / q_val) * ac * rc.powf(2.0 / 3.0) * s.sqrt()
            }
        })
        .collect()
}

/// Inversion: Boundary shear slope S_0 = tau_0 / (gamma * R_h)
pub fn boundary_shear_s0_kernel(
    tau_0: &[f64],
    gamma: &[f64],
    r_h: &[f64],
) -> Vec<f64> {
    let n = tau_0.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = tau_0[i];
            let g = gamma[i];
            let rh = r_h[i];
            if t < 0.0 || g <= 0.0 || rh <= 0.0 || t.is_nan() || g.is_nan() || rh.is_nan() {
                f64::NAN
            } else {
                t / (g * rh)
            }
        })
        .collect()
}

/// Inversion: Boundary shear hydraulic radius R_h = tau_0 / (gamma * S_0)
pub fn boundary_shear_rh_kernel(
    tau_0: &[f64],
    gamma: &[f64],
    slope: &[f64],
) -> Vec<f64> {
    let n = tau_0.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = tau_0[i];
            let g = gamma[i];
            let s = slope[i];
            if t < 0.0 || g <= 0.0 || s <= 0.0 || t.is_nan() || g.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                t / (g * s)
            }
        })
        .collect()
}

/// Inversion: Shields parameter shear stress tau_0 = theta_star * (gamma_s - gamma_w) * d50
pub fn shields_param_tau0_kernel(
    theta_star: &[f64],
    gamma_s: &[f64],
    gamma_w: &[f64],
    d50: &[f64],
) -> Vec<f64> {
    let n = theta_star.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let th = theta_star[i];
            let gs = gamma_s[i];
            let gw = gamma_w[i];
            let d = d50[i];
            if th < 0.0 || gs <= gw || gw <= 0.0 || d <= 0.0
                || th.is_nan() || gs.is_nan() || gw.is_nan() || d.is_nan() {
                f64::NAN
            } else {
                th * (gs - gw) * d
            }
        })
        .collect()
}

/// Inversion: Shields parameter particle diameter d50 = tau_0 / (theta_star * (gamma_s - gamma_w))
pub fn shields_param_d50_kernel(
    theta_star: &[f64],
    tau_0: &[f64],
    gamma_s: &[f64],
    gamma_w: &[f64],
) -> Vec<f64> {
    let n = theta_star.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let th = theta_star[i];
            let t = tau_0[i];
            let gs = gamma_s[i];
            let gw = gamma_w[i];
            if th <= 0.0 || t < 0.0 || gs <= gw || gw <= 0.0
                || th.is_nan() || t.is_nan() || gs.is_nan() || gw.is_nan() {
                f64::NAN
            } else {
                t / (th * (gs - gw))
            }
        })
        .collect()
}

/// Inversion: Lane balance slope S = Q_s * d50 / Q_w
pub fn lane_balance_s_kernel(
    qs: &[f64],
    d50: &[f64],
    qw: &[f64],
) -> Vec<f64> {
    let n = qs.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let qs_val = qs[i];
            let d = d50[i];
            let qw_val = qw[i];
            if qs_val < 0.0 || d <= 0.0 || qw_val <= 0.0 || qs_val.is_nan() || d.is_nan() || qw_val.is_nan() {
                f64::NAN
            } else {
                (qs_val * d) / qw_val
            }
        })
        .collect()
}

/// Inversion: Stokes settling diameter d = sqrt((18 * nu * w_s) / (g * (S_s - 1)))
pub fn stokes_settling_d_kernel(
    ws: &[f64],
    s_s: &[f64],
    nu: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = ws.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ws_val = ws[i];
            let ss = s_s[i];
            let nu_val = nu[i];
            if ws_val <= 0.0 || ss <= 1.0 || nu_val <= 0.0 || g <= 0.0
                || ws_val.is_nan() || ss.is_nan() || nu_val.is_nan() {
                f64::NAN
            } else {
                ((18.0 * nu_val * ws_val) / (g * (ss - 1.0))).sqrt()
            }
        })
        .collect()
}

