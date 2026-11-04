//! Surface Water Hydrology & Runoff Module
//! High-performance Rayon-parallelized computations for precipitation,
//! infiltration, runoff depth, peak flow, unit hydrographs, and flood routing.

use rayon::prelude::*;

/// IDF Sherman equation: i = a / ((t_d + b)^c)
pub fn idf_sherman_kernel(
    t_d: &[f64],
    a: &[f64],
    b: &[f64],
    c: &[f64],
) -> Vec<f64> {
    let n = t_d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = t_d[i];
            let a_val = a[i];
            let b_val = b[i];
            let c_val = c[i];

            if t <= 0.0 || a_val < 0.0 || b_val < 0.0 || c_val <= 0.0
                || t.is_nan() || a_val.is_nan() || b_val.is_nan() || c_val.is_nan() {
                f64::NAN
            } else {
                a_val / (t + b_val).powf(c_val)
            }
        })
        .collect()
}

/// Thiessen polygon areal weighted mean rainfall: P_mean = sum(A_i * P_i) / sum(A_i)
pub fn thiessen_areal_kernel(
    weights: &[f64],
    precip: &[f64],
) -> f64 {
    let n = weights.len();
    let (total_weighted, total_area) = (0..n)
        .into_par_iter()
        .map(|i| {
            let w = weights[i];
            let p = precip[i];
            if w < 0.0 || p < 0.0 || w.is_nan() || p.is_nan() {
                (0.0, 0.0)
            } else {
                (w * p, w)
            }
        })
        .reduce(|| (0.0, 0.0), |a, b| (a.0 + b.0, a.1 + b.1));

    if total_area > 0.0 {
        total_weighted / total_area
    } else {
        f64::NAN
    }
}

/// Horton infiltration rate: f_p = f_c + (f_0 - f_c) * exp(-k * t)
pub fn horton_rate_kernel(
    time: &[f64],
    f0: &[f64],
    fc: &[f64],
    k: &[f64],
) -> Vec<f64> {
    let n = time.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = time[i];
            let f_0 = f0[i];
            let f_c = fc[i];
            let k_val = k[i];

            if t < 0.0 || f_0 < 0.0 || f_c < 0.0 || k_val < 0.0
                || t.is_nan() || f_0.is_nan() || f_c.is_nan() || k_val.is_nan() {
                f64::NAN
            } else {
                f_c + (f_0 - f_c) * (-k_val * t).exp()
            }
        })
        .collect()
}

/// Horton cumulative infiltration: F = f_c * t + ((f_0 - f_c) / k) * (1 - exp(-k * t))
pub fn horton_cumulative_kernel(
    time: &[f64],
    f0: &[f64],
    fc: &[f64],
    k: &[f64],
) -> Vec<f64> {
    let n = time.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = time[i];
            let f_0 = f0[i];
            let f_c = fc[i];
            let k_val = k[i];

            if t < 0.0 || f_0 < 0.0 || f_c < 0.0 || k_val <= 0.0
                || t.is_nan() || f_0.is_nan() || f_c.is_nan() || k_val.is_nan() {
                f64::NAN
            } else {
                f_c * t + ((f_0 - f_c) / k_val) * (1.0 - (-k_val * t).exp())
            }
        })
        .collect()
}

/// Green-Ampt infiltration rate: f = K_s * (1 + (psi * delta_theta) / F)
pub fn green_ampt_rate_kernel(
    k_s: &[f64],
    psi: &[f64],
    delta_theta: &[f64],
    f_cum: &[f64],
) -> Vec<f64> {
    let n = k_s.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ks = k_s[i];
            let p = psi[i];
            let dt = delta_theta[i];
            let f = f_cum[i];

            if ks < 0.0 || p < 0.0 || dt < 0.0 || f <= 0.0
                || ks.is_nan() || p.is_nan() || dt.is_nan() || f.is_nan() {
                f64::NAN
            } else {
                ks * (1.0 + (p * dt) / f)
            }
        })
        .collect()
}

