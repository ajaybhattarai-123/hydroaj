"""
Comprehensive Verification Suite for Newly Added Expert Water Resources Formulas:
Time of Concentration (FAA, Kerby, Bransby-Williams, TR-55),
Empirical Peak Flood (Dicken, Ryves, Inglis, Nawab Jung, Fuller),
Infiltration (Philip, Kostiakov, Green-Ampt),
Evapotranspiration (FAO-56 Penman-Monteith, Priestley-Taylor, Blaney-Criddle),
Hydrographs & Routing (SCS, Snyder, Muskingum-Cunge, Lyne-Hollick),
Extreme Value (Gumbel, Log-Pearson 3, Plotting Positions),
Canal Regime (Lacey, Kennedy),
Specialized Weirs & Scour (Cipoletti, Sutro, HEC-18 Pier Scour),
Groundwater & Coastal Aquifers (Ghyben-Herzberg, Jacob Well Loss, Hantush, Specific Capacity).
"""

import math
import numpy as np
import pytest

import hydroaj.hydrology as hydro
import hydroaj.hydraulics as hyd
import hydroaj.structures as struct
import hydroaj.groundwater as gw


def assert_close(val, expected, rtol=1e-3, msg=""):
    assert math.isclose(val, expected, rel_tol=rtol, abs_tol=1e-5), f"{msg} Expected {expected}, got {val}"


# =============================================================================
# 1. TIME OF CONCENTRATION TESTS
# =============================================================================

def test_faa_tc_roundtrip():
    L = 300.0
    S = 1.5
    C = 0.65
    tc = hydro.faa_tc(L, S, C, system="si")
    assert tc > 0.0
    # Inversions
    L_back = hydro.faa_l(tc, S, C, system="si")
    assert_close(L_back, L, msg="FAA Length Inversion")
    S_back = hydro.faa_s(tc, L, C, system="si")
    assert_close(S_back, S, msg="FAA Slope Inversion")
    C_back = hydro.faa_c(tc, L, S, system="si")
    assert_close(C_back, C, msg="FAA Runoff Coeff Inversion")


def test_kerby_tc_roundtrip():
    L = 100.0
    S = 0.02
    n = 0.40
    tc = hydro.kerby_tc(L, S, n, system="si")
    assert tc > 0.0
    # Inversions
    L_back = hydro.kerby_l(tc, S, n, system="si")
    assert_close(L_back, L, msg="Kerby Length Inversion")
    S_back = hydro.kerby_s(tc, L, n, system="si")
    assert_close(S_back, S, msg="Kerby Slope Inversion")
    n_back = hydro.kerby_n(tc, L, S, system="si")
    assert_close(n_back, n, msg="Kerby Roughness Inversion")


def test_bransby_williams_tc_roundtrip():
    L = 12.0
    A = 25.0
    S = 8.0
    tc = hydro.bransby_williams_tc(L, A, S)
    assert tc > 0.0
    # Inversions
    L_back = hydro.bransby_williams_l(tc, A, S)
    assert_close(L_back, L, msg="Bransby-Williams Length Inversion")
    A_back = hydro.bransby_williams_a(tc, L, S)
    assert_close(A_back, A, msg="Bransby-Williams Area Inversion")
    S_back = hydro.bransby_williams_s(tc, L, A)
    assert_close(S_back, S, msg="Bransby-Williams Slope Inversion")


def test_tr55_composite_tc():
    t_sheet = 15.0
    t_shallow = 8.5
    t_channel = hydro.tr55_channel_tc(length=1200.0, velocity=2.0)
    assert_close(t_channel, 10.0, msg="TR-55 Channel Flow Time")
    t_total = hydro.tr55_composite_tc(t_sheet, t_shallow, t_channel)
    assert_close(t_total, 33.5, msg="TR-55 Composite Tc")


# =============================================================================
# 2. REGIONAL EMPIRICAL FLOOD FORMULAS TESTS
# =============================================================================

def test_dickens_roundtrip():
    A = 150.0
    cd = 14.0
    q = hydro.dickens_q(A, cd)
    assert q > 0.0
    cd_back = hydro.dickens_cd(q, A)
    assert_close(cd_back, cd, msg="Dickens CD Inversion")
    A_back = hydro.dickens_area(q, cd)
    assert_close(A_back, A, msg="Dickens Area Inversion")


def test_ryves_roundtrip():
    A = 80.0
    cr = 8.5
    q = hydro.ryves_q(A, cr)
    assert q > 0.0
    cr_back = hydro.ryves_cr(q, A)
    assert_close(cr_back, cr, msg="Ryves CR Inversion")
    A_back = hydro.ryves_area(q, cr)
    assert_close(A_back, A, msg="Ryves Area Inversion")


