//! Hydraulic Structures Module
//! High-performance Rayon-parallelized computations for weirs, flumes, orifices, and gates.

use rayon::prelude::*;

/// Francis formula for sharp-crested rectangular weir:
/// Q = k_francis * (L - 0.1 * n_e * H) * H^(3/2)
/// SI: k_francis = 1.84 (L, H in m, Q in m3/s)
/// US: k_francis = 3.33 (L, H in ft, Q in cfs)
pub fn francis_weir_kernel(
    length: &[f64],
    head: &[f64],
    contractions: &[f64],
    k_francis: f64,
) -> Vec<f64> {
    let n = length.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = length[i];
            let h = head[i];
            let ne = contractions[i];

            if l <= 0.0 || h < 0.0 || ne < 0.0 || l.is_nan() || h.is_nan() || ne.is_nan() {
                f64::NAN
            } else {
                let effective_l = l - 0.1 * ne * h;
                if effective_l <= 0.0 {
                    0.0
                } else {
                    k_francis * effective_l * h.powf(1.5)
                }
            }
        })
        .collect()
}

/// Triangular V-notch weir:
/// Q = (8/15) * C_d * sqrt(2 * g) * tan(theta / 2) * H^(5/2)
pub fn v_notch_weir_kernel(
    theta_rad: &[f64],
    head: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = theta_rad.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let theta = theta_rad[i];
            let h = head[i];
            let cd = c_d[i];

            if theta <= 0.0 || h < 0.0 || cd <= 0.0 || g <= 0.0
                || theta.is_nan() || h.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                (8.0 / 15.0) * cd * (2.0 * g).sqrt() * (theta / 2.0).tan() * h.powf(2.5)
            }
        })
        .collect()
}

/// Broad-crested weir:
/// Q = C_d * (2/3)^(3/2) * sqrt(g) * L * H^(3/2)
pub fn broad_crested_weir_kernel(
    length: &[f64],
    head: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = length.len();
    let factor = (2.0 / 3.0_f64).powf(1.5);
    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = length[i];
            let h = head[i];
            let cd = c_d[i];

            if l <= 0.0 || h < 0.0 || cd <= 0.0 || g <= 0.0
                || l.is_nan() || h.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                cd * factor * g.sqrt() * l * h.powf(1.5)
            }
        })
        .collect()
}

/// Parshall flume: Q = C * W * H^n
pub fn parshall_flume_kernel(
    throat_width: &[f64],
    head: &[f64],
    coeff_c: &[f64],
    exp_n: &[f64],
) -> Vec<f64> {
    let n_len = throat_width.len();
    (0..n_len)
        .into_par_iter()
        .map(|i| {
            let w = throat_width[i];
            let h = head[i];
            let c = coeff_c[i];
            let exp = exp_n[i];

            if w <= 0.0 || h < 0.0 || c <= 0.0 || exp <= 0.0
                || w.is_nan() || h.is_nan() || c.is_nan() || exp.is_nan() {
                f64::NAN
            } else {
                c * w * h.powf(exp)
            }
        })
        .collect()
}

/// Free orifice discharge: Q = C_d * A_o * sqrt(2 * g * H)
pub fn orifice_free_kernel(
    area: &[f64],
    head: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = area.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let a = area[i];
            let h = head[i];
            let cd = c_d[i];

            if a <= 0.0 || h < 0.0 || cd <= 0.0 || g <= 0.0
                || a.is_nan() || h.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                cd * a * (2.0 * g * h).sqrt()
            }
        })
        .collect()
}

/// Submerged orifice discharge: Q = C_d * A_o * sqrt(2 * g * (H_1 - H_2))
pub fn orifice_submerged_kernel(
    area: &[f64],
    head_1: &[f64],
    head_2: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = area.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let a = area[i];
            let h1 = head_1[i];
            let h2 = head_2[i];
            let cd = c_d[i];

            if a <= 0.0 || h1 < h2 || cd <= 0.0 || g <= 0.0
                || a.is_nan() || h1.is_nan() || h2.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                cd * a * (2.0 * g * (h1 - h2)).sqrt()
            }
        })
        .collect()
}