/// SCS Curve Number potential maximum retention:
/// S = (k_s / CN) - s_sub
/// SI: k_s = 25400.0, s_sub = 254.0 (mm)
/// US: k_s = 1000.0, s_sub = 10.0 (inches)
pub fn scs_retention_kernel(
    cn: &[f64],
    k_s: f64,
    s_sub: f64,
) -> Vec<f64> {
    let n = cn.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let curve_num = cn[i];
            if curve_num <= 0.0 || curve_num > 100.0 || curve_num.is_nan() {
                f64::NAN
            } else {
                (k_s / curve_num) - s_sub
            }
        })
        .collect()
}

/// SCS Curve Number runoff depth:
/// Q = ((P - I_a)^2) / (P - I_a + S) if P > I_a else 0.0
/// I_a = lambda * S (default lambda = 0.2)
pub fn scs_runoff_depth_kernel(
    precip: &[f64],
    retention: &[f64],
    lambda_ratio: &[f64],
) -> Vec<f64> {
    let n = precip.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = precip[i];
            let s = retention[i];
            let lam = lambda_ratio[i];

            if p < 0.0 || s < 0.0 || lam < 0.0 || p.is_nan() || s.is_nan() || lam.is_nan() {
                f64::NAN
            } else {
                let ia = lam * s;
                if p <= ia {
                    0.0
                } else {
                    let num = (p - ia) * (p - ia);
                    let den = p - ia + s;
                    if den <= 0.0 { 0.0 } else { num / den }
                }
            }
        })
        .collect()
}

/// Rational Method peak discharge:
/// SI: Q = 0.2778 * C * I * A (Q in m3/s, I in mm/hr, A in km2)
/// US: Q = C * I * A (Q in cfs, I in in/hr, A in acres)
pub fn rational_peak_flow_kernel(
    c: &[f64],
    intensity: &[f64],
    area: &[f64],
    k_factor: f64,
) -> Vec<f64> {
    let n = c.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let c_val = c[i];
            let i_val = intensity[i];
            let a_val = area[i];

            if c_val < 0.0 || i_val < 0.0 || a_val < 0.0
                || c_val.is_nan() || i_val.is_nan() || a_val.is_nan() {
                f64::NAN
            } else {
                k_factor * c_val * i_val * a_val
            }
        })
        .collect()
}

/// Kirpich time of concentration (minutes):
/// t_c = k_kirpich * L^0.77 * S^(-0.385)
/// k_kirpich = 0.01947 (SI: L in m) or 0.0078 (US: L in ft)
pub fn kirpich_tc_kernel(
    length: &[f64],
    slope: &[f64],
    k_kirpich: f64,
) -> Vec<f64> {
    let n = length.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = length[i];
            let s = slope[i];

            if l <= 0.0 || s <= 0.0 || l.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                k_kirpich * l.powf(0.77) * s.powf(-0.385)
            }
        })
        .collect()
}

/// Snyder's synthetic unit hydrograph parameters:
/// t_p = C_t * (L * L_c)^0.3 (basin lag, hr)
/// Q_p = (C_p * A) / t_p * k_snyder (peak discharge)
pub fn snyder_kernel(
    length: &[f64],
    length_centroid: &[f64],
    area: &[f64],
    c_t: &[f64],
    c_p: &[f64],
    k_snyder: f64,
) -> (Vec<f64>, Vec<f64>) {
    let n = length.len();
    let mut lag = vec![0.0; n];
    let mut peak = vec![0.0; n];

    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = length[i];
            let lc = length_centroid[i];
            let a = area[i];
            let ct = c_t[i];
            let cp = c_p[i];

            if l <= 0.0 || lc <= 0.0 || a <= 0.0 || ct <= 0.0 || cp <= 0.0
                || l.is_nan() || lc.is_nan() || a.is_nan() || ct.is_nan() || cp.is_nan() {
                (f64::NAN, f64::NAN)
            } else {
                let tp = ct * (l * lc).powf(0.3);
                let qp = if tp > 0.0 { (k_snyder * cp * a) / tp } else { f64::NAN };
                (tp, qp)
            }
        })
        .collect::<Vec<_>>()
        .into_iter()
        .enumerate()
        .for_each(|(i, (tp, qp))| {
            lag[i] = tp;
            peak[i] = qp;
        });

    (lag, peak)
}