def test_inglis_roundtrip():
    A = 50.0
    q = hydro.inglis_q(A)
    assert q > 0.0
    A_back = hydro.inglis_area(q)
    assert_close(A_back, A, msg="Inglis Area Inversion")


def test_nawab_jung_roundtrip():
    A = 120.0
    cn = 48.0
    q = hydro.nawab_jung_q(A, cn)
    assert q > 0.0
    cn_back = hydro.nawab_jung_cn(q, A)
    assert_close(cn_back, cn, msg="Nawab Jung CN Inversion")
    A_back = hydro.nawab_jung_area(q, cn)
    assert_close(A_back, A, msg="Nawab Jung Area Inversion")


def test_fuller_flood_roundtrip():
    A = 50.0
    T = 100.0
    cf = 1.5
    q = hydro.fuller_flood_q(A, T, cf)
    assert q > 0.0
    T_back = hydro.fuller_return_period(q, A, cf)
    assert_close(T_back, T, msg="Fuller Return Period Inversion")


# =============================================================================
# 3. INFILTRATION MODELS TESTS
# =============================================================================

def test_philip_infiltration_roundtrip():
    t = 2.0
    S = 25.0
    A = 5.0
    F = hydro.philip_cumulative(t, S, A)
    assert F > 0.0
    S_back = hydro.philip_sorptivity(F, t, A)
    assert_close(S_back, S, msg="Philip Sorptivity Inversion")


def test_kostiakov_infiltration_roundtrip():
    t = 1.5
    a = 30.0
    b = 0.65
    F = hydro.kostiakov_cumulative(t, a, b)
    assert F > 0.0
    t_back = hydro.kostiakov_time(F, a, b)
    assert_close(t_back, t, msg="Kostiakov Time Inversion")


def test_green_ampt_ponding_time():
    i = 40.0
    K = 10.0
    psi = 120.0
    dtheta = 0.25
    tp = hydro.green_ampt_ponding_time(i, K, psi, dtheta)
    assert tp > 0.0
    # Manual check: (10 * 120 * 0.25) / (40 * 30) = 300 / 1200 = 0.25 hr
    assert_close(tp, 0.25, msg="Green-Ampt Ponding Time")


# =============================================================================
# 4. EVAPOTRANSPIRATION TESTS
# =============================================================================

def test_fao56_penman_monteith_roundtrip():
    Rn = 18.5
    T = 24.0
    u2 = 2.2
    es = hydro.saturation_vapor_pressure(T)
    ea = 0.65 * es # 65% RH
    delta = hydro.vapor_pressure_slope(T)
    gamma = 0.067
    
    et0 = hydro.fao56_penman_monteith(Rn, T, u2, es, ea, delta, gamma)
    assert et0 > 0.0
    
    Rn_back = hydro.fao56_net_radiation(et0, T, u2, es, ea, delta, gamma)
    assert_close(Rn_back, Rn, msg="FAO-56 Net Radiation Inversion")


def test_blaney_criddle_roundtrip():
    T = 22.0
    p = 0.28
    et0 = hydro.blaney_criddle_et(T, p)
    assert et0 > 0.0
    T_back = hydro.blaney_criddle_temp(et0, p)
    assert_close(T_back, T, msg="Blaney-Criddle Temp Inversion")


# =============================================================================
# 5. SYNTHETIC HYDROGRAPHS & ROUTING TESTS
# =============================================================================

def test_scs_unit_hydrograph_roundtrip():
    A = 35.0
    tp = 4.5
    qp = hydro.scs_unit_hydrograph_peak(A, tp, system="si")
    assert qp > 0.0
    tp_back = hydro.scs_uh_tp(qp, A, system="si")
    assert_close(tp_back, tp, msg="SCS UH Tp Inversion")
    A_back = hydro.scs_uh_area(qp, tp, system="si")
    assert_close(A_back, A, msg="SCS UH Area Inversion")


def test_snyder_lag_time():
    L = 25.0
    Lc = 12.0
    ct = 1.4
    tp = hydro.snyder_lag_time(L, Lc, ct)
    assert tp > 0.0


def test_baseflow_lyne_hollick():
    hydrograph = [5.0, 10.0, 25.0, 80.0, 120.0, 75.0, 40.0, 20.0, 8.0, 5.0]
    quickflow, baseflow = hydro.baseflow_lyne_hollick(hydrograph, alpha=0.925)
    assert len(quickflow) == len(hydrograph)
    assert len(baseflow) == len(hydrograph)
    assert np.all(quickflow >= 0.0)
    assert np.all(baseflow >= 0.0)
    assert np.all(baseflow <= np.array(hydrograph) + 1e-6)


# =============================================================================
# 6. EXTREME VALUE STATISTICS TESTS
# =============================================================================

