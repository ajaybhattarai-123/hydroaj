//! HydroCivil - Core Computational Engine Python Extension
//! Exposes parallelized, memory-safe water resources engineering routines
//! built in Rust with Rayon, ndarray, and PyO3.

pub mod open_channel;
pub mod pipe_flow;
pub mod hydrology;
pub mod structures;
pub mod groundwater;
pub mod solvers;

use pyo3::prelude::*;
use numpy::{IntoPyArray, PyArray1, PyReadonlyArray1};

// ============================================================================
// PILLAR 1: OPEN CHANNEL HYDRAULICS
// ============================================================================

#[pyfunction]
fn manning_discharge<'py>(
    py: Python<'py>,
    area: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    roughness: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let a_s = area.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let n_s = roughness.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::manning_discharge_kernel(a_s, rh_s, s_s, n_s, k)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn manning_velocity<'py>(
    py: Python<'py>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    roughness: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let n_s = roughness.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::manning_velocity_kernel(rh_s, s_s, n_s, k)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn strickler_velocity<'py>(
    py: Python<'py>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    k_st: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let k_s = k_st.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::strickler_velocity_kernel(rh_s, s_s, k_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn chezy_velocity<'py>(
    py: Python<'py>,
    c: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let c_s = c.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::chezy_velocity_kernel(c_s, rh_s, s_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn kutter_chezy_c<'py>(
    py: Python<'py>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    roughness: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let n_s = roughness.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::kutter_chezy_c_kernel(rh_s, s_s, n_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn bazin_chezy_c<'py>(
    py: Python<'py>,
    r_h: PyReadonlyArray1<'py, f64>,
    gamma: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let rh_s = r_h.as_slice().unwrap();
    let g_s = gamma.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::bazin_chezy_c_kernel(rh_s, g_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn geom_rectangular<'py>(
    py: Python<'py>,
    b: PyReadonlyArray1<'py, f64>,
    y: PyReadonlyArray1<'py, f64>,
) -> (
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
) {
    let b_s = b.as_slice().unwrap();
    let y_s = y.as_slice().unwrap();

    let (a, p, rh, t, d, yb) = py.allow_threads(|| {
        open_channel::geom_rectangular_kernel(b_s, y_s)
    });
    (
        a.into_pyarray(py),
        p.into_pyarray(py),
        rh.into_pyarray(py),
        t.into_pyarray(py),
        d.into_pyarray(py),
        yb.into_pyarray(py),
    )
}

#[pyfunction]
fn geom_trapezoidal<'py>(
    py: Python<'py>,
    b: PyReadonlyArray1<'py, f64>,
    m: PyReadonlyArray1<'py, f64>,
    y: PyReadonlyArray1<'py, f64>,
) -> (
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
) {
    let b_s = b.as_slice().unwrap();
    let m_s = m.as_slice().unwrap();
    let y_s = y.as_slice().unwrap();

    let (a, p, rh, t, d, yb) = py.allow_threads(|| {
        open_channel::geom_trapezoidal_kernel(b_s, m_s, y_s)
    });
    (
        a.into_pyarray(py),
        p.into_pyarray(py),
        rh.into_pyarray(py),
        t.into_pyarray(py),
        d.into_pyarray(py),
        yb.into_pyarray(py),
    )
}

#[pyfunction]
fn geom_triangular<'py>(
    py: Python<'py>,
    m: PyReadonlyArray1<'py, f64>,
    y: PyReadonlyArray1<'py, f64>,
) -> (
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
) {
    let m_s = m.as_slice().unwrap();
    let y_s = y.as_slice().unwrap();

    let (a, p, rh, t, d, yb) = py.allow_threads(|| {
        open_channel::geom_triangular_kernel(m_s, y_s)
    });
    (
        a.into_pyarray(py),
        p.into_pyarray(py),
        rh.into_pyarray(py),
        t.into_pyarray(py),
        d.into_pyarray(py),
        yb.into_pyarray(py),
    )
}

#[pyfunction]
fn geom_circular<'py>(
    py: Python<'py>,
    d: PyReadonlyArray1<'py, f64>,
    y: PyReadonlyArray1<'py, f64>,
) -> (
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
) {
    let d_s = d.as_slice().unwrap();
    let y_s = y.as_slice().unwrap();

    let (a, p, rh, t, hyd) = py.allow_threads(|| {
        open_channel::geom_circular_kernel(d_s, y_s)
    });
    (
        a.into_pyarray(py),
        p.into_pyarray(py),
        rh.into_pyarray(py),
        t.into_pyarray(py),
        hyd.into_pyarray(py),
    )
}

#[pyfunction]
fn geom_parabolic<'py>(
    py: Python<'py>,
    t: PyReadonlyArray1<'py, f64>,
    y: PyReadonlyArray1<'py, f64>,
) -> (
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
    &'py PyArray1<f64>,
) {
    let t_s = t.as_slice().unwrap();
    let y_s = y.as_slice().unwrap();

    let (a, p, rh, hyd, yb) = py.allow_threads(|| {
        open_channel::geom_parabolic_kernel(t_s, y_s)
    });
    (
        a.into_pyarray(py),
        p.into_pyarray(py),
        rh.into_pyarray(py),
        hyd.into_pyarray(py),
        yb.into_pyarray(py),
    )
}