/// SCS Dimensionless Unit Hydrograph peak flow:
/// q_p = (k_scs * A) / t_p
/// k_scs = 0.208 (SI: A km2, t_p hr, q_p m3/s) or 484.0 (US: A mi2, t_p hr, q_p cfs)
pub fn scs_peak_flow_kernel(
    area: &[f64],
    time_to_peak: &[f64],
    k_scs: f64,
) -> Vec<f64> {
    let n = area.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let a = area[i];
            let tp = time_to_peak[i];

            if a <= 0.0 || tp <= 0.0 || a.is_nan() || tp.is_nan() {
                f64::NAN
            } else {
                (k_scs * a) / tp
            }
        })
        .collect()
}

/// Muskingum routing coefficients:
/// C_0 = (dt - 2*K*X) / (2*K*(1-X) + dt)
/// C_1 = (dt + 2*K*X) / (2*K*(1-X) + dt)
/// C_2 = (2*K*(1-X) - dt) / (2*K*(1-X) + dt)
pub fn muskingum_coefficients_kernel(
    k: &[f64],
    x: &[f64],
    dt: &[f64],
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let n = k.len();
    let mut c0_vec = vec![0.0; n];
    let mut c1_vec = vec![0.0; n];
    let mut c2_vec = vec![0.0; n];

    (0..n)
        .into_par_iter()
        .map(|i| {
            let k_val = k[i];
            let x_val = x[i];
            let dt_val = dt[i];

            if k_val <= 0.0 || x_val < 0.0 || x_val > 0.5 || dt_val <= 0.0
                || k_val.is_nan() || x_val.is_nan() || dt_val.is_nan() {
                (f64::NAN, f64::NAN, f64::NAN)
            } else {
                let denom = 2.0 * k_val * (1.0 - x_val) + dt_val;
                if denom.abs() < 1e-15 {
                    (f64::NAN, f64::NAN, f64::NAN)
                } else {
                    let c0 = (dt_val - 2.0 * k_val * x_val) / denom;
                    let c1 = (dt_val + 2.0 * k_val * x_val) / denom;
                    let c2 = (2.0 * k_val * (1.0 - x_val) - dt_val) / denom;
                    (c0, c1, c2)
                }
            }
        })
        .collect::<Vec<_>>()
        .into_iter()
        .enumerate()
        .for_each(|(i, (c0, c1, c2))| {
            c0_vec[i] = c0;
            c1_vec[i] = c1;
            c2_vec[i] = c2;
        });

    (c0_vec, c1_vec, c2_vec)
}

/// Muskingum route time series through a reach:
/// Q[j+1] = C0 * I[j+1] + C1 * I[j] + C2 * Q[j]
pub fn muskingum_route_kernel(
    inflow: &[f64],
    k: f64,
    x: f64,
    dt: f64,
    initial_outflow: f64,
) -> Vec<f64> {
    let n = inflow.len();
    if n == 0 {
        return vec![];
    }
    let mut outflow = vec![0.0; n];
    outflow[0] = initial_outflow;

    let denom = 2.0 * k * (1.0 - x) + dt;
    if denom.abs() < 1e-15 || k <= 0.0 || x < 0.0 || dt <= 0.0 {
        return vec![f64::NAN; n];
    }

    let c0 = (dt - 2.0 * k * x) / denom;
    let c1 = (dt + 2.0 * k * x) / denom;
    let c2 = (2.0 * k * (1.0 - x) - dt) / denom;

    for j in 0..(n - 1) {
        let i_curr = inflow[j + 1];
        let i_prev = inflow[j];
        let q_prev = outflow[j];
        outflow[j + 1] = c0 * i_curr + c1 * i_prev + c2 * q_prev;
    }

    outflow
}

// ============================================================================
// EXPANSION FORMULAS: ADVANCED HYDROLOGY & WATERSHED MODELLING
// ============================================================================

/// SCS Composite Curve Number: CN_bar = sum(A_i * CN_i) / sum(A_i)
pub fn scs_composite_cn_kernel(
    areas: &[f64],
    cns: &[f64],
) -> f64 {
    let n = areas.len();
    let (num, den) = (0..n)
        .into_par_iter()
        .map(|i| {
            let a = areas[i];
            let cn = cns[i];
            if a < 0.0 || cn <= 0.0 || a.is_nan() || cn.is_nan() {
                (0.0, 0.0)
            } else {
                (a * cn, a)
            }
        })
        .reduce(|| (0.0, 0.0), |a, b| (a.0 + b.0, a.1 + b.1));

    if den > 0.0 {
        num / den
    } else {
        f64::NAN
    }
}