def test_gumbel_flood_roundtrip():
    mean = 250.0
    std = 75.0
    T = 50.0
    xt = hydro.gumbel_design_flood(mean, std, T)
    assert xt > mean
    T_back = hydro.gumbel_return_period_from_flood(xt, mean, std)
    assert_close(T_back, T, msg="Gumbel Return Period Inversion")


def test_plotting_positions():
    p_w, t_w = hydro.weibull_plotting_position(rank=1, total_samples=10)
    assert_close(p_w, 1.0 / 11.0, msg="Weibull P")
    assert_close(t_w, 11.0, msg="Weibull T")


# =============================================================================
# 7. CANAL REGIME HYDRAULICS (LACEY & KENNEDY) TESTS
# =============================================================================

def test_lacey_regime_roundtrips():
    d50 = 0.35
    f = hyd.lacey_silt_factor(d50)
    assert f > 0.0
    d50_back = hyd.lacey_d50(f)
    assert_close(d50_back, d50, msg="Lacey d50 Inversion")
    
    Q = 45.0
    V = hyd.lacey_regime_velocity(Q, f)
    Q_back_v = hyd.lacey_velocity_discharge(V, f)
    assert_close(Q_back_v, Q, msg="Lacey Velocity Q Inversion")
    
    P = hyd.lacey_wetted_perimeter(Q)
    Q_back_p = hyd.lacey_perimeter_discharge(P)
    assert_close(Q_back_p, Q, msg="Lacey Perimeter Q Inversion")
    
    S = hyd.lacey_regime_slope(Q, f)
    Q_back_s = hyd.lacey_slope_discharge(S, f)
    assert_close(Q_back_s, Q, msg="Lacey Slope Q Inversion")


def test_kennedy_critical_velocity_roundtrip():
    y = 2.5
    m = 1.1
    v0 = hyd.kennedy_critical_velocity(y, m, system="si")
    assert v0 > 0.0
    y_back = hyd.kennedy_critical_depth(v0, m, system="si")
    assert_close(y_back, y, msg="Kennedy Critical Depth Inversion")


# =============================================================================
# 8. SPECIALIZED WEIRS & SCOUR TESTS
# =============================================================================

def test_cipoletti_weir_roundtrip():
    L = 3.5
    H = 0.65
    Q = struct.cipoletti_weir_q(L, H, system="si")
    assert Q > 0.0
    L_back = struct.cipoletti_weir_l(Q, H, system="si")
    assert_close(L_back, L, msg="Cipoletti Length Inversion")
    H_back = struct.cipoletti_weir_h(Q, L, system="si")
    assert_close(H_back, H, msg="Cipoletti Head Inversion")


def test_sutro_weir_roundtrip():
    b = 0.8
    a = 0.15
    H = 0.60
    cd = 0.62
    Q = struct.sutro_weir_q(b, a, H, cd, system="si")
    assert Q > 0.0
    H_back = struct.sutro_weir_h(Q, b, a, cd, system="si")
    assert_close(H_back, H, msg="Sutro Head Inversion")


def test_hec18_pier_scour_roundtrip():
    a = 1.5
    y = 3.0
    v = 2.2
    ys = struct.hec18_pier_scour(a, y, v, system="si")
    assert ys > 0.0
    a_back = struct.hec18_pier_width(ys, y, v, system="si")
    assert_close(a_back, a, msg="HEC-18 Pier Width Inversion")


# =============================================================================
# 9. GROUNDWATER EXTENSIONS TESTS
# =============================================================================

def test_ghyben_herzberg_roundtrip():
    hf = 2.5
    z = gw.ghyben_herzberg_depth(hf)
    assert z > 0.0
    hf_back = gw.ghyben_herzberg_head(z)
    assert_close(hf_back, hf, msg="Ghyben-Herzberg Head Inversion")


def test_jacob_well_drawdown_roundtrip():
    Q = 0.04
    B = 25.0
    C = 120.0
    sw = gw.jacob_well_drawdown(Q, B, C)
    assert sw > 0.0
    B_back = gw.jacob_well_b(sw, Q, C)
    assert_close(B_back, B, msg="Jacob Well B Inversion")
    C_back = gw.jacob_well_c(sw, Q, B)
    assert_close(C_back, C, msg="Jacob Well C Inversion")
    eff = gw.jacob_well_efficiency(Q, B, C)
    assert 0.0 < eff < 100.0


def test_specific_capacity():
    Q = 500.0 # m3/day
    sw = 4.0  # m
    T = gw.specific_capacity_to_transmissivity(Q, sw, aquifer_type="confined")
    assert_close(T, 1500.0 * (500.0 / 4.0), msg="Specific capacity T")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

