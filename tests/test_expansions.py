"""
Comprehensive Unit Tests for HydroCivil Expansion Functions (Formulas 63 - 110).
Covers Optimal Sections, Jump Efficiency, Culverts, Pipe Networks, Spillways,
Sediment Transport & Advanced Hydrology.
"""

import numpy as np
import pytest

from hydroaj import (
    optimal_rectangular_section,
    optimal_trapezoidal_section,
    optimal_triangular_section,
    critical_velocity,
    critical_slope,
    gravity_wave_celerity,
    hydraulic_jump_efficiency,
    hydraulic_jump_height,
    critical_depth_triangular,
    horton_einstein_composite_n,
    pavlovskii_composite_n,
    culvert_inlet_unsubmerged,
    culvert_inlet_submerged,
    culvert_outlet_control_head,
    culvert_entrance_loss,
    hardy_cross_correction,
    equivalent_pipe_length,
    equivalent_diameter_series,
    parallel_pipes_distribution,
    water_horsepower,
    pump_brake_power,
    ogee_spillway_discharge,
    ogee_discharge_coefficient,
    spillway_effective_length,
    chute_terminal_velocity,
    stilling_basin_length,
    morning_glory_weir_flow,
    siphon_spillway_discharge,
    drop_structure_depth,
    tailwater_depth,
    boundary_shear_stress,
    shear_velocity,
    shields_parameter,
    critical_shear_stress,
    lane_sediment_balance,
    meyer_peter_muller_bedload,
    rubey_settling_velocity,
    stokes_settling_velocity,
    scs_composite_cn,
    scs_cn_amc_i,
    scs_cn_amc_iii,
    tr55_sheet_flow_time,
    tr55_shallow_concentrated_velocity,
    gumbel_flood_frequency,
    nash_cascade_iuh,
    hargreaves_samani_et0,
    net_radiation_equivalent_evap,
    time_area_runoff_step,
)


def test_optimal_sections():
    # Rectangular: y=2 -> b=4, A=8, P=8, Rh=1
    b, a, p, rh = optimal_rectangular_section(2.0)
    assert pytest.approx(b) == 4.0
    assert pytest.approx(a) == 8.0
    assert pytest.approx(p) == 8.0
    assert pytest.approx(rh) == 1.0

    # Trapezoidal: y=3 -> Rh=1.5
    b_t, m_t, rh_t = optimal_trapezoidal_section(3.0)
    assert pytest.approx(m_t) == 1.0 / np.sqrt(3.0)
    assert pytest.approx(rh_t) == 1.5

    # Triangular: y=2 -> A=4
    a_tri, p_tri, rh_tri = optimal_triangular_section(2.0)
    assert pytest.approx(a_tri) == 4.0
    assert pytest.approx(p_tri) == 2.0 * np.sqrt(2.0) * 2.0


def test_open_channel_expansions():
    # Critical velocity: Dh=4, g=9.80665 -> sqrt(9.80665 * 4) = 6.263
    vc = critical_velocity(4.0, system="si")
    assert pytest.approx(vc, rel=1e-3) == np.sqrt(9.80665 * 4.0)

    # Jump efficiency: Fr=2
    eff = hydraulic_jump_efficiency(2.0)
    assert 0.0 < eff < 1.0

    # Jump height: y1=0.5, y2=2.5 -> hj=2.0
    assert pytest.approx(hydraulic_jump_height(0.5, 2.5)) == 2.0

    # Triangular critical depth: Q=10, m=1.5, g=9.80665
    yc = critical_depth_triangular(10.0, 1.5, system="si")
    assert yc > 0.0

    # Composite roughness
    p_arr = [10.0, 5.0]
    n_arr = [0.025, 0.040]
    n_he = horton_einstein_composite_n(p_arr, n_arr)
    n_pav = pavlovskii_composite_n(p_arr, n_arr)
    assert 0.025 <= n_he <= 0.040
    assert 0.025 <= n_pav <= 0.040


def test_culverts_and_pipes():
    # Entrance loss
    he = culvert_entrance_loss(0.5, 3.0, system="si")
    assert pytest.approx(he, rel=1e-3) == 0.5 * 9.0 / (2.0 * 9.80665)

    # Equivalent length: KL=2.0, D=0.5, f=0.02 -> 2.0 * 0.5 / 0.02 = 50.0
    le = equivalent_pipe_length(2.0, 0.5, 0.02)
    assert pytest.approx(le) == 50.0

    # Water power: Q=1.0 m3/s, H=10.0 m, gamma=9806.65 N/m3 -> 98.0665 kW
    pw = water_horsepower(1.0, 10.0, system="si")
    assert pytest.approx(pw, rel=1e-3) == 98.0665

    # Brake power: Pw=98.0665, eta=0.8 -> 122.58 kW
    pb = pump_brake_power(pw, 0.8)
    assert pytest.approx(pb, rel=1e-3) == 98.0665 / 0.8


def test_structures_and_spillways():
    # Ogee spillway: Co=2.1, Le=50, He=4 -> 840.0
    q_ogee = ogee_spillway_discharge(2.1, 50.0, 4.0)
    assert pytest.approx(q_ogee) == 840.0

    # Effective length: L=50, N=2, Kp=0.02, Ka=0.1, He=4.0
    # Contraction = 2 * (2*0.02 + 0.1) * 4 = 2 * 0.14 * 4 = 1.12 -> Le = 48.88
    le = spillway_effective_length(50.0, 2.0, 0.02, 0.1, 4.0)
    assert pytest.approx(le) == 48.88

    # Stilling basin: y2=3.0, k=4.3 -> L=12.9
    lsb = stilling_basin_length(3.0, 4.3)
    assert pytest.approx(lsb) == 12.9


def test_sediment_mechanics():
    # Boundary shear stress: gamma=9806.65, Rh=2.0, S=0.001 -> 19.613 Pa
    tau = boundary_shear_stress(9806.65, 2.0, 0.001)
    assert pytest.approx(tau, rel=1e-3) == 19.6133

    # Shields parameter: tau=10, dg=16000, d50=0.002 -> 0.3125
    th = shields_parameter(10.0, 16000.0, 0.002)
    assert pytest.approx(th) == 0.3125

    # MPM bedload
    qb = meyer_peter_muller_bedload(0.1)
    assert pytest.approx(qb, rel=1e-3) == 8.0 * (0.1 - 0.047)**1.5

    # Stokes settling: d=1e-4, Ss=2.65, nu=1e-6, g=9.80665
    ws = stokes_settling_velocity(1e-4, 2.65, 1e-6, system="si")
    expected_ws = (9.80665 * 1.65 * 1e-8) / (18.0 * 1e-6)
    assert pytest.approx(ws, rel=1e-3) == expected_ws


def test_hydrology_expansions():
    # Composite CN: 40 ha at 70, 60 ha at 80 -> (40*70 + 60*80)/100 = 76.0
    cn_comp = scs_composite_cn([40.0, 60.0], [70.0, 80.0])
    assert pytest.approx(cn_comp) == 76.0

    # AMC conversions: CN_II=80 -> CN_I and CN_III
    cn1 = scs_cn_amc_i(80.0)
    cn3 = scs_cn_amc_iii(80.0)
    assert cn1 < 80.0 < cn3

    # Gumbel flood frequency
    xf = gumbel_flood_frequency(500.0, 150.0, 100.0)
    assert xf > 500.0

    # Hargreaves ET0
    et0 = hargreaves_samani_et0(15.0, 25.0, 32.0, 18.0)
    assert et0 > 0.0