/// SCS AMC I (Dry antecedent moisture condition) Curve Number:
/// CN_I = (4.2 * CN_II) / (10.0 - 0.058 * CN_II)
pub fn scs_cn_amc_i_kernel(cn_ii: &[f64]) -> Vec<f64> {
    let n = cn_ii.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let cn2 = cn_ii[i];
            if cn2 < 10.0 || cn2 > 100.0 || cn2.is_nan() {
                f64::NAN
            } else {
                let den = 10.0 - 0.058 * cn2;
                if den <= 0.0 { f64::NAN } else { (4.2 * cn2) / den }
            }
        })
        .collect()
}

/// SCS AMC III (Wet antecedent moisture condition) Curve Number:
/// CN_III = (23.0 * CN_II) / (10.0 + 0.13 * CN_II)
pub fn scs_cn_amc_iii_kernel(cn_ii: &[f64]) -> Vec<f64> {
    let n = cn_ii.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let cn2 = cn_ii[i];
            if cn2 < 10.0 || cn2 > 100.0 || cn2.is_nan() {
                f64::NAN
            } else {
                let den = 10.0 + 0.13 * cn2;
                if den <= 0.0 { f64::NAN } else { (23.0 * cn2) / den }
            }
        })
        .collect()
}

/// TR-55 Sheet Flow Travel Time:
/// T_t = (0.007 * (n * L)^0.8) / (P_2^0.5 * s^0.4) (hr)
pub fn tr55_sheet_flow_time_kernel(
    n_manning: &[f64],
    length: &[f64],
    p2_precip: &[f64],
    slope: &[f64],
) -> Vec<f64> {
    let n = n_manning.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let nm = n_manning[i];
            let l = length[i];
            let p2 = p2_precip[i];
            let s = slope[i];

            if nm <= 0.0 || l <= 0.0 || p2 <= 0.0 || s <= 0.0
                || nm.is_nan() || l.is_nan() || p2.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                (0.007 * (nm * l).powf(0.8)) / (p2.sqrt() * s.powf(0.4))
            }
        })
        .collect()
}

/// TR-55 Shallow Concentrated Flow Velocity:
/// V = k_surface * sqrt(s)
pub fn tr55_shallow_concentrated_velocity_kernel(
    slope: &[f64],
    k_surface: &[f64],
) -> Vec<f64> {
    let n = slope.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let s = slope[i];
            let k = k_surface[i];

            if s < 0.0 || k <= 0.0 || s.is_nan() || k.is_nan() {
                f64::NAN
            } else {
                k * s.sqrt()
            }
        })
        .collect()
}

/// Gumbel (EV-1) Extreme Value Flood Frequency Quantile:
/// X_T = mean_X + K_T * std_X
/// K_T = -(sqrt(6)/pi) * (0.5772156649 + ln(ln(T / (T - 1))))
pub fn gumbel_flood_frequency_kernel(
    mean_x: &[f64],
    std_x: &[f64],
    return_period: &[f64],
) -> Vec<f64> {
    let n = mean_x.len();
    let sqrt6_over_pi = 6.0_f64.sqrt() / std::f64::consts::PI;
    let euler_mascheroni = 0.57721566490153286;

    (0..n)
        .into_par_iter()
        .map(|i| {
            let mx = mean_x[i];
            let sx = std_x[i];
            let t = return_period[i];

            if t <= 1.0 || sx < 0.0 || mx.is_nan() || sx.is_nan() || t.is_nan() {
                f64::NAN
            } else {
                let y_t = -( (t / (t - 1.0)).ln() ).ln();
                let k_t = -sqrt6_over_pi * (euler_mascheroni + (-y_t));
                mx + k_t * sx
            }
        })
        .collect()
}

/// Lanczos approximation for Gamma(z)
fn gamma_approx(z: f64) -> f64 {
    if z < 0.5 {
        std::f64::consts::PI / ((std::f64::consts::PI * z).sin() * gamma_approx(1.0 - z))
    } else {
        let z = z - 1.0;
        let c = [
            0.99999999999980993,
            676.5203681218851,
            -1259.1392167224028,
            771.32342877765313,
            -176.61502916214059,
            12.507343278686905,
            -0.13857109526572012,
            9.9843695780195716e-6,
            1.5056327351493116e-7,
        ];
        let mut x = c[0];
        for i in 1..9 {
            x += c[i] / (z + i as f64);
        }
        let t = z + 7.5;
        (2.0 * std::f64::consts::PI).sqrt() * t.powf(z + 0.5) * (-t).exp() * x
    }
}

