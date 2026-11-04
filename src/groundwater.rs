//! Seepage & Groundwater Module
//! High-performance Rayon-parallelized computations for Darcy flow,
//! Thiem equilibrium equations, and Theis non-equilibrium transient well equations.

use rayon::prelude::*;
use std::f64::consts::PI;

/// Darcy 1D Flow: Q = -K * A * dh_dl
pub fn darcy_flow_1d_kernel(
    k: &[f64],
    area: &[f64],
    dh_dl: &[f64],
) -> Vec<f64> {
    let n = k.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let k_val = k[i];
            let a_val = area[i];
            let grad = dh_dl[i];

            if k_val < 0.0 || a_val < 0.0 || k_val.is_nan() || a_val.is_nan() || grad.is_nan() {
                f64::NAN
            } else {
                -k_val * a_val * grad
            }
        })
        .collect()
}

/// Darcy Flux (Specific Discharge): q = -K * dh_dl
pub fn darcy_flux_kernel(
    k: &[f64],
    dh_dl: &[f64],
) -> Vec<f64> {
    let n = k.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let k_val = k[i];
            let grad = dh_dl[i];

            if k_val < 0.0 || k_val.is_nan() || grad.is_nan() {
                f64::NAN
            } else {
                -k_val * grad
            }
        })
        .collect()
}

/// Thiem steady-state confined well:
/// Q = (2 * pi * T * (h_2 - h_1)) / ln(r_2 / r_1)
pub fn thiem_confined_kernel(
    transmissivity: &[f64],
    h1: &[f64],
    h2: &[f64],
    r1: &[f64],
    r2: &[f64],
) -> Vec<f64> {
    let n = transmissivity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = transmissivity[i];
            let head1 = h1[i];
            let head2 = h2[i];
            let rad1 = r1[i];
            let rad2 = r2[i];

            if t <= 0.0 || rad1 <= 0.0 || rad2 <= rad1
                || t.is_nan() || head1.is_nan() || head2.is_nan() || rad1.is_nan() || rad2.is_nan() {
                f64::NAN
            } else {
                let ln_ratio = (rad2 / rad1).ln();
                (2.0 * PI * t * (head2 - head1)) / ln_ratio
            }
        })
        .collect()
}

/// Thiem steady-state unconfined well (Dupuit):
/// Q = (pi * K * (h_2^2 - h_1^2)) / ln(r_2 / r_1)
pub fn thiem_unconfined_kernel(
    conductivity: &[f64],
    h1: &[f64],
    h2: &[f64],
    r1: &[f64],
    r2: &[f64],
) -> Vec<f64> {
    let n = conductivity.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let k = conductivity[i];
            let head1 = h1[i];
            let head2 = h2[i];
            let rad1 = r1[i];
            let rad2 = r2[i];

            if k <= 0.0 || rad1 <= 0.0 || rad2 <= rad1 || head1 < 0.0 || head2 < 0.0
                || k.is_nan() || head1.is_nan() || head2.is_nan() || rad1.is_nan() || rad2.is_nan() {
                f64::NAN
            } else {
                let ln_ratio = (rad2 / rad1).ln();
                (PI * k * (head2 * head2 - head1 * head1)) / ln_ratio
            }
        })
        .collect()
}