/// Sluice gate free discharge: Q = C_d * b * a * sqrt(2 * g * y_1)
pub fn sluice_gate_free_kernel(
    gate_width: &[f64],
    gate_opening: &[f64],
    upstream_depth: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = gate_width.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let b = gate_width[i];
            let a = gate_opening[i];
            let y1 = upstream_depth[i];
            let cd = c_d[i];

            if b <= 0.0 || a <= 0.0 || y1 < 0.0 || cd <= 0.0 || g <= 0.0
                || b.is_nan() || a.is_nan() || y1.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                cd * b * a * (2.0 * g * y1).sqrt()
            }
        })
        .collect()
}

/// Sluice gate submerged discharge: Q = C_s * b * a * sqrt(2 * g * (y_1 - y_2))
pub fn sluice_gate_submerged_kernel(
    gate_width: &[f64],
    gate_opening: &[f64],
    upstream_depth: &[f64],
    tailwater_depth: &[f64],
    c_s: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = gate_width.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let b = gate_width[i];
            let a = gate_opening[i];
            let y1 = upstream_depth[i];
            let y2 = tailwater_depth[i];
            let cs = c_s[i];

            if b <= 0.0 || a <= 0.0 || y1 < y2 || cs <= 0.0 || g <= 0.0
                || b.is_nan() || a.is_nan() || y1.is_nan() || y2.is_nan() || cs.is_nan() {
                f64::NAN
            } else {
                cs * b * a * (2.0 * g * (y1 - y2)).sqrt()
            }
        })
        .collect()
}

// ============================================================================
// EXPANSION FORMULAS: SPILLWAYS, STILLING BASINS & DAM HYDRAULICS
// ============================================================================

/// Ogee spillway discharge: Q = C_o * L_e * H_e^(3/2)
pub fn ogee_spillway_discharge_kernel(
    c_o: &[f64],
    l_e: &[f64],
    h_e: &[f64],
) -> Vec<f64> {
    let n = c_o.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let co = c_o[i];
            let le = l_e[i];
            let he = h_e[i];

            if co <= 0.0 || le <= 0.0 || he < 0.0 || co.is_nan() || le.is_nan() || he.is_nan() {
                f64::NAN
            } else {
                co * le * he.powf(1.5)
            }
        })
        .collect()
}

/// Ogee discharge coefficient variation with actual head:
/// C = C_o * (H_e / H_o)^0.12
pub fn ogee_discharge_coefficient_kernel(
    c_o: &[f64],
    h_e: &[f64],
    h_o: &[f64],
) -> Vec<f64> {
    let n = c_o.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let co = c_o[i];
            let he = h_e[i];
            let ho = h_o[i];

            if co <= 0.0 || he < 0.0 || ho <= 0.0 || co.is_nan() || he.is_nan() || ho.is_nan() {
                f64::NAN
            } else {
                co * (he / ho).powf(0.12)
            }
        })
        .collect()
}

/// Spillway effective crest length accounting for pier and abutment contractions:
/// L_e = L - 2.0 * (N * K_p + K_a) * H_e
pub fn spillway_effective_length_kernel(
    length: &[f64],
    n_piers: &[f64],
    k_p: &[f64],
    k_a: &[f64],
    h_e: &[f64],
) -> Vec<f64> {
    let n = length.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let l = length[i];
            let np = n_piers[i];
            let kp = k_p[i];
            let ka = k_a[i];
            let he = h_e[i];

            if l <= 0.0 || np < 0.0 || kp < 0.0 || ka < 0.0 || he < 0.0
                || l.is_nan() || np.is_nan() || kp.is_nan() || ka.is_nan() || he.is_nan() {
                f64::NAN
            } else {
                let contraction = 2.0 * (np * kp + ka) * he;
                (l - contraction).max(0.0)
            }
        })
        .collect()
}