/// Nash Cascade Instantaneous Unit Hydrograph (IUH):
/// u(t) = (1 / (K * Gamma(n))) * (t / K)^(n - 1) * exp(-t / K)
pub fn nash_cascade_iuh_kernel(
    time: &[f64],
    n_reservoirs: &[f64],
    k_storage: &[f64],
) -> Vec<f64> {
    let n = time.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = time[i];
            let n_res = n_reservoirs[i];
            let k = k_storage[i];

            if t < 0.0 || n_res <= 0.0 || k <= 0.0 || t.is_nan() || n_res.is_nan() || k.is_nan() {
                f64::NAN
            } else if t == 0.0 && n_res < 1.0 {
                f64::NAN
            } else if t == 0.0 && n_res > 1.0 {
                0.0
            } else {
                let gamma_n = gamma_approx(n_res);
                if gamma_n <= 0.0 || gamma_n.is_nan() {
                    f64::NAN
                } else {
                    let factor = 1.0 / (k * gamma_n);
                    let power = (t / k).powf(n_res - 1.0);
                    let exp_term = (-t / k).exp();
                    factor * power * exp_term
                }
            }
        })
        .collect()
}

/// Hargreaves-Samani Reference Crop Evapotranspiration (ET0):
/// ET_0 = 0.0023 * R_a * (T_mean + 17.8) * sqrt(T_max - T_min)
pub fn hargreaves_samani_et0_kernel(
    r_a: &[f64],
    t_mean: &[f64],
    t_max: &[f64],
    t_min: &[f64],
) -> Vec<f64> {
    let n = r_a.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let ra = r_a[i];
            let tmean = t_mean[i];
            let tmax = t_max[i];
            let tmin = t_min[i];

            if ra < 0.0 || tmax < tmin || ra.is_nan() || tmean.is_nan() || tmax.is_nan() || tmin.is_nan() {
                f64::NAN
            } else {
                0.0023 * ra * (tmean + 17.8) * (tmax - tmin).sqrt()
            }
        })
        .collect()
}

/// Net Radiation Equivalent Evaporation:
/// R_n_mm = (R_n_MJ * 1e6) / (rho_w * lambda_latent)
pub fn net_radiation_equivalent_evap_kernel(
    rn_mj: &[f64],
    lambda_latent: &[f64],
    rho_w: f64,
) -> Vec<f64> {
    let n = rn_mj.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let rn = rn_mj[i];
            let lam = lambda_latent[i];

            if lam <= 0.0 || rho_w <= 0.0 || rn.is_nan() || lam.is_nan() {
                f64::NAN
            } else {
                (rn * 1.0e6) / (rho_w * lam)
            }
        })
        .collect()
}

/// Time-Area Runoff Convolution Step:
/// Q_j = sum(I_{excess} * A_k) * k_unit
pub fn time_area_runoff_step_kernel(
    i_excess: &[f64],
    a_k: &[f64],
    k_unit: f64,
) -> f64 {
    let n = i_excess.len().min(a_k.len());
    let sum_prod = (0..n)
        .into_par_iter()
        .map(|i| {
            let ie = i_excess[i];
            let ak = a_k[i];
            if ie < 0.0 || ak < 0.0 || ie.is_nan() || ak.is_nan() {
                0.0
            } else {
                ie * ak
            }
        })
        .sum::<f64>();

    sum_prod * k_unit
}

// ============================================================================
// DEDICATED BIDIRECTIONAL ALGEBRAIC INVERSIONS (APPROACH 1)
// ============================================================================

/// Inversion: Rational runoff coefficient C = Q / (k * i * A)
pub fn rational_c_kernel(
    q: &[f64],
    intensity: &[f64],
    area: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let i_val = intensity[i];
            let a = area[i];
            if q_val < 0.0 || i_val <= 0.0 || a <= 0.0 || k <= 0.0
                || q_val.is_nan() || i_val.is_nan() || a.is_nan() {
                f64::NAN
            } else {
                q_val / (k * i_val * a)
            }
        })
        .collect()
}