/// High-accuracy Well Function W(u) = E_1(u) (Exponential Integral)
/// Valid for all u > 0.
#[inline]
pub fn well_function_w(u: f64) -> f64 {
    if u <= 0.0 || u.is_nan() {
        return f64::NAN;
    }
    if u > 40.0 {
        return 0.0;
    }

    // Euler-Mascheroni constant
    const EULER: f64 = 0.57721566490153286;

    if u <= 1.0 {
        // Series expansion: W(u) = -ln(u) - gamma - sum_{n=1}^inf (-u)^n / (n * n!)
        let mut sum = 0.0;
        let mut term = -u;
        for n in 1..=50 {
            let delta = term / (n as f64);
            sum += delta;
            if delta.abs() < 1e-15 {
                break;
            }
            term = -term * u / ((n + 1) as f64);
        }
        -u.ln() - EULER - sum
    } else {
        // Continued fraction for u > 1 (Lenz's method)
        // E1(u) = exp(-u) / (u + 1/(1 + 1/(u + 2/(1 + 2/(u + ...)))))
        let mut c = 1e-30;
        let mut d = 0.0;
        let mut f = 1e-30;

        for i in 1..=100 {
            let a = if i % 2 == 1 {
                ((i + 1) / 2) as f64
            } else {
                (i / 2) as f64
            };
            let b = if i % 2 == 1 {
                u
            } else {
                1.0
            };

            d = b + a * d;
            if d.abs() < 1e-30 { d = 1e-30; }
            c = b + a / c;
            if c.abs() < 1e-30 { c = 1e-30; }
            d = 1.0 / d;
            let delta = c * d;
            f *= delta;
            if (delta - 1.0).abs() < 1e-15 {
                break;
            }
        }
        (-u).exp() / (u + f)
    }
}

/// Theis non-equilibrium transient well drawdown:
/// s = (Q / (4 * pi * T)) * W(u)
/// u = (r^2 * S) / (4 * T * t)
pub fn theis_drawdown_kernel(
    pumping_rate: &[f64],
    transmissivity: &[f64],
    storativity: &[f64],
    radius: &[f64],
    time: &[f64],
) -> Vec<f64> {
    let n = pumping_rate.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q = pumping_rate[i];
            let t = transmissivity[i];
            let s = storativity[i];
            let r = radius[i];
            let time_val = time[i];

            if q < 0.0 || t <= 0.0 || s <= 0.0 || r <= 0.0 || time_val <= 0.0
                || q.is_nan() || t.is_nan() || s.is_nan() || r.is_nan() || time_val.is_nan() {
                f64::NAN
            } else {
                let u = (r * r * s) / (4.0 * t * time_val);
                let wu = well_function_w(u);
                (q / (4.0 * PI * t)) * wu
            }
        })
        .collect()
}

/// Cooper-Jacob approximation for well drawdown (valid for u < 0.05):
/// s = (2.302585 * Q / (4 * pi * T)) * log10((2.25 * T * t) / (r^2 * S))
pub fn cooper_jacob_drawdown_kernel(
    pumping_rate: &[f64],
    transmissivity: &[f64],
    storativity: &[f64],
    radius: &[f64],
    time: &[f64],
) -> Vec<f64> {
    let n = pumping_rate.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q = pumping_rate[i];
            let t = transmissivity[i];
            let s = storativity[i];
            let r = radius[i];
            let time_val = time[i];

            if q < 0.0 || t <= 0.0 || s <= 0.0 || r <= 0.0 || time_val <= 0.0
                || q.is_nan() || t.is_nan() || s.is_nan() || r.is_nan() || time_val.is_nan() {
                f64::NAN
            } else {
                let arg = (2.25 * t * time_val) / (r * r * s);
                if arg <= 0.0 {
                    f64::NAN
                } else {
                    (2.302585092994046 * q / (4.0 * PI * t)) * arg.log10()
                }
            }
        })
        .collect()
}

// ============================================================================
// DEDICATED BIDIRECTIONAL ALGEBRAIC INVERSIONS (APPROACH 1)
// ============================================================================

/// Inversion: Darcy hydraulic conductivity K = -Q / (A * dh_dl)
pub fn darcy_flow_k_kernel(
    q: &[f64],
    area: &[f64],
    dh_dl: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let a = area[i];
            let grad = dh_dl[i];
            if a <= 0.0 || grad == 0.0 || q_val.is_nan() || a.is_nan() || grad.is_nan() {
                f64::NAN
            } else {
                -q_val / (a * grad)
            }
        })
        .collect()
}