/// Chute spillway terminal velocity: V = sqrt(2 * g * (Z_drop - H_loss))
pub fn chute_terminal_velocity_kernel(
    z_drop: &[f64],
    h_loss: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = z_drop.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let zd = z_drop[i];
            let hl = h_loss[i];

            if zd < hl || zd < 0.0 || hl < 0.0 || g <= 0.0 || zd.is_nan() || hl.is_nan() {
                f64::NAN
            } else {
                (2.0 * g * (zd - hl)).sqrt()
            }
        })
        .collect()
}

/// Stilling basin length: L_sb = k_basin * y_2
pub fn stilling_basin_length_kernel(
    y_2: &[f64],
    k_basin: &[f64],
) -> Vec<f64> {
    let n = y_2.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y2 = y_2[i];
            let kb = k_basin[i];

            if y2 < 0.0 || kb <= 0.0 || y2.is_nan() || kb.is_nan() {
                f64::NAN
            } else {
                kb * y2
            }
        })
        .collect()
}

/// Morning glory (shaft/drop inlet) circular spillway flow:
/// Q = C * (2 * PI * R) * H^(3/2)
pub fn morning_glory_weir_flow_kernel(
    radius: &[f64],
    head: &[f64],
    c_coeff: &[f64],
) -> Vec<f64> {
    let n = radius.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let r = radius[i];
            let h = head[i];
            let c = c_coeff[i];

            if r <= 0.0 || h < 0.0 || c <= 0.0 || r.is_nan() || h.is_nan() || c.is_nan() {
                f64::NAN
            } else {
                c * (2.0 * std::f64::consts::PI * r) * h.powf(1.5)
            }
        })
        .collect()
}

/// Siphon spillway discharge: Q = C_d * A_throat * sqrt(2 * g * H_operating)
pub fn siphon_spillway_discharge_kernel(
    a_throat: &[f64],
    h_operating: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = a_throat.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let at = a_throat[i];
            let ho = h_operating[i];
            let cd = c_d[i];

            if at <= 0.0 || ho < 0.0 || cd <= 0.0 || g <= 0.0 || at.is_nan() || ho.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                cd * at * (2.0 * g * ho).sqrt()
            }
        })
        .collect()
}

/// Straight drop spillway toe depth (Rand 1955):
/// y_1 = 0.54 * h_d * (q^2 / (g * h_d^3))^0.425
pub fn drop_structure_depth_kernel(
    h_d: &[f64],
    q: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = h_d.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let hd = h_d[i];
            let q_val = q[i];

            if hd <= 0.0 || q_val < 0.0 || g <= 0.0 || hd.is_nan() || q_val.is_nan() {
                f64::NAN
            } else {
                let drop_num = (q_val * q_val) / (g * hd.powi(3));
                0.54 * hd * drop_num.powf(0.425)
            }
        })
        .collect()
}

/// Tailwater rating curve stage: y_tw = a * Q^b + z_0
pub fn tailwater_depth_kernel(
    discharge: &[f64],
    a_coeff: &[f64],
    b_exp: &[f64],
    z_0: &[f64],
) -> Vec<f64> {
    let n = discharge.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q = discharge[i];
            let a = a_coeff[i];
            let b = b_exp[i];
            let z0 = z_0[i];

            if q < 0.0 || a <= 0.0 || b <= 0.0 || q.is_nan() || a.is_nan() || b.is_nan() || z0.is_nan() {
                f64::NAN
            } else {
                a * q.powf(b) + z0
            }
        })
        .collect()
}

// ============================================================================
// DEDICATED BIDIRECTIONAL ALGEBRAIC INVERSIONS (APPROACH 1)
// ============================================================================

/// Inversion: Francis weir crest length L = Q / (k * H^1.5) + 0.1 * n_e * H
pub fn francis_weir_l_kernel(
    q: &[f64],
    head: &[f64],
    contractions: &[f64],
    k_francis: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let h = head[i];
            let ne = contractions[i];
            if q_val < 0.0 || h <= 0.0 || ne < 0.0 || k_francis <= 0.0
                || q_val.is_nan() || h.is_nan() || ne.is_nan() {
                f64::NAN
            } else {
                (q_val / (k_francis * h.powf(1.5))) + (0.1 * ne * h)
            }
        })
        .collect()
}