#[pyfunction]
fn specific_energy<'py>(
    py: Python<'py>,
    y: PyReadonlyArray1<'py, f64>,
    q: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let y_s = y.as_slice().unwrap();
    let q_s = q.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::specific_energy_kernel(y_s, q_s, a_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn froude_number<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    top_w: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let t_s = top_w.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::froude_number_kernel(q_s, a_s, t_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn specific_force<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    y_bar: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let yb_s = y_bar.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::specific_force_kernel(q_s, a_s, yb_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_depth_rectangular<'py>(
    py: Python<'py>,
    unit_q: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = unit_q.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::critical_depth_rectangular_kernel(q_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn normal_depth_trapezoidal<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    b: PyReadonlyArray1<'py, f64>,
    m: PyReadonlyArray1<'py, f64>,
    s0: PyReadonlyArray1<'py, f64>,
    roughness: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let b_s = b.as_slice().unwrap();
    let m_s = m.as_slice().unwrap();
    let s_s = s0.as_slice().unwrap();
    let n_s = roughness.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::normal_depth_trapezoidal_kernel(q_s, b_s, m_s, s_s, n_s, k)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn belanger_conjugate_depth<'py>(
    py: Python<'py>,
    y1: PyReadonlyArray1<'py, f64>,
    fr1: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y_s = y1.as_slice().unwrap();
    let fr_s = fr1.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::belanger_conjugate_depth_kernel(y_s, fr_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn hydraulic_jump_head_loss<'py>(
    py: Python<'py>,
    y1: PyReadonlyArray1<'py, f64>,
    y2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y1_s = y1.as_slice().unwrap();
    let y2_s = y2.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::hydraulic_jump_head_loss_kernel(y1_s, y2_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn hydraulic_jump_length<'py>(
    py: Python<'py>,
    y1: PyReadonlyArray1<'py, f64>,
    y2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y1_s = y1.as_slice().unwrap();
    let y2_s = y2.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::hydraulic_jump_length_kernel(y1_s, y2_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn gvf_gradient<'py>(
    py: Python<'py>,
    s0: PyReadonlyArray1<'py, f64>,
    sf: PyReadonlyArray1<'py, f64>,
    fr: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let s0_s = s0.as_slice().unwrap();
    let sf_s = sf.as_slice().unwrap();
    let fr_s = fr.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::gvf_gradient_kernel(s0_s, sf_s, fr_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn manning_friction_slope<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    roughness: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let n_s = roughness.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::manning_friction_slope_kernel(q_s, n_s, a_s, rh_s, k)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn direct_step<'py>(
    py: Python<'py>,
    e1: PyReadonlyArray1<'py, f64>,
    e2: PyReadonlyArray1<'py, f64>,
    s0: PyReadonlyArray1<'py, f64>,
    sf1: PyReadonlyArray1<'py, f64>,
    sf2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let e1_s = e1.as_slice().unwrap();
    let e2_s = e2.as_slice().unwrap();
    let s0_s = s0.as_slice().unwrap();
    let sf1_s = sf1.as_slice().unwrap();
    let sf2_s = sf2.as_slice().unwrap();

    let res = py.allow_threads(|| {
        open_channel::direct_step_kernel(e1_s, e2_s, s0_s, sf1_s, sf2_s)
    });
    res.into_pyarray(py)
}

// ============================================================================
// PILLAR 2: PRESSURIZED PIPE FLOW & HYDRODYNAMICS
// ============================================================================

#[pyfunction]
fn darcy_weisbach<'py>(
    py: Python<'py>,
    f: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let f_s = f.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::darcy_weisbach_kernel(f_s, l_s, d_s, v_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn reynolds_number<'py>(
    py: Python<'py>,
    velocity: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    kinematic_viscosity: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let v_s = velocity.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let nu_s = kinematic_viscosity.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::reynolds_number_kernel(v_s, d_s, nu_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn laminar_friction<'py>(
    py: Python<'py>,
    reynolds: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let re_s = reynolds.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::laminar_friction_kernel(re_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn colebrook_white<'py>(
    py: Python<'py>,
    eps_over_d: PyReadonlyArray1<'py, f64>,
    reynolds: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let ed_s = eps_over_d.as_slice().unwrap();
    let re_s = reynolds.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::colebrook_white_kernel(ed_s, re_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn swamee_jain<'py>(
    py: Python<'py>,
    eps_over_d: PyReadonlyArray1<'py, f64>,
    reynolds: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let ed_s = eps_over_d.as_slice().unwrap();
    let re_s = reynolds.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::swamee_jain_kernel(ed_s, re_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn haaland<'py>(
    py: Python<'py>,
    eps_over_d: PyReadonlyArray1<'py, f64>,
    reynolds: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let ed_s = eps_over_d.as_slice().unwrap();
    let re_s = reynolds.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::haaland_kernel(ed_s, re_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn churchill<'py>(
    py: Python<'py>,
    eps_over_d: PyReadonlyArray1<'py, f64>,
    reynolds: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let ed_s = eps_over_d.as_slice().unwrap();
    let re_s = reynolds.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::churchill_kernel(ed_s, re_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn wood<'py>(
    py: Python<'py>,
    eps_over_d: PyReadonlyArray1<'py, f64>,
    reynolds: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let ed_s = eps_over_d.as_slice().unwrap();
    let re_s = reynolds.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::wood_kernel(ed_s, re_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn hazen_williams<'py>(
    py: Python<'py>,
    length: PyReadonlyArray1<'py, f64>,
    discharge: PyReadonlyArray1<'py, f64>,
    c_coeff: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    k_hw: f64,
) -> &'py PyArray1<f64> {
    let l_s = length.as_slice().unwrap();
    let q_s = discharge.as_slice().unwrap();
    let c_s = c_coeff.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::hazen_williams_kernel(l_s, q_s, c_s, d_s, k_hw)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn hazen_williams_velocity<'py>(
    py: Python<'py>,
    c_coeff: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    k_v: f64,
) -> &'py PyArray1<f64> {
    let c_s = c_coeff.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::hazen_williams_velocity_kernel(c_s, rh_s, s_s, k_v)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn minor_loss<'py>(
    py: Python<'py>,
    k_l: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let k_s = k_l.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::minor_loss_kernel(k_s, v_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn wave_celerity<'py>(
    py: Python<'py>,
    bulk_modulus: PyReadonlyArray1<'py, f64>,
    density: PyReadonlyArray1<'py, f64>,
    elastic_modulus: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    wall_thickness: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let k_s = bulk_modulus.as_slice().unwrap();
    let rho_s = density.as_slice().unwrap();
    let e_s = elastic_modulus.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let t_s = wall_thickness.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::wave_celerity_kernel(k_s, rho_s, e_s, d_s, t_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn joukowsky<'py>(
    py: Python<'py>,
    celerity: PyReadonlyArray1<'py, f64>,
    delta_v: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let a_s = celerity.as_slice().unwrap();
    let dv_s = delta_v.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::joukowsky_kernel(a_s, dv_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_closure_time<'py>(
    py: Python<'py>,
    length: PyReadonlyArray1<'py, f64>,
    celerity: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let l_s = length.as_slice().unwrap();
    let a_s = celerity.as_slice().unwrap();

    let res = py.allow_threads(|| {
        pipe_flow::critical_closure_time_kernel(l_s, a_s)
    });
    res.into_pyarray(py)
}

// ============================================================================
// PILLAR 3: SURFACE WATER HYDROLOGY & RUNOFF
// ============================================================================

#[pyfunction]
fn idf_sherman<'py>(
    py: Python<'py>,
    t_d: PyReadonlyArray1<'py, f64>,
    a: PyReadonlyArray1<'py, f64>,
    b: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let td_s = t_d.as_slice().unwrap();
    let a_s = a.as_slice().unwrap();
    let b_s = b.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::idf_sherman_kernel(td_s, a_s, b_s, c_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn thiessen_areal<'py>(
    py: Python<'py>,
    weights: PyReadonlyArray1<'py, f64>,
    precip: PyReadonlyArray1<'py, f64>,
) -> f64 {
    let w_s = weights.as_slice().unwrap();
    let p_s = precip.as_slice().unwrap();

    py.allow_threads(|| {
        hydrology::thiessen_areal_kernel(w_s, p_s)
    })
}

#[pyfunction]
fn horton_rate<'py>(
    py: Python<'py>,
    time: PyReadonlyArray1<'py, f64>,
    f0: PyReadonlyArray1<'py, f64>,
    fc: PyReadonlyArray1<'py, f64>,
    k: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = time.as_slice().unwrap();
    let f0_s = f0.as_slice().unwrap();
    let fc_s = fc.as_slice().unwrap();
    let k_s = k.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::horton_rate_kernel(t_s, f0_s, fc_s, k_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn horton_cumulative<'py>(
    py: Python<'py>,
    time: PyReadonlyArray1<'py, f64>,
    f0: PyReadonlyArray1<'py, f64>,
    fc: PyReadonlyArray1<'py, f64>,
    k: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = time.as_slice().unwrap();
    let f0_s = f0.as_slice().unwrap();
    let fc_s = fc.as_slice().unwrap();
    let k_s = k.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::horton_cumulative_kernel(t_s, f0_s, fc_s, k_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn green_ampt_rate<'py>(
    py: Python<'py>,
    k_s: PyReadonlyArray1<'py, f64>,
    psi: PyReadonlyArray1<'py, f64>,
    delta_theta: PyReadonlyArray1<'py, f64>,
    f_cum: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let ks_s = k_s.as_slice().unwrap();
    let p_s = psi.as_slice().unwrap();
    let dt_s = delta_theta.as_slice().unwrap();
    let f_s = f_cum.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::green_ampt_rate_kernel(ks_s, p_s, dt_s, f_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn scs_retention<'py>(
    py: Python<'py>,
    cn: PyReadonlyArray1<'py, f64>,
    k_s: f64,
    s_sub: f64,
) -> &'py PyArray1<f64> {
    let cn_s = cn.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::scs_retention_kernel(cn_s, k_s, s_sub)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn scs_runoff_depth<'py>(
    py: Python<'py>,
    precip: PyReadonlyArray1<'py, f64>,
    retention: PyReadonlyArray1<'py, f64>,
    lambda_ratio: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let p_s = precip.as_slice().unwrap();
    let s_s = retention.as_slice().unwrap();
    let lam_s = lambda_ratio.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::scs_runoff_depth_kernel(p_s, s_s, lam_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn rational_peak_flow<'py>(
    py: Python<'py>,
    c: PyReadonlyArray1<'py, f64>,
    intensity: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    k_factor: f64,
) -> &'py PyArray1<f64> {
    let c_s = c.as_slice().unwrap();
    let i_s = intensity.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::rational_peak_flow_kernel(c_s, i_s, a_s, k_factor)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn kirpich_tc<'py>(
    py: Python<'py>,
    length: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    k_kirpich: f64,
) -> &'py PyArray1<f64> {
    let l_s = length.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::kirpich_tc_kernel(l_s, s_s, k_kirpich)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn snyder<'py>(
    py: Python<'py>,
    length: PyReadonlyArray1<'py, f64>,
    length_centroid: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    c_t: PyReadonlyArray1<'py, f64>,
    c_p: PyReadonlyArray1<'py, f64>,
    k_snyder: f64,
) -> (&'py PyArray1<f64>, &'py PyArray1<f64>) {
    let l_s = length.as_slice().unwrap();
    let lc_s = length_centroid.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let ct_s = c_t.as_slice().unwrap();
    let cp_s = c_p.as_slice().unwrap();

    let (lag, peak) = py.allow_threads(|| {
        hydrology::snyder_kernel(l_s, lc_s, a_s, ct_s, cp_s, k_snyder)
    });
    (lag.into_pyarray(py), peak.into_pyarray(py))
}

#[pyfunction]
fn scs_peak_flow<'py>(
    py: Python<'py>,
    area: PyReadonlyArray1<'py, f64>,
    time_to_peak: PyReadonlyArray1<'py, f64>,
    k_scs: f64,
) -> &'py PyArray1<f64> {
    let a_s = area.as_slice().unwrap();
    let tp_s = time_to_peak.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::scs_peak_flow_kernel(a_s, tp_s, k_scs)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn muskingum_coefficients<'py>(
    py: Python<'py>,
    k: PyReadonlyArray1<'py, f64>,
    x: PyReadonlyArray1<'py, f64>,
    dt: PyReadonlyArray1<'py, f64>,
) -> (&'py PyArray1<f64>, &'py PyArray1<f64>, &'py PyArray1<f64>) {
    let k_s = k.as_slice().unwrap();
    let x_s = x.as_slice().unwrap();
    let dt_s = dt.as_slice().unwrap();

    let (c0, c1, c2) = py.allow_threads(|| {
        hydrology::muskingum_coefficients_kernel(k_s, x_s, dt_s)
    });
    (c0.into_pyarray(py), c1.into_pyarray(py), c2.into_pyarray(py))
}

#[pyfunction]
fn muskingum_route<'py>(
    py: Python<'py>,
    inflow: PyReadonlyArray1<'py, f64>,
    k: f64,
    x: f64,
    dt: f64,
    initial_outflow: f64,
) -> &'py PyArray1<f64> {
    let inf_s = inflow.as_slice().unwrap();

    let res = py.allow_threads(|| {
        hydrology::muskingum_route_kernel(inf_s, k, x, dt, initial_outflow)
    });
    res.into_pyarray(py)
}

// ============================================================================
// PILLAR 4: HYDRAULIC STRUCTURES & GROUNDWATER
// ============================================================================

#[pyfunction]
fn francis_weir<'py>(
    py: Python<'py>,
    length: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    contractions: PyReadonlyArray1<'py, f64>,
    k_francis: f64,
) -> &'py PyArray1<f64> {
    let l_s = length.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let ne_s = contractions.as_slice().unwrap();

    let res = py.allow_threads(|| {
        structures::francis_weir_kernel(l_s, h_s, ne_s, k_francis)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn v_notch_weir<'py>(
    py: Python<'py>,
    theta_rad: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let t_s = theta_rad.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();

    let res = py.allow_threads(|| {
        structures::v_notch_weir_kernel(t_s, h_s, cd_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn broad_crested_weir<'py>(
    py: Python<'py>,
    length: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let l_s = length.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();

    let res = py.allow_threads(|| {
        structures::broad_crested_weir_kernel(l_s, h_s, cd_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn parshall_flume<'py>(
    py: Python<'py>,
    throat_width: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    coeff_c: PyReadonlyArray1<'py, f64>,
    exp_n: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let w_s = throat_width.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let c_s = coeff_c.as_slice().unwrap();
    let e_s = exp_n.as_slice().unwrap();

    let res = py.allow_threads(|| {
        structures::parshall_flume_kernel(w_s, h_s, c_s, e_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn orifice_free<'py>(
    py: Python<'py>,
    area: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let a_s = area.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();

    let res = py.allow_threads(|| {
        structures::orifice_free_kernel(a_s, h_s, cd_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn orifice_submerged<'py>(
    py: Python<'py>,
    area: PyReadonlyArray1<'py, f64>,
    head_1: PyReadonlyArray1<'py, f64>,
    head_2: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let a_s = area.as_slice().unwrap();
    let h1_s = head_1.as_slice().unwrap();
    let h2_s = head_2.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();

    let res = py.allow_threads(|| {
        structures::orifice_submerged_kernel(a_s, h1_s, h2_s, cd_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn sluice_gate_free<'py>(
    py: Python<'py>,
    gate_width: PyReadonlyArray1<'py, f64>,
    gate_opening: PyReadonlyArray1<'py, f64>,
    upstream_depth: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let b_s = gate_width.as_slice().unwrap();
    let a_s = gate_opening.as_slice().unwrap();
    let y1_s = upstream_depth.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();

    let res = py.allow_threads(|| {
        structures::sluice_gate_free_kernel(b_s, a_s, y1_s, cd_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn sluice_gate_submerged<'py>(
    py: Python<'py>,
    gate_width: PyReadonlyArray1<'py, f64>,
    gate_opening: PyReadonlyArray1<'py, f64>,
    upstream_depth: PyReadonlyArray1<'py, f64>,
    tailwater_depth: PyReadonlyArray1<'py, f64>,
    c_s: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let b_s = gate_width.as_slice().unwrap();
    let a_s = gate_opening.as_slice().unwrap();
    let y1_s = upstream_depth.as_slice().unwrap();
    let y2_s = tailwater_depth.as_slice().unwrap();
    let cs_s = c_s.as_slice().unwrap();

    let res = py.allow_threads(|| {
        structures::sluice_gate_submerged_kernel(b_s, a_s, y1_s, y2_s, cs_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn darcy_flow_1d<'py>(
    py: Python<'py>,
    k: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    dh_dl: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let k_s = k.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let grad_s = dh_dl.as_slice().unwrap();

    let res = py.allow_threads(|| {
        groundwater::darcy_flow_1d_kernel(k_s, a_s, grad_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn darcy_flux<'py>(
    py: Python<'py>,
    k: PyReadonlyArray1<'py, f64>,
    dh_dl: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let k_s = k.as_slice().unwrap();
    let grad_s = dh_dl.as_slice().unwrap();

    let res = py.allow_threads(|| {
        groundwater::darcy_flux_kernel(k_s, grad_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn thiem_confined<'py>(
    py: Python<'py>,
    transmissivity: PyReadonlyArray1<'py, f64>,
    h1: PyReadonlyArray1<'py, f64>,
    h2: PyReadonlyArray1<'py, f64>,
    r1: PyReadonlyArray1<'py, f64>,
    r2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = transmissivity.as_slice().unwrap();
    let h1_s = h1.as_slice().unwrap();
    let h2_s = h2.as_slice().unwrap();
    let r1_s = r1.as_slice().unwrap();
    let r2_s = r2.as_slice().unwrap();

    let res = py.allow_threads(|| {
        groundwater::thiem_confined_kernel(t_s, h1_s, h2_s, r1_s, r2_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn thiem_unconfined<'py>(
    py: Python<'py>,
    conductivity: PyReadonlyArray1<'py, f64>,
    h1: PyReadonlyArray1<'py, f64>,
    h2: PyReadonlyArray1<'py, f64>,
    r1: PyReadonlyArray1<'py, f64>,
    r2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let k_s = conductivity.as_slice().unwrap();
    let h1_s = h1.as_slice().unwrap();
    let h2_s = h2.as_slice().unwrap();
    let r1_s = r1.as_slice().unwrap();
    let r2_s = r2.as_slice().unwrap();

    let res = py.allow_threads(|| {
        groundwater::thiem_unconfined_kernel(k_s, h1_s, h2_s, r1_s, r2_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn theis_drawdown<'py>(
    py: Python<'py>,
    pumping_rate: PyReadonlyArray1<'py, f64>,
    transmissivity: PyReadonlyArray1<'py, f64>,
    storativity: PyReadonlyArray1<'py, f64>,
    radius: PyReadonlyArray1<'py, f64>,
    time: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = pumping_rate.as_slice().unwrap();
    let t_s = transmissivity.as_slice().unwrap();
    let s_s = storativity.as_slice().unwrap();
    let r_s = radius.as_slice().unwrap();
    let time_s = time.as_slice().unwrap();

    let res = py.allow_threads(|| {
        groundwater::theis_drawdown_kernel(q_s, t_s, s_s, r_s, time_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn cooper_jacob_drawdown<'py>(
    py: Python<'py>,
    pumping_rate: PyReadonlyArray1<'py, f64>,
    transmissivity: PyReadonlyArray1<'py, f64>,
    storativity: PyReadonlyArray1<'py, f64>,
    radius: PyReadonlyArray1<'py, f64>,
    time: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = pumping_rate.as_slice().unwrap();
    let t_s = transmissivity.as_slice().unwrap();
    let s_s = storativity.as_slice().unwrap();
    let r_s = radius.as_slice().unwrap();
    let time_s = time.as_slice().unwrap();

    let res = py.allow_threads(|| {
        groundwater::cooper_jacob_drawdown_kernel(q_s, t_s, s_s, r_s, time_s)
    });
    res.into_pyarray(py)
}


// ============================================================================
// EXPANSIONS: OPEN CHANNEL & SEDIMENT
// ============================================================================

#[pyfunction]
fn optimal_rectangular_section<'py>(
    py: Python<'py>,
    y: PyReadonlyArray1<'py, f64>,
) -> (&'py PyArray1<f64>, &'py PyArray1<f64>, &'py PyArray1<f64>, &'py PyArray1<f64>) {
    let y_s = y.as_slice().unwrap();
    let (b, a, p, rh) = py.allow_threads(|| {
        open_channel::optimal_rectangular_section_kernel(y_s)
    });
    (b.into_pyarray(py), a.into_pyarray(py), p.into_pyarray(py), rh.into_pyarray(py))
}

#[pyfunction]
fn optimal_trapezoidal_section<'py>(
    py: Python<'py>,
    y: PyReadonlyArray1<'py, f64>,
) -> (&'py PyArray1<f64>, &'py PyArray1<f64>, &'py PyArray1<f64>) {
    let y_s = y.as_slice().unwrap();
    let (b, m, rh) = py.allow_threads(|| {
        open_channel::optimal_trapezoidal_section_kernel(y_s)
    });
    (b.into_pyarray(py), m.into_pyarray(py), rh.into_pyarray(py))
}

#[pyfunction]
fn optimal_triangular_section<'py>(
    py: Python<'py>,
    y: PyReadonlyArray1<'py, f64>,
) -> (&'py PyArray1<f64>, &'py PyArray1<f64>, &'py PyArray1<f64>) {
    let y_s = y.as_slice().unwrap();
    let (a, p, rh) = py.allow_threads(|| {
        open_channel::optimal_triangular_section_kernel(y_s)
    });
    (a.into_pyarray(py), p.into_pyarray(py), rh.into_pyarray(py))
}

#[pyfunction]
fn critical_velocity<'py>(
    py: Python<'py>,
    d_h: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let dh_s = d_h.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::critical_velocity_kernel(dh_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_slope<'py>(
    py: Python<'py>,
    roughness: PyReadonlyArray1<'py, f64>,
    r_hc: PyReadonlyArray1<'py, f64>,
    g: f64,
    k: f64,
) -> &'py PyArray1<f64> {
    let n_s = roughness.as_slice().unwrap();
    let rh_s = r_hc.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::critical_slope_kernel(n_s, rh_s, g, k)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn gravity_wave_celerity<'py>(
    py: Python<'py>,
    d_h: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let dh_s = d_h.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::gravity_wave_celerity_kernel(dh_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn hydraulic_jump_efficiency<'py>(
    py: Python<'py>,
    fr_1: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let fr_s = fr_1.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::hydraulic_jump_efficiency_kernel(fr_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn hydraulic_jump_height<'py>(
    py: Python<'py>,
    y_1: PyReadonlyArray1<'py, f64>,
    y_2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y1_s = y_1.as_slice().unwrap();
    let y2_s = y_2.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::hydraulic_jump_height_kernel(y1_s, y2_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_depth_triangular<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    m: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let m_s = m.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::critical_depth_triangular_kernel(q_s, m_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn horton_einstein_composite_n<'py>(
    py: Python<'py>,
    p_i: PyReadonlyArray1<'py, f64>,
    n_i: PyReadonlyArray1<'py, f64>,
) -> f64 {
    let p_s = p_i.as_slice().unwrap();
    let n_s = n_i.as_slice().unwrap();
    py.allow_threads(|| {
        open_channel::horton_einstein_composite_n_kernel(p_s, n_s)
    })
}

#[pyfunction]
fn pavlovskii_composite_n<'py>(
    py: Python<'py>,
    p_i: PyReadonlyArray1<'py, f64>,
    n_i: PyReadonlyArray1<'py, f64>,
) -> f64 {
    let p_s = p_i.as_slice().unwrap();
    let n_s = n_i.as_slice().unwrap();
    py.allow_threads(|| {
        open_channel::pavlovskii_composite_n_kernel(p_s, n_s)
    })
}

#[pyfunction]
fn boundary_shear_stress<'py>(
    py: Python<'py>,
    gamma: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let g_s = gamma.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::boundary_shear_stress_kernel(g_s, rh_s, s_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn shear_velocity<'py>(
    py: Python<'py>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::shear_velocity_kernel(rh_s, s_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn shields_parameter<'py>(
    py: Python<'py>,
    tau_0: PyReadonlyArray1<'py, f64>,
    delta_gamma: PyReadonlyArray1<'py, f64>,
    d_50: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = tau_0.as_slice().unwrap();
    let dg_s = delta_gamma.as_slice().unwrap();
    let d_s = d_50.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::shields_parameter_kernel(t_s, dg_s, d_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_shear_stress<'py>(
    py: Python<'py>,
    theta_c: PyReadonlyArray1<'py, f64>,
    delta_gamma: PyReadonlyArray1<'py, f64>,
    d_50: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let tc_s = theta_c.as_slice().unwrap();
    let dg_s = delta_gamma.as_slice().unwrap();
    let d_s = d_50.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::critical_shear_stress_kernel(tc_s, dg_s, d_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn lane_sediment_balance<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    d_50: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let d_s = d_50.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::lane_sediment_balance_kernel(q_s, s_s, d_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn meyer_peter_muller_bedload<'py>(
    py: Python<'py>,
    theta_star: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let th_s = theta_star.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::meyer_peter_muller_bedload_kernel(th_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn rubey_settling_velocity<'py>(
    py: Python<'py>,
    d: PyReadonlyArray1<'py, f64>,
    s_s: PyReadonlyArray1<'py, f64>,
    nu: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let d_s = d.as_slice().unwrap();
    let ss_s = s_s.as_slice().unwrap();
    let nu_s = nu.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::rubey_settling_velocity_kernel(d_s, ss_s, nu_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn stokes_settling_velocity<'py>(
    py: Python<'py>,
    d: PyReadonlyArray1<'py, f64>,
    s_s: PyReadonlyArray1<'py, f64>,
    nu: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let d_s = d.as_slice().unwrap();
    let ss_s = s_s.as_slice().unwrap();
    let nu_s = nu.as_slice().unwrap();
    let res = py.allow_threads(|| {
        open_channel::stokes_settling_velocity_kernel(d_s, ss_s, nu_s, g)
    });
    res.into_pyarray(py)
}

// ============================================================================
// EXPANSIONS: PIPE FLOW & CULVERTS
// ============================================================================

#[pyfunction]
fn culvert_inlet_unsubmerged<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    d: PyReadonlyArray1<'py, f64>,
    a: PyReadonlyArray1<'py, f64>,
    h_c: PyReadonlyArray1<'py, f64>,
    s: PyReadonlyArray1<'py, f64>,
    k_coeff: PyReadonlyArray1<'py, f64>,
    m_exp: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let d_s = d.as_slice().unwrap();
    let a_s = a.as_slice().unwrap();
    let hc_s = h_c.as_slice().unwrap();
    let s_s = s.as_slice().unwrap();
    let k_s = k_coeff.as_slice().unwrap();
    let m_s = m_exp.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::culvert_inlet_unsubmerged_kernel(q_s, d_s, a_s, hc_s, s_s, k_s, m_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn culvert_inlet_submerged<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    d: PyReadonlyArray1<'py, f64>,
    a: PyReadonlyArray1<'py, f64>,
    s: PyReadonlyArray1<'py, f64>,
    c_coeff: PyReadonlyArray1<'py, f64>,
    y_const: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let d_s = d.as_slice().unwrap();
    let a_s = a.as_slice().unwrap();
    let s_s = s.as_slice().unwrap();
    let c_s = c_coeff.as_slice().unwrap();
    let y_s = y_const.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::culvert_inlet_submerged_kernel(q_s, d_s, a_s, s_s, c_s, y_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn culvert_outlet_control_head<'py>(
    py: Python<'py>,
    h_o: PyReadonlyArray1<'py, f64>,
    h_losses: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let ho_s = h_o.as_slice().unwrap();
    let h_s = h_losses.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let s0_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::culvert_outlet_control_head_kernel(ho_s, h_s, l_s, s0_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn culvert_entrance_loss<'py>(
    py: Python<'py>,
    k_e: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let ke_s = k_e.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::culvert_entrance_loss_kernel(ke_s, v_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn hardy_cross_correction<'py>(
    py: Python<'py>,
    sum_hf: PyReadonlyArray1<'py, f64>,
    sum_dhf_dq: PyReadonlyArray1<'py, f64>,
    n_exp: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let shf_s = sum_hf.as_slice().unwrap();
    let sdhf_s = sum_dhf_dq.as_slice().unwrap();
    let n_s = n_exp.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::hardy_cross_correction_kernel(shf_s, sdhf_s, n_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn equivalent_pipe_length<'py>(
    py: Python<'py>,
    k_l: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    f: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let kl_s = k_l.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let f_s = f.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::equivalent_pipe_length_kernel(kl_s, d_s, f_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn equivalent_diameter_series<'py>(
    py: Python<'py>,
    l_total: PyReadonlyArray1<'py, f64>,
    sum_l_d5: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let lt_s = l_total.as_slice().unwrap();
    let sld_s = sum_l_d5.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::equivalent_diameter_series_kernel(lt_s, sld_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn parallel_pipes_distribution<'py>(
    py: Python<'py>,
    q_total: PyReadonlyArray1<'py, f64>,
    k_i: PyReadonlyArray1<'py, f64>,
    sum_k: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let qt_s = q_total.as_slice().unwrap();
    let ki_s = k_i.as_slice().unwrap();
    let sk_s = sum_k.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::parallel_pipes_distribution_kernel(qt_s, ki_s, sk_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn water_power<'py>(
    py: Python<'py>,
    discharge: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    gamma: PyReadonlyArray1<'py, f64>,
    divisor: f64,
) -> &'py PyArray1<f64> {
    let q_s = discharge.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let gam_s = gamma.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::water_power_kernel(q_s, h_s, gam_s, divisor)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn pump_brake_power<'py>(
    py: Python<'py>,
    p_w: PyReadonlyArray1<'py, f64>,
    eta: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let pw_s = p_w.as_slice().unwrap();
    let e_s = eta.as_slice().unwrap();
    let res = py.allow_threads(|| {
        pipe_flow::pump_brake_power_kernel(pw_s, e_s)
    });
    res.into_pyarray(py)
}

// ============================================================================
// EXPANSIONS: STRUCTURES & SPILLWAYS
// ============================================================================

#[pyfunction]
fn ogee_spillway_discharge<'py>(
    py: Python<'py>,
    c_o: PyReadonlyArray1<'py, f64>,
    l_e: PyReadonlyArray1<'py, f64>,
    h_e: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let co_s = c_o.as_slice().unwrap();
    let le_s = l_e.as_slice().unwrap();
    let he_s = h_e.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::ogee_spillway_discharge_kernel(co_s, le_s, he_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn ogee_discharge_coefficient<'py>(
    py: Python<'py>,
    c_o: PyReadonlyArray1<'py, f64>,
    h_e: PyReadonlyArray1<'py, f64>,
    h_o: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let co_s = c_o.as_slice().unwrap();
    let he_s = h_e.as_slice().unwrap();
    let ho_s = h_o.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::ogee_discharge_coefficient_kernel(co_s, he_s, ho_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn spillway_effective_length<'py>(
    py: Python<'py>,
    length: PyReadonlyArray1<'py, f64>,
    n_piers: PyReadonlyArray1<'py, f64>,
    k_p: PyReadonlyArray1<'py, f64>,
    k_a: PyReadonlyArray1<'py, f64>,
    h_e: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let l_s = length.as_slice().unwrap();
    let np_s = n_piers.as_slice().unwrap();
    let kp_s = k_p.as_slice().unwrap();
    let ka_s = k_a.as_slice().unwrap();
    let he_s = h_e.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::spillway_effective_length_kernel(l_s, np_s, kp_s, ka_s, he_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn chute_terminal_velocity<'py>(
    py: Python<'py>,
    z_drop: PyReadonlyArray1<'py, f64>,
    h_loss: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let zd_s = z_drop.as_slice().unwrap();
    let hl_s = h_loss.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::chute_terminal_velocity_kernel(zd_s, hl_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn stilling_basin_length<'py>(
    py: Python<'py>,
    y_2: PyReadonlyArray1<'py, f64>,
    k_basin: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y2_s = y_2.as_slice().unwrap();
    let kb_s = k_basin.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::stilling_basin_length_kernel(y2_s, kb_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn morning_glory_weir_flow<'py>(
    py: Python<'py>,
    radius: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    c_coeff: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let r_s = radius.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let c_s = c_coeff.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::morning_glory_weir_flow_kernel(r_s, h_s, c_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn siphon_spillway_discharge<'py>(
    py: Python<'py>,
    a_throat: PyReadonlyArray1<'py, f64>,
    h_operating: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let at_s = a_throat.as_slice().unwrap();
    let ho_s = h_operating.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::siphon_spillway_discharge_kernel(at_s, ho_s, cd_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn drop_structure_depth<'py>(
    py: Python<'py>,
    h_d: PyReadonlyArray1<'py, f64>,
    q: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let hd_s = h_d.as_slice().unwrap();
    let q_s = q.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::drop_structure_depth_kernel(hd_s, q_s, g)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn tailwater_depth<'py>(
    py: Python<'py>,
    discharge: PyReadonlyArray1<'py, f64>,
    a_coeff: PyReadonlyArray1<'py, f64>,
    b_exp: PyReadonlyArray1<'py, f64>,
    z_0: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = discharge.as_slice().unwrap();
    let a_s = a_coeff.as_slice().unwrap();
    let b_s = b_exp.as_slice().unwrap();
    let z0_s = z_0.as_slice().unwrap();
    let res = py.allow_threads(|| {
        structures::tailwater_depth_kernel(q_s, a_s, b_s, z0_s)
    });
    res.into_pyarray(py)
}

// ============================================================================
// EXPANSIONS: ADVANCED HYDROLOGY
// ============================================================================

#[pyfunction]
fn scs_composite_cn<'py>(
    py: Python<'py>,
    areas: PyReadonlyArray1<'py, f64>,
    cns: PyReadonlyArray1<'py, f64>,
) -> f64 {
    let a_s = areas.as_slice().unwrap();
    let cn_s = cns.as_slice().unwrap();
    py.allow_threads(|| {
        hydrology::scs_composite_cn_kernel(a_s, cn_s)
    })
}

#[pyfunction]
fn scs_cn_amc_i<'py>(
    py: Python<'py>,
    cn_ii: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let cn_s = cn_ii.as_slice().unwrap();
    let res = py.allow_threads(|| {
        hydrology::scs_cn_amc_i_kernel(cn_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn scs_cn_amc_iii<'py>(
    py: Python<'py>,
    cn_ii: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let cn_s = cn_ii.as_slice().unwrap();
    let res = py.allow_threads(|| {
        hydrology::scs_cn_amc_iii_kernel(cn_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn tr55_sheet_flow_time<'py>(
    py: Python<'py>,
    n_manning: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    p2_precip: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let nm_s = n_manning.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let p2_s = p2_precip.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| {
        hydrology::tr55_sheet_flow_time_kernel(nm_s, l_s, p2_s, s_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn tr55_shallow_concentrated_velocity<'py>(
    py: Python<'py>,
    slope: PyReadonlyArray1<'py, f64>,
    k_surface: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let s_s = slope.as_slice().unwrap();
    let k_s = k_surface.as_slice().unwrap();
    let res = py.allow_threads(|| {
        hydrology::tr55_shallow_concentrated_velocity_kernel(s_s, k_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn gumbel_flood_frequency<'py>(
    py: Python<'py>,
    mean_x: PyReadonlyArray1<'py, f64>,
    std_x: PyReadonlyArray1<'py, f64>,
    return_period: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let mx_s = mean_x.as_slice().unwrap();
    let sx_s = std_x.as_slice().unwrap();
    let t_s = return_period.as_slice().unwrap();
    let res = py.allow_threads(|| {
        hydrology::gumbel_flood_frequency_kernel(mx_s, sx_s, t_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn nash_cascade_iuh<'py>(
    py: Python<'py>,
    time: PyReadonlyArray1<'py, f64>,
    n_reservoirs: PyReadonlyArray1<'py, f64>,
    k_storage: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = time.as_slice().unwrap();
    let nr_s = n_reservoirs.as_slice().unwrap();
    let ks_s = k_storage.as_slice().unwrap();
    let res = py.allow_threads(|| {
        hydrology::nash_cascade_iuh_kernel(t_s, nr_s, ks_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn hargreaves_samani_et0<'py>(
    py: Python<'py>,
    r_a: PyReadonlyArray1<'py, f64>,
    t_mean: PyReadonlyArray1<'py, f64>,
    t_max: PyReadonlyArray1<'py, f64>,
    t_min: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let ra_s = r_a.as_slice().unwrap();
    let tm_s = t_mean.as_slice().unwrap();
    let tmax_s = t_max.as_slice().unwrap();
    let tmin_s = t_min.as_slice().unwrap();
    let res = py.allow_threads(|| {
        hydrology::hargreaves_samani_et0_kernel(ra_s, tm_s, tmax_s, tmin_s)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn net_radiation_equivalent_evap<'py>(
    py: Python<'py>,
    rn_mj: PyReadonlyArray1<'py, f64>,
    lambda_latent: PyReadonlyArray1<'py, f64>,
    rho_w: f64,
) -> &'py PyArray1<f64> {
    let rn_s = rn_mj.as_slice().unwrap();
    let lam_s = lambda_latent.as_slice().unwrap();
    let res = py.allow_threads(|| {
        hydrology::net_radiation_equivalent_evap_kernel(rn_s, lam_s, rho_w)
    });
    res.into_pyarray(py)
}

#[pyfunction]
fn time_area_runoff_step<'py>(
    py: Python<'py>,
    i_excess: PyReadonlyArray1<'py, f64>,
    a_k: PyReadonlyArray1<'py, f64>,
    k_unit: f64,
) -> f64 {
    let ie_s = i_excess.as_slice().unwrap();
    let ak_s = a_k.as_slice().unwrap();
    py.allow_threads(|| {
        hydrology::time_area_runoff_step_kernel(ie_s, ak_s, k_unit)
    })
}

/// The PyO3 module definition exposing all compiled computational kernels.

// ============================================================================
// DEDICATED BIDIRECTIONAL ALGEBRAIC INVERSIONS (APPROACH 1)
// ============================================================================

// --- Open Channel Inversions ---
#[pyfunction]
fn manning_n<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::manning_n_kernel(q_s, a_s, rh_s, s_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn manning_s0<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    roughness: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let n_s = roughness.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::manning_s0_kernel(q_s, a_s, rh_s, n_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn manning_rh<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    roughness: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let n_s = roughness.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::manning_rh_kernel(q_s, a_s, s_s, n_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn manning_a<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    roughness: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let n_s = roughness.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::manning_a_kernel(q_s, rh_s, s_s, n_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn chezy_c<'py>(
    py: Python<'py>,
    velocity: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let v_s = velocity.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::chezy_c_kernel(v_s, rh_s, s_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn chezy_s0<'py>(
    py: Python<'py>,
    velocity: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let v_s = velocity.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::chezy_s0_kernel(v_s, c_s, rh_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn chezy_rh<'py>(
    py: Python<'py>,
    velocity: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let v_s = velocity.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::chezy_rh_kernel(v_s, c_s, s_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn strickler_kst<'py>(
    py: Python<'py>,
    velocity: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let v_s = velocity.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::strickler_kst_kernel(v_s, rh_s, s_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn strickler_s0<'py>(
    py: Python<'py>,
    velocity: PyReadonlyArray1<'py, f64>,
    k_st: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let v_s = velocity.as_slice().unwrap();
    let k_s = k_st.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::strickler_s0_kernel(v_s, k_s, rh_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn froude_v<'py>(
    py: Python<'py>,
    fr: PyReadonlyArray1<'py, f64>,
    d_h: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let fr_s = fr.as_slice().unwrap();
    let dh_s = d_h.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::froude_v_kernel(fr_s, dh_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn froude_dh<'py>(
    py: Python<'py>,
    fr: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let fr_s = fr.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::froude_dh_kernel(fr_s, v_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn specific_energy_v<'py>(
    py: Python<'py>,
    e: PyReadonlyArray1<'py, f64>,
    y: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let e_s = e.as_slice().unwrap();
    let y_s = y.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::specific_energy_v_kernel(e_s, y_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn hydraulic_jump_fr1<'py>(
    py: Python<'py>,
    y1: PyReadonlyArray1<'py, f64>,
    y2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y1_s = y1.as_slice().unwrap();
    let y2_s = y2.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::hydraulic_jump_fr1_kernel(y1_s, y2_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn hydraulic_jump_y1<'py>(
    py: Python<'py>,
    y2: PyReadonlyArray1<'py, f64>,
    fr1: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y2_s = y2.as_slice().unwrap();
    let fr_s = fr1.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::hydraulic_jump_y1_kernel(y2_s, fr_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_depth_rect_q<'py>(
    py: Python<'py>,
    yc: PyReadonlyArray1<'py, f64>,
    b: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let yc_s = yc.as_slice().unwrap();
    let b_s = b.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::critical_depth_rect_q_kernel(yc_s, b_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_depth_tri_q<'py>(
    py: Python<'py>,
    yc: PyReadonlyArray1<'py, f64>,
    z: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let yc_s = yc.as_slice().unwrap();
    let z_s = z.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::critical_depth_tri_q_kernel(yc_s, z_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_velocity_dh<'py>(
    py: Python<'py>,
    vc: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let vc_s = vc.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::critical_velocity_dh_kernel(vc_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_slope_n<'py>(
    py: Python<'py>,
    sc: PyReadonlyArray1<'py, f64>,
    q: PyReadonlyArray1<'py, f64>,
    b: PyReadonlyArray1<'py, f64>,
    g: f64,
    k: f64,
) -> &'py PyArray1<f64> {
    let sc_s = sc.as_slice().unwrap();
    let q_s = q.as_slice().unwrap();
    let b_s = b.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::critical_slope_n_kernel(sc_s, q_s, b_s, g, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn boundary_shear_s0<'py>(
    py: Python<'py>,
    tau_0: PyReadonlyArray1<'py, f64>,
    gamma: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = tau_0.as_slice().unwrap();
    let g_s = gamma.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::boundary_shear_s0_kernel(t_s, g_s, rh_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn boundary_shear_rh<'py>(
    py: Python<'py>,
    tau_0: PyReadonlyArray1<'py, f64>,
    gamma: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = tau_0.as_slice().unwrap();
    let g_s = gamma.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::boundary_shear_rh_kernel(t_s, g_s, s_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn shields_param_tau0<'py>(
    py: Python<'py>,
    theta_star: PyReadonlyArray1<'py, f64>,
    gamma_s: PyReadonlyArray1<'py, f64>,
    gamma_w: PyReadonlyArray1<'py, f64>,
    d50: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let th_s = theta_star.as_slice().unwrap();
    let gs_s = gamma_s.as_slice().unwrap();
    let gw_s = gamma_w.as_slice().unwrap();
    let d_s = d50.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::shields_param_tau0_kernel(th_s, gs_s, gw_s, d_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn shields_param_d50<'py>(
    py: Python<'py>,
    theta_star: PyReadonlyArray1<'py, f64>,
    tau_0: PyReadonlyArray1<'py, f64>,
    gamma_s: PyReadonlyArray1<'py, f64>,
    gamma_w: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let th_s = theta_star.as_slice().unwrap();
    let t_s = tau_0.as_slice().unwrap();
    let gs_s = gamma_s.as_slice().unwrap();
    let gw_s = gamma_w.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::shields_param_d50_kernel(th_s, t_s, gs_s, gw_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn lane_balance_s<'py>(
    py: Python<'py>,
    qs: PyReadonlyArray1<'py, f64>,
    d50: PyReadonlyArray1<'py, f64>,
    qw: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let qs_s = qs.as_slice().unwrap();
    let d_s = d50.as_slice().unwrap();
    let qw_s = qw.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::lane_balance_s_kernel(qs_s, d_s, qw_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn stokes_settling_d<'py>(
    py: Python<'py>,
    ws: PyReadonlyArray1<'py, f64>,
    s_s: PyReadonlyArray1<'py, f64>,
    nu: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let ws_s = ws.as_slice().unwrap();
    let ss_s = s_s.as_slice().unwrap();
    let nu_s = nu.as_slice().unwrap();
    let res = py.allow_threads(|| open_channel::stokes_settling_d_kernel(ws_s, ss_s, nu_s, g));
    res.into_pyarray(py)
}

// --- Pipe Flow Inversions ---
#[pyfunction]
fn darcy_weisbach_f<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::darcy_weisbach_f_kernel(h_s, l_s, d_s, v_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn darcy_weisbach_d<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    f: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let f_s = f.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::darcy_weisbach_d_kernel(h_s, f_s, l_s, v_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn darcy_weisbach_l<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    f: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let f_s = f.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::darcy_weisbach_l_kernel(h_s, f_s, d_s, v_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn darcy_weisbach_v<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    f: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let f_s = f.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::darcy_weisbach_v_kernel(h_s, f_s, l_s, d_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn darcy_weisbach_q<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    f: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let f_s = f.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::darcy_weisbach_q_kernel(h_s, f_s, l_s, d_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn hazen_williams_q<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    k_l: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::hazen_williams_q_kernel(h_s, c_s, d_s, l_s, k_l));
    res.into_pyarray(py)
}

#[pyfunction]
fn hazen_williams_d<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    q: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    k_l: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let q_s = q.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::hazen_williams_d_kernel(h_s, q_s, c_s, l_s, k_l));
    res.into_pyarray(py)
}

#[pyfunction]
fn hazen_williams_l<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    q: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    k_l: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let q_s = q.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::hazen_williams_l_kernel(h_s, q_s, c_s, d_s, k_l));
    res.into_pyarray(py)
}

#[pyfunction]
fn hazen_williams_c<'py>(
    py: Python<'py>,
    hf: PyReadonlyArray1<'py, f64>,
    q: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    k_l: f64,
) -> &'py PyArray1<f64> {
    let h_s = hf.as_slice().unwrap();
    let q_s = q.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::hazen_williams_c_kernel(h_s, q_s, d_s, l_s, k_l));
    res.into_pyarray(py)
}

#[pyfunction]
fn hazen_williams_s<'py>(
    py: Python<'py>,
    velocity: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
    r_h: PyReadonlyArray1<'py, f64>,
    k_v: f64,
) -> &'py PyArray1<f64> {
    let v_s = velocity.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();
    let rh_s = r_h.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::hazen_williams_s_kernel(v_s, c_s, rh_s, k_v));
    res.into_pyarray(py)
}

#[pyfunction]
fn reynolds_v<'py>(
    py: Python<'py>,
    re: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    kinematic_viscosity: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let r_s = re.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let nu_s = kinematic_viscosity.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::reynolds_v_kernel(r_s, d_s, nu_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn reynolds_d<'py>(
    py: Python<'py>,
    re: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    kinematic_viscosity: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let r_s = re.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();
    let nu_s = kinematic_viscosity.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::reynolds_d_kernel(r_s, v_s, nu_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn minor_loss_kl<'py>(
    py: Python<'py>,
    hm: PyReadonlyArray1<'py, f64>,
    velocity: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let h_s = hm.as_slice().unwrap();
    let v_s = velocity.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::minor_loss_kl_kernel(h_s, v_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn minor_loss_v<'py>(
    py: Python<'py>,
    hm: PyReadonlyArray1<'py, f64>,
    kl: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let h_s = hm.as_slice().unwrap();
    let k_s = kl.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::minor_loss_v_kernel(h_s, k_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn joukowsky_dv<'py>(
    py: Python<'py>,
    dp: PyReadonlyArray1<'py, f64>,
    a: PyReadonlyArray1<'py, f64>,
    rho: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let p_s = dp.as_slice().unwrap();
    let a_s = a.as_slice().unwrap();
    let r_s = rho.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::joukowsky_dv_kernel(p_s, a_s, r_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn joukowsky_a<'py>(
    py: Python<'py>,
    dp: PyReadonlyArray1<'py, f64>,
    dv: PyReadonlyArray1<'py, f64>,
    rho: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let p_s = dp.as_slice().unwrap();
    let v_s = dv.as_slice().unwrap();
    let r_s = rho.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::joukowsky_a_kernel(p_s, v_s, r_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_closure_l<'py>(
    py: Python<'py>,
    tc: PyReadonlyArray1<'py, f64>,
    a: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = tc.as_slice().unwrap();
    let a_s = a.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::critical_closure_l_kernel(t_s, a_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn critical_closure_a<'py>(
    py: Python<'py>,
    tc: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let t_s = tc.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::critical_closure_a_kernel(t_s, l_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn equivalent_pipe_kl<'py>(
    py: Python<'py>,
    le: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
    f: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let l_s = le.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let f_s = f.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::equivalent_pipe_kl_kernel(l_s, d_s, f_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn equivalent_pipe_f<'py>(
    py: Python<'py>,
    le: PyReadonlyArray1<'py, f64>,
    kl: PyReadonlyArray1<'py, f64>,
    diameter: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let l_s = le.as_slice().unwrap();
    let k_s = kl.as_slice().unwrap();
    let d_s = diameter.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::equivalent_pipe_f_kernel(l_s, k_s, d_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn water_power_q<'py>(
    py: Python<'py>,
    pw: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    gamma: PyReadonlyArray1<'py, f64>,
    divisor: f64,
) -> &'py PyArray1<f64> {
    let p_s = pw.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let gam_s = gamma.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::water_power_q_kernel(p_s, h_s, gam_s, divisor));
    res.into_pyarray(py)
}

#[pyfunction]
fn water_power_h<'py>(
    py: Python<'py>,
    pw: PyReadonlyArray1<'py, f64>,
    q: PyReadonlyArray1<'py, f64>,
    gamma: PyReadonlyArray1<'py, f64>,
    divisor: f64,
) -> &'py PyArray1<f64> {
    let p_s = pw.as_slice().unwrap();
    let q_s = q.as_slice().unwrap();
    let gam_s = gamma.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::water_power_h_kernel(p_s, q_s, gam_s, divisor));
    res.into_pyarray(py)
}

#[pyfunction]
fn pump_power_pw<'py>(
    py: Python<'py>,
    pb: PyReadonlyArray1<'py, f64>,
    eta: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let b_s = pb.as_slice().unwrap();
    let e_s = eta.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::pump_power_pw_kernel(b_s, e_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn pump_power_eta<'py>(
    py: Python<'py>,
    pw: PyReadonlyArray1<'py, f64>,
    pb: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let w_s = pw.as_slice().unwrap();
    let b_s = pb.as_slice().unwrap();
    let res = py.allow_threads(|| pipe_flow::pump_power_eta_kernel(w_s, b_s));
    res.into_pyarray(py)
}

// --- Hydrology Inversions ---
#[pyfunction]
fn rational_c<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    intensity: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let i_s = intensity.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::rational_c_kernel(q_s, i_s, a_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn rational_i<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::rational_i_kernel(q_s, c_s, a_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn rational_a<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    c: PyReadonlyArray1<'py, f64>,
    intensity: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let c_s = c.as_slice().unwrap();
    let i_s = intensity.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::rational_a_kernel(q_s, c_s, i_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn scs_cn_s<'py>(
    py: Python<'py>,
    cn: PyReadonlyArray1<'py, f64>,
    factor: f64,
    offset: f64,
) -> &'py PyArray1<f64> {
    let c_s = cn.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::scs_cn_s_kernel(c_s, factor, offset));
    res.into_pyarray(py)
}

#[pyfunction]
fn scs_cn_cn<'py>(
    py: Python<'py>,
    s: PyReadonlyArray1<'py, f64>,
    factor: f64,
    offset: f64,
) -> &'py PyArray1<f64> {
    let s_s = s.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::scs_cn_cn_kernel(s_s, factor, offset));
    res.into_pyarray(py)
}

#[pyfunction]
fn scs_cn_p<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    s: PyReadonlyArray1<'py, f64>,
    lambda: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let s_s = s.as_slice().unwrap();
    let lam_s = lambda.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::scs_cn_p_kernel(q_s, s_s, lam_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn horton_rate_f0<'py>(
    py: Python<'py>,
    fp: PyReadonlyArray1<'py, f64>,
    fc: PyReadonlyArray1<'py, f64>,
    k: PyReadonlyArray1<'py, f64>,
    t: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let p_s = fp.as_slice().unwrap();
    let c_s = fc.as_slice().unwrap();
    let k_s = k.as_slice().unwrap();
    let t_s = t.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::horton_rate_f0_kernel(p_s, c_s, k_s, t_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn horton_rate_fc<'py>(
    py: Python<'py>,
    fp: PyReadonlyArray1<'py, f64>,
    f0: PyReadonlyArray1<'py, f64>,
    k: PyReadonlyArray1<'py, f64>,
    t: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let p_s = fp.as_slice().unwrap();
    let z_s = f0.as_slice().unwrap();
    let k_s = k.as_slice().unwrap();
    let t_s = t.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::horton_rate_fc_kernel(p_s, z_s, k_s, t_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn horton_rate_k<'py>(
    py: Python<'py>,
    fp: PyReadonlyArray1<'py, f64>,
    f0: PyReadonlyArray1<'py, f64>,
    fc: PyReadonlyArray1<'py, f64>,
    t: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let p_s = fp.as_slice().unwrap();
    let z_s = f0.as_slice().unwrap();
    let c_s = fc.as_slice().unwrap();
    let t_s = t.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::horton_rate_k_kernel(p_s, z_s, c_s, t_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn kirpich_s<'py>(
    py: Python<'py>,
    tc: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let t_s = tc.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::kirpich_s_kernel(t_s, l_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn kirpich_l<'py>(
    py: Python<'py>,
    tc: PyReadonlyArray1<'py, f64>,
    slope: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let t_s = tc.as_slice().unwrap();
    let s_s = slope.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::kirpich_l_kernel(t_s, s_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn scs_amc_cnii_from_i<'py>(
    py: Python<'py>,
    cni: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let c_s = cni.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::scs_amc_cnii_from_i_kernel(c_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn scs_amc_cnii_from_iii<'py>(
    py: Python<'py>,
    cniii: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let c_s = cniii.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::scs_amc_cnii_from_iii_kernel(c_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn tr55_shallow_s<'py>(
    py: Python<'py>,
    v: PyReadonlyArray1<'py, f64>,
    k: f64,
) -> &'py PyArray1<f64> {
    let v_s = v.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::tr55_shallow_s_kernel(v_s, k));
    res.into_pyarray(py)
}

#[pyfunction]
fn hargreaves_ra<'py>(
    py: Python<'py>,
    et0: PyReadonlyArray1<'py, f64>,
    t_mean: PyReadonlyArray1<'py, f64>,
    t_max: PyReadonlyArray1<'py, f64>,
    t_min: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let et_s = et0.as_slice().unwrap();
    let tm_s = t_mean.as_slice().unwrap();
    let tmx_s = t_max.as_slice().unwrap();
    let tmn_s = t_min.as_slice().unwrap();
    let res = py.allow_threads(|| hydrology::hargreaves_ra_kernel(et_s, tm_s, tmx_s, tmn_s));
    res.into_pyarray(py)
}

// --- Structures Inversions ---
#[pyfunction]
fn francis_weir_l<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    contractions: PyReadonlyArray1<'py, f64>,
    k_francis: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let ne_s = contractions.as_slice().unwrap();
    let res = py.allow_threads(|| structures::francis_weir_l_kernel(q_s, h_s, ne_s, k_francis));
    res.into_pyarray(py)
}

#[pyfunction]
fn v_notch_weir_h<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    theta_rad: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let th_s = theta_rad.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::v_notch_weir_h_kernel(q_s, th_s, cd_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn v_notch_weir_cd<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    theta_rad: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let th_s = theta_rad.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let res = py.allow_threads(|| structures::v_notch_weir_cd_kernel(q_s, th_s, h_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn v_notch_weir_theta<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::v_notch_weir_theta_kernel(q_s, h_s, cd_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn broad_crested_weir_h<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::broad_crested_weir_h_kernel(q_s, l_s, cd_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn broad_crested_weir_l<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::broad_crested_weir_l_kernel(q_s, h_s, cd_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn orifice_free_h<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::orifice_free_h_kernel(q_s, a_s, cd_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn orifice_free_ao<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    head: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let h_s = head.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::orifice_free_ao_kernel(q_s, h_s, cd_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn sluice_gate_free_a<'py>(
    py: Python<'py>,
    b: PyReadonlyArray1<'py, f64>,
    q: PyReadonlyArray1<'py, f64>,
    y1: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let b_s = b.as_slice().unwrap();
    let y_s = y1.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::sluice_gate_free_a_kernel(q_s, b_s, y_s, cd_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn ogee_spillway_he<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    length: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let l_s = length.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::ogee_spillway_he_kernel(q_s, l_s, cd_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn ogee_spillway_le<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    he: PyReadonlyArray1<'py, f64>,
    c_d: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let h_s = he.as_slice().unwrap();
    let cd_s = c_d.as_slice().unwrap();
    let res = py.allow_threads(|| structures::ogee_spillway_le_kernel(q_s, h_s, cd_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn chute_velocity_z<'py>(
    py: Python<'py>,
    v: PyReadonlyArray1<'py, f64>,
    v0: PyReadonlyArray1<'py, f64>,
    z0: PyReadonlyArray1<'py, f64>,
    g: f64,
) -> &'py PyArray1<f64> {
    let v_s = v.as_slice().unwrap();
    let v0_s = v0.as_slice().unwrap();
    let z0_s = z0.as_slice().unwrap();
    let res = py.allow_threads(|| structures::chute_velocity_z_kernel(v_s, v0_s, z0_s, g));
    res.into_pyarray(py)
}

#[pyfunction]
fn stilling_basin_y2<'py>(
    py: Python<'py>,
    y1: PyReadonlyArray1<'py, f64>,
    fr1: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y_s = y1.as_slice().unwrap();
    let fr_s = fr1.as_slice().unwrap();
    let res = py.allow_threads(|| structures::stilling_basin_y2_kernel(y_s, fr_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn stilling_basin_y1<'py>(
    py: Python<'py>,
    y2: PyReadonlyArray1<'py, f64>,
    fr1: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let y_s = y2.as_slice().unwrap();
    let fr_s = fr1.as_slice().unwrap();
    let res = py.allow_threads(|| structures::stilling_basin_y1_kernel(y_s, fr_s));
    res.into_pyarray(py)
}

// --- Groundwater Inversions ---
#[pyfunction]
fn darcy_flow_k<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
    dh_dl: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let grad_s = dh_dl.as_slice().unwrap();
    let res = py.allow_threads(|| groundwater::darcy_flow_k_kernel(q_s, a_s, grad_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn darcy_flow_dh_dl<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    k: PyReadonlyArray1<'py, f64>,
    area: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let k_s = k.as_slice().unwrap();
    let a_s = area.as_slice().unwrap();
    let res = py.allow_threads(|| groundwater::darcy_flow_dh_dl_kernel(q_s, k_s, a_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn thiem_confined_t<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    h1: PyReadonlyArray1<'py, f64>,
    h2: PyReadonlyArray1<'py, f64>,
    r1: PyReadonlyArray1<'py, f64>,
    r2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let h1_s = h1.as_slice().unwrap();
    let h2_s = h2.as_slice().unwrap();
    let r1_s = r1.as_slice().unwrap();
    let r2_s = r2.as_slice().unwrap();
    let res = py.allow_threads(|| groundwater::thiem_confined_t_kernel(q_s, h1_s, h2_s, r1_s, r2_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn thiem_confined_dh<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    transmissivity: PyReadonlyArray1<'py, f64>,
    r1: PyReadonlyArray1<'py, f64>,
    r2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let t_s = transmissivity.as_slice().unwrap();
    let r1_s = r1.as_slice().unwrap();
    let r2_s = r2.as_slice().unwrap();
    let res = py.allow_threads(|| groundwater::thiem_confined_dh_kernel(q_s, t_s, r1_s, r2_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn thiem_unconfined_k<'py>(
    py: Python<'py>,
    q: PyReadonlyArray1<'py, f64>,
    h1: PyReadonlyArray1<'py, f64>,
    h2: PyReadonlyArray1<'py, f64>,
    r1: PyReadonlyArray1<'py, f64>,
    r2: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let q_s = q.as_slice().unwrap();
    let h1_s = h1.as_slice().unwrap();
    let h2_s = h2.as_slice().unwrap();
    let r1_s = r1.as_slice().unwrap();
    let r2_s = r2.as_slice().unwrap();
    let res = py.allow_threads(|| groundwater::thiem_unconfined_k_kernel(q_s, h1_s, h2_s, r1_s, r2_s));
    res.into_pyarray(py)
}

#[pyfunction]
fn cooper_jacob_q<'py>(
    py: Python<'py>,
    s: PyReadonlyArray1<'py, f64>,
    transmissivity: PyReadonlyArray1<'py, f64>,
    storativity: PyReadonlyArray1<'py, f64>,
    radius: PyReadonlyArray1<'py, f64>,
    time: PyReadonlyArray1<'py, f64>,
) -> &'py PyArray1<f64> {
    let s_s = s.as_slice().unwrap();
    let t_s = transmissivity.as_slice().unwrap();
    let stor_s = storativity.as_slice().unwrap();
    let r_s = radius.as_slice().unwrap();
    let time_s = time.as_slice().unwrap();
    let res = py.allow_threads(|| groundwater::cooper_jacob_q_kernel(s_s, t_s, stor_s, r_s, time_s));
    res.into_pyarray(py)
}

#[pymodule]
fn _hydroaj_core(_py: Python, m: &PyModule) -> PyResult<()> {
    // Open Channel
    m.add_function(wrap_pyfunction!(manning_discharge, m)?)?;
    m.add_function(wrap_pyfunction!(manning_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(strickler_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(chezy_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(kutter_chezy_c, m)?)?;
    m.add_function(wrap_pyfunction!(bazin_chezy_c, m)?)?;
    m.add_function(wrap_pyfunction!(geom_rectangular, m)?)?;
    m.add_function(wrap_pyfunction!(geom_trapezoidal, m)?)?;
    m.add_function(wrap_pyfunction!(geom_triangular, m)?)?;
    m.add_function(wrap_pyfunction!(geom_circular, m)?)?;
    m.add_function(wrap_pyfunction!(geom_parabolic, m)?)?;
    m.add_function(wrap_pyfunction!(specific_energy, m)?)?;
    m.add_function(wrap_pyfunction!(froude_number, m)?)?;
    m.add_function(wrap_pyfunction!(specific_force, m)?)?;
    m.add_function(wrap_pyfunction!(critical_depth_rectangular, m)?)?;
    m.add_function(wrap_pyfunction!(normal_depth_trapezoidal, m)?)?;
    m.add_function(wrap_pyfunction!(belanger_conjugate_depth, m)?)?;
    m.add_function(wrap_pyfunction!(hydraulic_jump_head_loss, m)?)?;
    m.add_function(wrap_pyfunction!(hydraulic_jump_length, m)?)?;
    m.add_function(wrap_pyfunction!(gvf_gradient, m)?)?;
    m.add_function(wrap_pyfunction!(manning_friction_slope, m)?)?;
    m.add_function(wrap_pyfunction!(direct_step, m)?)?;

    // Pipe Flow
    m.add_function(wrap_pyfunction!(darcy_weisbach, m)?)?;
    m.add_function(wrap_pyfunction!(reynolds_number, m)?)?;
    m.add_function(wrap_pyfunction!(laminar_friction, m)?)?;
    m.add_function(wrap_pyfunction!(colebrook_white, m)?)?;
    m.add_function(wrap_pyfunction!(swamee_jain, m)?)?;
    m.add_function(wrap_pyfunction!(haaland, m)?)?;
    m.add_function(wrap_pyfunction!(churchill, m)?)?;
    m.add_function(wrap_pyfunction!(wood, m)?)?;
    m.add_function(wrap_pyfunction!(hazen_williams, m)?)?;
    m.add_function(wrap_pyfunction!(hazen_williams_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(minor_loss, m)?)?;
    m.add_function(wrap_pyfunction!(wave_celerity, m)?)?;
    m.add_function(wrap_pyfunction!(joukowsky, m)?)?;
    m.add_function(wrap_pyfunction!(critical_closure_time, m)?)?;

    // Hydrology
    m.add_function(wrap_pyfunction!(idf_sherman, m)?)?;
    m.add_function(wrap_pyfunction!(thiessen_areal, m)?)?;
    m.add_function(wrap_pyfunction!(horton_rate, m)?)?;
    m.add_function(wrap_pyfunction!(horton_cumulative, m)?)?;
    m.add_function(wrap_pyfunction!(green_ampt_rate, m)?)?;
    m.add_function(wrap_pyfunction!(scs_retention, m)?)?;
    m.add_function(wrap_pyfunction!(scs_runoff_depth, m)?)?;
    m.add_function(wrap_pyfunction!(rational_peak_flow, m)?)?;
    m.add_function(wrap_pyfunction!(kirpich_tc, m)?)?;
    m.add_function(wrap_pyfunction!(snyder, m)?)?;
    m.add_function(wrap_pyfunction!(scs_peak_flow, m)?)?;
    m.add_function(wrap_pyfunction!(muskingum_coefficients, m)?)?;
    m.add_function(wrap_pyfunction!(muskingum_route, m)?)?;

    // Structures & Groundwater
    m.add_function(wrap_pyfunction!(francis_weir, m)?)?;
    m.add_function(wrap_pyfunction!(v_notch_weir, m)?)?;
    m.add_function(wrap_pyfunction!(broad_crested_weir, m)?)?;
    m.add_function(wrap_pyfunction!(parshall_flume, m)?)?;
    m.add_function(wrap_pyfunction!(orifice_free, m)?)?;
    m.add_function(wrap_pyfunction!(orifice_submerged, m)?)?;
    m.add_function(wrap_pyfunction!(sluice_gate_free, m)?)?;
    m.add_function(wrap_pyfunction!(sluice_gate_submerged, m)?)?;
    m.add_function(wrap_pyfunction!(darcy_flow_1d, m)?)?;
    m.add_function(wrap_pyfunction!(darcy_flux, m)?)?;
    m.add_function(wrap_pyfunction!(thiem_confined, m)?)?;
    m.add_function(wrap_pyfunction!(thiem_unconfined, m)?)?;
    m.add_function(wrap_pyfunction!(theis_drawdown, m)?)?;
    m.add_function(wrap_pyfunction!(cooper_jacob_drawdown, m)?)?;

    // Open Channel Expansions & Sediment
    m.add_function(wrap_pyfunction!(optimal_rectangular_section, m)?)?;
    m.add_function(wrap_pyfunction!(optimal_trapezoidal_section, m)?)?;
    m.add_function(wrap_pyfunction!(optimal_triangular_section, m)?)?;
    m.add_function(wrap_pyfunction!(critical_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(critical_slope, m)?)?;
    m.add_function(wrap_pyfunction!(gravity_wave_celerity, m)?)?;
    m.add_function(wrap_pyfunction!(hydraulic_jump_efficiency, m)?)?;
    m.add_function(wrap_pyfunction!(hydraulic_jump_height, m)?)?;
    m.add_function(wrap_pyfunction!(critical_depth_triangular, m)?)?;
    m.add_function(wrap_pyfunction!(horton_einstein_composite_n, m)?)?;
    m.add_function(wrap_pyfunction!(pavlovskii_composite_n, m)?)?;
    m.add_function(wrap_pyfunction!(boundary_shear_stress, m)?)?;
    m.add_function(wrap_pyfunction!(shear_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(shields_parameter, m)?)?;
    m.add_function(wrap_pyfunction!(critical_shear_stress, m)?)?;
    m.add_function(wrap_pyfunction!(lane_sediment_balance, m)?)?;
    m.add_function(wrap_pyfunction!(meyer_peter_muller_bedload, m)?)?;
    m.add_function(wrap_pyfunction!(rubey_settling_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(stokes_settling_velocity, m)?)?;

    // Pipe Flow Expansions & Culverts
    m.add_function(wrap_pyfunction!(culvert_inlet_unsubmerged, m)?)?;
    m.add_function(wrap_pyfunction!(culvert_inlet_submerged, m)?)?;
    m.add_function(wrap_pyfunction!(culvert_outlet_control_head, m)?)?;
    m.add_function(wrap_pyfunction!(culvert_entrance_loss, m)?)?;
    m.add_function(wrap_pyfunction!(hardy_cross_correction, m)?)?;
    m.add_function(wrap_pyfunction!(equivalent_pipe_length, m)?)?;
    m.add_function(wrap_pyfunction!(equivalent_diameter_series, m)?)?;
    m.add_function(wrap_pyfunction!(parallel_pipes_distribution, m)?)?;
    m.add_function(wrap_pyfunction!(water_power, m)?)?;
    m.add_function(wrap_pyfunction!(pump_brake_power, m)?)?;

    // Structures & Spillways Expansions
    m.add_function(wrap_pyfunction!(ogee_spillway_discharge, m)?)?;
    m.add_function(wrap_pyfunction!(ogee_discharge_coefficient, m)?)?;
    m.add_function(wrap_pyfunction!(spillway_effective_length, m)?)?;
    m.add_function(wrap_pyfunction!(chute_terminal_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(stilling_basin_length, m)?)?;
    m.add_function(wrap_pyfunction!(morning_glory_weir_flow, m)?)?;
    m.add_function(wrap_pyfunction!(siphon_spillway_discharge, m)?)?;
    m.add_function(wrap_pyfunction!(drop_structure_depth, m)?)?;
    m.add_function(wrap_pyfunction!(tailwater_depth, m)?)?;

    // Hydrology Expansions
    m.add_function(wrap_pyfunction!(scs_composite_cn, m)?)?;
    m.add_function(wrap_pyfunction!(scs_cn_amc_i, m)?)?;
    m.add_function(wrap_pyfunction!(scs_cn_amc_iii, m)?)?;
    m.add_function(wrap_pyfunction!(tr55_sheet_flow_time, m)?)?;
    m.add_function(wrap_pyfunction!(tr55_shallow_concentrated_velocity, m)?)?;
    m.add_function(wrap_pyfunction!(gumbel_flood_frequency, m)?)?;
    m.add_function(wrap_pyfunction!(nash_cascade_iuh, m)?)?;
    m.add_function(wrap_pyfunction!(hargreaves_samani_et0, m)?)?;
    m.add_function(wrap_pyfunction!(net_radiation_equivalent_evap, m)?)?;
    m.add_function(wrap_pyfunction!(time_area_runoff_step, m)?)?;

    
    // Dedicated Bidirectional Inversions - Open Channel
    m.add_function(wrap_pyfunction!(manning_n, m)?)?;
    m.add_function(wrap_pyfunction!(manning_s0, m)?)?;
    m.add_function(wrap_pyfunction!(manning_rh, m)?)?;
    m.add_function(wrap_pyfunction!(manning_a, m)?)?;
    m.add_function(wrap_pyfunction!(chezy_c, m)?)?;
    m.add_function(wrap_pyfunction!(chezy_s0, m)?)?;
    m.add_function(wrap_pyfunction!(chezy_rh, m)?)?;
    m.add_function(wrap_pyfunction!(strickler_kst, m)?)?;
    m.add_function(wrap_pyfunction!(strickler_s0, m)?)?;
    m.add_function(wrap_pyfunction!(froude_v, m)?)?;
    m.add_function(wrap_pyfunction!(froude_dh, m)?)?;
    m.add_function(wrap_pyfunction!(specific_energy_v, m)?)?;
    m.add_function(wrap_pyfunction!(hydraulic_jump_fr1, m)?)?;
    m.add_function(wrap_pyfunction!(hydraulic_jump_y1, m)?)?;
    m.add_function(wrap_pyfunction!(critical_depth_rect_q, m)?)?;
    m.add_function(wrap_pyfunction!(critical_depth_tri_q, m)?)?;
    m.add_function(wrap_pyfunction!(critical_velocity_dh, m)?)?;
    m.add_function(wrap_pyfunction!(critical_slope_n, m)?)?;
    m.add_function(wrap_pyfunction!(boundary_shear_s0, m)?)?;
    m.add_function(wrap_pyfunction!(boundary_shear_rh, m)?)?;
    m.add_function(wrap_pyfunction!(shields_param_tau0, m)?)?;
    m.add_function(wrap_pyfunction!(shields_param_d50, m)?)?;
    m.add_function(wrap_pyfunction!(lane_balance_s, m)?)?;
    m.add_function(wrap_pyfunction!(stokes_settling_d, m)?)?;

    // Dedicated Bidirectional Inversions - Pipe Flow
    m.add_function(wrap_pyfunction!(darcy_weisbach_f, m)?)?;
    m.add_function(wrap_pyfunction!(darcy_weisbach_d, m)?)?;
    m.add_function(wrap_pyfunction!(darcy_weisbach_l, m)?)?;
    m.add_function(wrap_pyfunction!(darcy_weisbach_v, m)?)?;
    m.add_function(wrap_pyfunction!(darcy_weisbach_q, m)?)?;
    m.add_function(wrap_pyfunction!(hazen_williams_q, m)?)?;
    m.add_function(wrap_pyfunction!(hazen_williams_d, m)?)?;
    m.add_function(wrap_pyfunction!(hazen_williams_l, m)?)?;
    m.add_function(wrap_pyfunction!(hazen_williams_c, m)?)?;
    m.add_function(wrap_pyfunction!(hazen_williams_s, m)?)?;
    m.add_function(wrap_pyfunction!(reynolds_v, m)?)?;
    m.add_function(wrap_pyfunction!(reynolds_d, m)?)?;
    m.add_function(wrap_pyfunction!(minor_loss_kl, m)?)?;
    m.add_function(wrap_pyfunction!(minor_loss_v, m)?)?;
    m.add_function(wrap_pyfunction!(joukowsky_dv, m)?)?;
    m.add_function(wrap_pyfunction!(joukowsky_a, m)?)?;
    m.add_function(wrap_pyfunction!(critical_closure_l, m)?)?;
    m.add_function(wrap_pyfunction!(critical_closure_a, m)?)?;
    m.add_function(wrap_pyfunction!(equivalent_pipe_kl, m)?)?;
    m.add_function(wrap_pyfunction!(equivalent_pipe_f, m)?)?;
    m.add_function(wrap_pyfunction!(water_power_q, m)?)?;
    m.add_function(wrap_pyfunction!(water_power_h, m)?)?;
    m.add_function(wrap_pyfunction!(pump_power_pw, m)?)?;
    m.add_function(wrap_pyfunction!(pump_power_eta, m)?)?;

    // Dedicated Bidirectional Inversions - Hydrology
    m.add_function(wrap_pyfunction!(rational_c, m)?)?;
    m.add_function(wrap_pyfunction!(rational_i, m)?)?;
    m.add_function(wrap_pyfunction!(rational_a, m)?)?;
    m.add_function(wrap_pyfunction!(scs_cn_s, m)?)?;
    m.add_function(wrap_pyfunction!(scs_cn_cn, m)?)?;
    m.add_function(wrap_pyfunction!(scs_cn_p, m)?)?;
    m.add_function(wrap_pyfunction!(horton_rate_f0, m)?)?;
    m.add_function(wrap_pyfunction!(horton_rate_fc, m)?)?;
    m.add_function(wrap_pyfunction!(horton_rate_k, m)?)?;
    m.add_function(wrap_pyfunction!(kirpich_s, m)?)?;
    m.add_function(wrap_pyfunction!(kirpich_l, m)?)?;
    m.add_function(wrap_pyfunction!(scs_amc_cnii_from_i, m)?)?;
    m.add_function(wrap_pyfunction!(scs_amc_cnii_from_iii, m)?)?;
    m.add_function(wrap_pyfunction!(tr55_shallow_s, m)?)?;
    m.add_function(wrap_pyfunction!(hargreaves_ra, m)?)?;

    // Dedicated Bidirectional Inversions - Structures
    m.add_function(wrap_pyfunction!(francis_weir_l, m)?)?;
    m.add_function(wrap_pyfunction!(v_notch_weir_h, m)?)?;
    m.add_function(wrap_pyfunction!(v_notch_weir_cd, m)?)?;
    m.add_function(wrap_pyfunction!(v_notch_weir_theta, m)?)?;
    m.add_function(wrap_pyfunction!(broad_crested_weir_h, m)?)?;
    m.add_function(wrap_pyfunction!(broad_crested_weir_l, m)?)?;
    m.add_function(wrap_pyfunction!(orifice_free_h, m)?)?;
    m.add_function(wrap_pyfunction!(orifice_free_ao, m)?)?;
    m.add_function(wrap_pyfunction!(sluice_gate_free_a, m)?)?;
    m.add_function(wrap_pyfunction!(ogee_spillway_he, m)?)?;
    m.add_function(wrap_pyfunction!(ogee_spillway_le, m)?)?;
    m.add_function(wrap_pyfunction!(chute_velocity_z, m)?)?;
    m.add_function(wrap_pyfunction!(stilling_basin_y2, m)?)?;
    m.add_function(wrap_pyfunction!(stilling_basin_y1, m)?)?;

    // Dedicated Bidirectional Inversions - Groundwater
    m.add_function(wrap_pyfunction!(darcy_flow_k, m)?)?;
    m.add_function(wrap_pyfunction!(darcy_flow_dh_dl, m)?)?;
    m.add_function(wrap_pyfunction!(thiem_confined_t, m)?)?;
    m.add_function(wrap_pyfunction!(thiem_confined_dh, m)?)?;
    m.add_function(wrap_pyfunction!(thiem_unconfined_k, m)?)?;
    m.add_function(wrap_pyfunction!(cooper_jacob_q, m)?)?;

    Ok(())
}