/// Inversion: Darcy hydraulic gradient dh_dl = -Q / (K * A)
pub fn darcy_flow_dh_dl_kernel(
    q: &[f64],
    k: &[f64],
    area: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let k_val = k[i];
            let a = area[i];
            if k_val <= 0.0 || a <= 0.0 || q_val.is_nan() || k_val.is_nan() || a.is_nan() {
                f64::NAN
            } else {
                -q_val / (k_val * a)
            }
        })
        .collect()
}

/// Inversion: Thiem confined transmissivity T = (Q * ln(r_2 / r_1)) / (2 * pi * (h_2 - h_1))
pub fn thiem_confined_t_kernel(
    q: &[f64],
    h1: &[f64],
    h2: &[f64],
    r1: &[f64],
    r2: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let head1 = h1[i];
            let head2 = h2[i];
            let rad1 = r1[i];
            let rad2 = r2[i];
            if q_val <= 0.0 || rad1 <= 0.0 || rad2 <= rad1 || head2 <= head1
                || q_val.is_nan() || head1.is_nan() || head2.is_nan() || rad1.is_nan() || rad2.is_nan() {
                f64::NAN
            } else {
                let ln_ratio = (rad2 / rad1).ln();
                (q_val * ln_ratio) / (2.0 * PI * (head2 - head1))
            }
        })
        .collect()
}

/// Inversion: Thiem confined head difference (h_2 - h_1) = (Q * ln(r_2 / r_1)) / (2 * pi * T)
pub fn thiem_confined_dh_kernel(
    q: &[f64],
    transmissivity: &[f64],
    r1: &[f64],
    r2: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let t = transmissivity[i];
            let rad1 = r1[i];
            let rad2 = r2[i];
            if q_val < 0.0 || t <= 0.0 || rad1 <= 0.0 || rad2 <= rad1
                || q_val.is_nan() || t.is_nan() || rad1.is_nan() || rad2.is_nan() {
                f64::NAN
            } else {
                let ln_ratio = (rad2 / rad1).ln();
                (q_val * ln_ratio) / (2.0 * PI * t)
            }
        })
        .collect()
}

/// Inversion: Thiem unconfined hydraulic conductivity K = (Q * ln(r_2 / r_1)) / (pi * (h_2^2 - h_1^2))
pub fn thiem_unconfined_k_kernel(
    q: &[f64],
    h1: &[f64],
    h2: &[f64],
    r1: &[f64],
    r2: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let head1 = h1[i];
            let head2 = h2[i];
            let rad1 = r1[i];
            let rad2 = r2[i];
            if q_val <= 0.0 || rad1 <= 0.0 || rad2 <= rad1 || head2 <= head1 || head1 < 0.0
                || q_val.is_nan() || head1.is_nan() || head2.is_nan() || rad1.is_nan() || rad2.is_nan() {
                f64::NAN
            } else {
                let ln_ratio = (rad2 / rad1).ln();
                let head_diff_sq = head2 * head2 - head1 * head1;
                (q_val * ln_ratio) / (PI * head_diff_sq)
            }
        })
        .collect()
}

/// Inversion: Cooper-Jacob pumping rate Q = (4 * pi * T * s) / (2.302585 * log10((2.25 * T * t) / (r^2 * S)))
pub fn cooper_jacob_q_kernel(
    s: &[f64],
    transmissivity: &[f64],
    storativity: &[f64],
    radius: &[f64],
    time: &[f64],
) -> Vec<f64> {
    let n = s.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let s_val = s[i];
            let t = transmissivity[i];
            let stor = storativity[i];
            let r = radius[i];
            let time_val = time[i];
            if s_val < 0.0 || t <= 0.0 || stor <= 0.0 || r <= 0.0 || time_val <= 0.0
                || s_val.is_nan() || t.is_nan() || stor.is_nan() || r.is_nan() || time_val.is_nan() {
                f64::NAN
            } else {
                let arg = (2.25 * t * time_val) / (r * r * stor);
                if arg <= 1.0 {
                    f64::NAN
                } else {
                    (4.0 * PI * t * s_val) / (2.302585092994046 * arg.log10())
                }
            }
        })
        .collect()
}