/// Inversion: V-notch weir head H = (Q / ((8/15) * C_d * sqrt(2*g) * tan(theta/2)))^(2/5)
pub fn v_notch_weir_h_kernel(
    q: &[f64],
    theta_rad: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let theta = theta_rad[i];
            let cd = c_d[i];
            if q_val < 0.0 || theta <= 0.0 || cd <= 0.0 || g <= 0.0
                || q_val.is_nan() || theta.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                let factor = (8.0 / 15.0) * cd * (2.0 * g).sqrt() * (theta / 2.0).tan();
                if factor <= 0.0 {
                    f64::NAN
                } else {
                    (q_val / factor).powf(0.4)
                }
            }
        })
        .collect()
}

/// Inversion: V-notch weir coefficient C_d = Q / ((8/15) * sqrt(2*g) * tan(theta/2) * H^(5/2))
pub fn v_notch_weir_cd_kernel(
    q: &[f64],
    theta_rad: &[f64],
    head: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let theta = theta_rad[i];
            let h = head[i];
            if q_val < 0.0 || theta <= 0.0 || h <= 0.0 || g <= 0.0
                || q_val.is_nan() || theta.is_nan() || h.is_nan() {
                f64::NAN
            } else {
                let denom = (8.0 / 15.0) * (2.0 * g).sqrt() * (theta / 2.0).tan() * h.powf(2.5);
                if denom <= 0.0 {
                    f64::NAN
                } else {
                    q_val / denom
                }
            }
        })
        .collect()
}

/// Inversion: V-notch weir angle theta = 2 * arctan(Q / ((8/15) * C_d * sqrt(2*g) * H^(5/2)))
pub fn v_notch_weir_theta_kernel(
    q: &[f64],
    head: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let h = head[i];
            let cd = c_d[i];
            if q_val < 0.0 || h <= 0.0 || cd <= 0.0 || g <= 0.0
                || q_val.is_nan() || h.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                let denom = (8.0 / 15.0) * cd * (2.0 * g).sqrt() * h.powf(2.5);
                if denom <= 0.0 {
                    f64::NAN
                } else {
                    2.0 * (q_val / denom).atan()
                }
            }
        })
        .collect()
}

/// Inversion: Broad-crested weir head H = (Q / (C_d * b * sqrt(g) * (2/3)^1.5))^(2/3)
pub fn broad_crested_weir_h_kernel(
    q: &[f64],
    length: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let b = length[i];
            let cd = c_d[i];
            if q_val < 0.0 || b <= 0.0 || cd <= 0.0 || g <= 0.0
                || q_val.is_nan() || b.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                let factor = cd * b * g.sqrt() * (2.0 / 3.0_f64).powf(1.5);
                if factor <= 0.0 {
                    f64::NAN
                } else {
                    (q_val / factor).powf(2.0 / 3.0)
                }
            }
        })
        .collect()
}

/// Inversion: Broad-crested weir crest width b = Q / (C_d * sqrt(g) * (2/3)^1.5 * H^1.5)
pub fn broad_crested_weir_l_kernel(
    q: &[f64],
    head: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let h = head[i];
            let cd = c_d[i];
            if q_val < 0.0 || h <= 0.0 || cd <= 0.0 || g <= 0.0
                || q_val.is_nan() || h.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                let factor = cd * g.sqrt() * (2.0 / 3.0_f64).powf(1.5) * h.powf(1.5);
                if factor <= 0.0 {
                    f64::NAN
                } else {
                    q_val / factor
                }
            }
        })
        .collect()
}

/// Inversion: Orifice free head H = (1 / (2 * g)) * (Q / (C_d * A_o))^2
pub fn orifice_free_h_kernel(
    q: &[f64],
    area: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let ao = area[i];
            let cd = c_d[i];
            if q_val < 0.0 || ao <= 0.0 || cd <= 0.0 || g <= 0.0
                || q_val.is_nan() || ao.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                let ratio = q_val / (cd * ao);
                (ratio * ratio) / (2.0 * g)
            }
        })
        .collect()
}