/// Inversion: Rational rainfall intensity i = Q / (k * C * A)
pub fn rational_i_kernel(
    q: &[f64],
    c: &[f64],
    area: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let c_val = c[i];
            let a = area[i];
            if q_val < 0.0 || c_val <= 0.0 || a <= 0.0 || k <= 0.0
                || q_val.is_nan() || c_val.is_nan() || a.is_nan() {
                f64::NAN
            } else {
                q_val / (k * c_val * a)
            }
        })
        .collect()
}

/// Inversion: Rational drainage area A = Q / (k * C * i)
pub fn rational_a_kernel(
    q: &[f64],
    c: &[f64],
    intensity: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let c_val = c[i];
            let i_val = intensity[i];
            if q_val < 0.0 || c_val <= 0.0 || i_val <= 0.0 || k <= 0.0
                || q_val.is_nan() || c_val.is_nan() || i_val.is_nan() {
                f64::NAN
            } else {
                q_val / (k * c_val * i_val)
            }
        })
        .collect()
}

/// Inversion: SCS-CN potential retention S = (factor / CN) - offset
pub fn scs_cn_s_kernel(
    cn: &[f64],
    factor: f64,
    offset: f64,
) -> Vec<f64> {
    let n = cn.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let c = cn[i];
            if c <= 0.0 || c > 100.0 || c.is_nan() {
                f64::NAN
            } else {
                (factor / c) - offset
            }
        })
        .collect()
}

/// Inversion: SCS-CN curve number CN = factor / (S + offset)
pub fn scs_cn_cn_kernel(
    s: &[f64],
    factor: f64,
    offset: f64,
) -> Vec<f64> {
    let n = s.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let s_val = s[i];
            if s_val < 0.0 || (s_val + offset) <= 0.0 || s_val.is_nan() {
                f64::NAN
            } else {
                factor / (s_val + offset)
            }
        })
        .collect()
}

/// Inversion: SCS-CN rainfall depth P = lambda * S + 0.5 * (Q + sqrt(Q^2 + 4 * Q * S))
pub fn scs_cn_p_kernel(
    q: &[f64],
    s: &[f64],
    lambda: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let s_val = s[i];
            let lam = lambda[i];
            if q_val < 0.0 || s_val < 0.0 || lam < 0.0 || q_val.is_nan() || s_val.is_nan() || lam.is_nan() {
                f64::NAN
            } else if q_val == 0.0 {
                lam * s_val
            } else {
                let inside = q_val * q_val + 4.0 * q_val * s_val;
                lam * s_val + 0.5 * (q_val + inside.sqrt())
            }
        })
        .collect()
}

/// Inversion: Horton initial infiltration rate f_0 = f_c + (f_p - f_c) * exp(k * t)
pub fn horton_rate_f0_kernel(
    fp: &[f64],
    fc: &[f64],
    k: &[f64],
    t: &[f64],
) -> Vec<f64> {
    let n = fp.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = fp[i];
            let c = fc[i];
            let k_val = k[i];
            let t_val = t[i];
            if p < 0.0 || c < 0.0 || k_val < 0.0 || t_val < 0.0
                || p.is_nan() || c.is_nan() || k_val.is_nan() || t_val.is_nan() {
                f64::NAN
            } else {
                c + (p - c) * (k_val * t_val).exp()
            }
        })
        .collect()
}

/// Inversion: Horton constant infiltration rate f_c = (f_p - f_0 * exp(-k * t)) / (1 - exp(-k * t))
pub fn horton_rate_fc_kernel(
    fp: &[f64],
    f0: &[f64],
    k: &[f64],
    t: &[f64],
) -> Vec<f64> {
    let n = fp.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = fp[i];
            let z = f0[i];
            let k_val = k[i];
            let t_val = t[i];
            if p < 0.0 || z < 0.0 || k_val <= 0.0 || t_val <= 0.0
                || p.is_nan() || z.is_nan() || k_val.is_nan() || t_val.is_nan() {
                f64::NAN
            } else {
                let e = (-k_val * t_val).exp();
                let denom = 1.0 - e;
                if denom.abs() < 1e-12 {
                    f64::NAN
                } else {
                    (p - z * e) / denom
                }
            }
        })
        .collect()
}