/// Inversion: Orifice area A_o = Q / (C_d * sqrt(2 * g * H))
pub fn orifice_free_ao_kernel(
    q: &[f64],
    head: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let h = head[i];
            let cd = c_d[i];
            if q_val < 0.0 || h <= 0.0 || cd <= 0.0 || g <= 0.0
                || q_val.is_nan() || h.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                q_val / (cd * (2.0 * g * h).sqrt())
            }
        })
        .collect()
}

/// Inversion: Sluice gate opening a = Q / (C_d * b * sqrt(2 * g * y_1))
pub fn sluice_gate_free_a_kernel(
    q: &[f64],
    b: &[f64],
    y1: &[f64],
    c_d: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let b_val = b[i];
            let y = y1[i];
            let cd = c_d[i];
            if q_val < 0.0 || b_val <= 0.0 || y <= 0.0 || cd <= 0.0 || g <= 0.0
                || q_val.is_nan() || b_val.is_nan() || y.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                q_val / (cd * b_val * (2.0 * g * y).sqrt())
            }
        })
        .collect()
}

/// Inversion: Ogee spillway head H_e = (Q / (C_d * L_e))^(2/3)
pub fn ogee_spillway_he_kernel(
    q: &[f64],
    length: &[f64],
    c_d: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let le = length[i];
            let cd = c_d[i];
            if q_val < 0.0 || le <= 0.0 || cd <= 0.0
                || q_val.is_nan() || le.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                (q_val / (cd * le)).powf(2.0 / 3.0)
            }
        })
        .collect()
}

/// Inversion: Ogee spillway effective length L_e = Q / (C_d * H_e^1.5)
pub fn ogee_spillway_le_kernel(
    q: &[f64],
    he: &[f64],
    c_d: &[f64],
) -> Vec<f64> {
    let n = q.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let q_val = q[i];
            let h = he[i];
            let cd = c_d[i];
            if q_val < 0.0 || h <= 0.0 || cd <= 0.0
                || q_val.is_nan() || h.is_nan() || cd.is_nan() {
                f64::NAN
            } else {
                q_val / (cd * h.powf(1.5))
            }
        })
        .collect()
}

/// Inversion: Chute spillway drop elevation Z = Z_0 - (V^2 - V_0^2) / (2 * g)
pub fn chute_velocity_z_kernel(
    v: &[f64],
    v0: &[f64],
    z0: &[f64],
    g: f64,
) -> Vec<f64> {
    let n = v.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let v_val = v[i];
            let v0_val = v0[i];
            let z0_val = z0[i];
            if v_val < v0_val || v0_val < 0.0 || g <= 0.0
                || v_val.is_nan() || v0_val.is_nan() || z0_val.is_nan() {
                f64::NAN
            } else {
                z0_val - (v_val * v_val - v0_val * v0_val) / (2.0 * g)
            }
        })
        .collect()
}

/// Inversion: Stilling basin sequent depth y_2 = 0.5 * y_1 * (sqrt(1 + 8 * Fr_1^2) - 1)
pub fn stilling_basin_y2_kernel(
    y1: &[f64],
    fr1: &[f64],
) -> Vec<f64> {
    let n = y1.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y = y1[i];
            let fr = fr1[i];
            if y <= 0.0 || fr <= 1.0 || y.is_nan() || fr.is_nan() {
                f64::NAN
            } else {
                0.5 * y * ((1.0 + 8.0 * fr * fr).sqrt() - 1.0)
            }
        })
        .collect()
}

/// Inversion: Stilling basin initial depth y_1 = y_2 / (0.5 * (sqrt(1 + 8 * Fr_1^2) - 1))
pub fn stilling_basin_y1_kernel(
    y2: &[f64],
    fr1: &[f64],
) -> Vec<f64> {
    let n = y2.len();
    (0..n)
        .into_par_iter()
        .map(|i| {
            let y = y2[i];
            let fr = fr1[i];
            if y <= 0.0 || fr <= 1.0 || y.is_nan() || fr.is_nan() {
                f64::NAN
            } else {
                let factor = 0.5 * ((1.0 + 8.0 * fr * fr).sqrt() - 1.0);
                y / factor
            }
        })
        .collect()
}