/// Inversion: Horton decay constant k = - (1 / t) * ln((f_p - f_c) / (f_0 - f_c))
pub fn horton_rate_k_kernel(
    fp: &[f64],
    f0: &[f64],
    fc: &[f64],
    t: &[f64],
) -> Vec<f64> {
    let n = fp.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let p = fp[i];
            let z = f0[i];
            let c = fc[i];
            let t_val = t[i];
            if p < c || z <= c || t_val <= 0.0
                || p.is_nan() || z.is_nan() || c.is_nan() || t_val.is_nan() {
                f64::NAN
            } else {
                let ratio = (p - c) / (z - c);
                if ratio <= 0.0 {
                    f64::NAN
                } else {
                    -ratio.ln() / t_val
                }
            }
        })
        .collect()
}

/// Inversion: Kirpich slope S = (k * L^0.77 / t_c)^(1 / 0.385)
pub fn kirpich_s_kernel(
    tc: &[f64],
    length: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = tc.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = tc[i];
            let l = length[i];
            if t <= 0.0 || l <= 0.0 || k <= 0.0 || t.is_nan() || l.is_nan() {
                f64::NAN
            } else {
                let ratio = (k * l.powf(0.77)) / t;
                ratio.powf(1.0 / 0.385)
            }
        })
        .collect()
}

/// Inversion: Kirpich length L = (t_c * S^0.385 / k)^(1 / 0.77)
pub fn kirpich_l_kernel(
    tc: &[f64],
    slope: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = tc.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let t = tc[i];
            let s = slope[i];
            if t <= 0.0 || s <= 0.0 || k <= 0.0 || t.is_nan() || s.is_nan() {
                f64::NAN
            } else {
                let ratio = (t * s.powf(0.385)) / k;
                ratio.powf(1.0 / 0.77)
            }
        })
        .collect()
}

/// Inversion: SCS CN_II from dry condition CN_I: CN_II = (10 * CN_I) / (4.2 + 0.058 * CN_I)
pub fn scs_amc_cnii_from_i_kernel(
    cni: &[f64],
) -> Vec<f64> {
    let n = cni.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let c = cni[i];
            if c <= 0.0 || c > 100.0 || c.is_nan() {
                f64::NAN
            } else {
                (10.0 * c) / (4.2 + 0.058 * c)
            }
        })
        .collect()
}

/// Inversion: SCS CN_II from wet condition CN_III: CN_II = (10 * CN_III) / (23.0 - 0.13 * CN_III)
pub fn scs_amc_cnii_from_iii_kernel(
    cniii: &[f64],
) -> Vec<f64> {
    let n = cniii.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let c = cniii[i];
            if c <= 0.0 || c > 100.0 || c.is_nan() {
                f64::NAN
            } else {
                let denom = 23.0 - 0.13 * c;
                if denom <= 0.0 {
                    f64::NAN
                } else {
                    (10.0 * c) / denom
                }
            }
        })
        .collect()
}

/// Inversion: TR-55 shallow concentrated slope S = (V / k)^2
pub fn tr55_shallow_s_kernel(
    v: &[f64],
    k: f64,
) -> Vec<f64> {
    let n = v.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v_val = v[i];
            if v_val < 0.0 || k <= 0.0 || v_val.is_nan() {
                f64::NAN
            } else {
                let ratio = v_val / k;
                ratio * ratio
            }
        })
        .collect()
}

/// Inversion: Hargreaves extraterrestrial radiation R_a = ET_0 / (0.0023 * (T_mean + 17.8) * sqrt(T_max - T_min))
pub fn hargreaves_ra_kernel(
    et0: &[f64],
    t_mean: &[f64],
    t_max: &[f64],
    t_min: &[f64],
) -> Vec<f64> {
    let n = et0.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let et = et0[i];
            let tm = t_mean[i];
            let tmx = t_max[i];
            let tmn = t_min[i];
            let trange = tmx - tmn;
            if et < 0.0 || trange <= 0.0 || (tm + 17.8) <= 0.0
                || et.is_nan() || tm.is_nan() || tmx.is_nan() || tmn.is_nan() {
                f64::NAN
            } else {
                et / (0.0023 * (tm + 17.8) * trange.sqrt())
            }
        })
        .collect()
}

