"""
Rigorous Round-Trip Numerical Inversion Test Suite for Project HydroCivil.
Verifies that f^-1(f(x)) == x within 1e-9 tolerance across scalar and vectorized inputs
for all dedicated bidirectional equation families (Approach 1).
"""

import math
import numpy as np
import pytest

import hydroaj as hc


class TestOpenChannelInversions:
    """Tests forward and inverse relationships for open channel flow."""

    def test_manning_roundtrip_scalar(self):
        a = 15.0
        rh = 1.85
        s0 = 0.0015
        n_val = 0.025
        
        # Forward
        q = hc.manning_q(a, rh, s0, n_val)
        assert q > 0.0

        # Inversions
        n_calc = hc.manning_n(q, a, rh, s0)
        s0_calc = hc.manning_s0(q, a, rh, n_val)
        rh_calc = hc.manning_rh(q, a, s0, n_val)
        a_calc = hc.manning_a(q, rh, s0, n_val)

        assert pytest.approx(n_val, rel=1e-9) == n_calc
        assert pytest.approx(s0, rel=1e-9) == s0_calc
        assert pytest.approx(rh, rel=1e-9) == rh_calc
        assert pytest.approx(a, rel=1e-9) == a_calc

        # Aliases
        assert hc.manning_roughness(q, a, rh, s0) == n_calc
        assert hc.manning_slope(q, a, rh, n_val) == s0_calc
        assert hc.manning_hydraulic_radius(q, a, s0, n_val) == rh_calc
        assert hc.manning_area(q, rh, s0, n_val) == a_calc

    def test_manning_roundtrip_vectorized(self):
        a = np.array([5.0, 10.0, 20.0, 50.0])
        rh = np.array([0.8, 1.2, 1.9, 2.8])
        s0 = np.array([0.002, 0.001, 0.0008, 0.0005])
        n_val = np.array([0.015, 0.020, 0.025, 0.030])

        q = hc.manning_q(a, rh, s0, n_val)
        n_calc = hc.manning_n(q, a, rh, s0)
        s0_calc = hc.manning_s0(q, a, rh, n_val)

        np.testing.assert_allclose(n_calc, n_val, rtol=1e-9)
        np.testing.assert_allclose(s0_calc, s0, rtol=1e-9)

    def test_strickler_roundtrip(self):
        rh = 2.1
        s0 = 0.0012
        kst = 45.0

        v = hc.strickler_v(rh, s0, kst)
        kst_calc = hc.strickler_kst(v, rh, s0)
        s0_calc = hc.strickler_s0(v, kst, rh)

        assert pytest.approx(kst, rel=1e-9) == kst_calc
        assert pytest.approx(s0, rel=1e-9) == s0_calc

    def test_chezy_roundtrip(self):
        rh = 1.6
        s0 = 0.0018
        c = 55.0

        v = hc.chezy_v(c, rh, s0)
        c_calc = hc.chezy_c(v, rh, s0)
        s0_calc = hc.chezy_s0(v, c, rh)
        rh_calc = hc.chezy_rh(v, c, s0)

        assert pytest.approx(c, rel=1e-9) == c_calc
        assert pytest.approx(s0, rel=1e-9) == s0_calc
        assert pytest.approx(rh, rel=1e-9) == rh_calc

    def test_froude_roundtrip(self):
        v = 3.5
        dh = 1.25

        fr = hc.froude_fr(v, dh)
        v_calc = hc.froude_v(fr, dh)
        dh_calc = hc.froude_dh(fr, v)

        assert pytest.approx(v, rel=1e-9) == v_calc
        assert pytest.approx(dh, rel=1e-9) == dh_calc

    def test_specific_energy_roundtrip(self):
        y = 1.8
        v = 2.4

        e = hc.specific_energy_e(y, v)
        v_calc = hc.specific_energy_v(e, y)

        assert pytest.approx(v, rel=1e-9) == v_calc

    def test_hydraulic_jump_roundtrip(self):
        y1 = 0.6
        fr1 = 4.5

        y2 = hc.hydraulic_jump_y2(y1, fr1)
        fr1_calc = hc.hydraulic_jump_fr1(y1, y2)
        y1_calc = hc.hydraulic_jump_y1(y2, fr1)

        assert pytest.approx(fr1, rel=1e-9) == fr1_calc
        assert pytest.approx(y1, rel=1e-9) == y1_calc

    def test_critical_depth_rectangular_roundtrip(self):
        q = 25.0
        b = 6.0

        yc = hc.critical_depth_rect_yc(q, b)
        q_calc = hc.critical_depth_rect_q(yc, b)

        assert pytest.approx(q, rel=1e-9) == q_calc

    def test_critical_depth_triangular_roundtrip(self):
        q = 8.5
        z = 1.5

        yc = hc.critical_depth_tri_yc(q, z)
        q_calc = hc.critical_depth_tri_q(yc, z)

        assert pytest.approx(q, rel=1e-9) == q_calc


class TestPipeFlowInversions:
    """Tests forward and inverse relationships for pressurized pipe flow."""

    def test_darcy_weisbach_roundtrip_scalar(self):
        f = 0.022
        l = 500.0
        d = 0.40
        v = 2.1

        hf = hc.darcy_weisbach_hf(f, l, d, v)
        f_calc = hc.darcy_weisbach_f(hf, l, d, v)
        d_calc = hc.darcy_weisbach_d(hf, f, l, v)
        l_calc = hc.darcy_weisbach_l(hf, f, d, v)
        v_calc = hc.darcy_weisbach_v(hf, f, l, d)

        assert pytest.approx(f, rel=1e-9) == f_calc
        assert pytest.approx(d, rel=1e-9) == d_calc
        assert pytest.approx(l, rel=1e-9) == l_calc
        assert pytest.approx(v, rel=1e-9) == v_calc

        # Discharge forward/inverse check
        q = (math.pi * d**2 / 4.0) * v
        q_calc = hc.darcy_weisbach_q(hf, f, l, d)
        assert pytest.approx(q, rel=1e-9) == q_calc

    def test_darcy_weisbach_roundtrip_vectorized(self):
        f = np.array([0.015, 0.020, 0.028])
        l = np.array([200.0, 450.0, 1000.0])
        d = np.array([0.25, 0.50, 1.0])
        v = np.array([1.5, 2.2, 3.0])

        hf = hc.darcy_weisbach_hf(f, l, d, v)
        f_calc = hc.darcy_weisbach_f(hf, l, d, v)
        v_calc = hc.darcy_weisbach_v(hf, f, l, d)

        np.testing.assert_allclose(f_calc, f, rtol=1e-9)
        np.testing.assert_allclose(v_calc, v, rtol=1e-9)

    def test_hazen_williams_roundtrip(self):
        c = 130.0
        d = 0.35
        l = 600.0
        q = 0.15

        hf = hc.hazen_williams_hf(c, d, l, q)
        q_calc = hc.hazen_williams_q(hf, c, d, l)
        d_calc = hc.hazen_williams_d(hf, q, c, l)
        l_calc = hc.hazen_williams_l(hf, q, c, d)
        c_calc = hc.hazen_williams_c(hf, q, d, l)

        assert pytest.approx(q, rel=1e-9) == q_calc
        assert pytest.approx(d, rel=1e-9) == d_calc
        assert pytest.approx(l, rel=1e-9) == l_calc
        assert pytest.approx(c, rel=1e-9) == c_calc

    def test_reynolds_roundtrip(self):
        v = 2.4
        d = 0.30
        nu = 1.004e-6

        re = hc.reynolds_re(v, d, nu)
        v_calc = hc.reynolds_v(re, d, nu)
        d_calc = hc.reynolds_d(re, v, nu)

        assert pytest.approx(v, rel=1e-9) == v_calc
        assert pytest.approx(d, rel=1e-9) == d_calc

    def test_minor_loss_roundtrip(self):
        kl = 2.5
        v = 1.8

        hm = hc.minor_loss_hm(kl, v)
        kl_calc = hc.minor_loss_kl(hm, v)
        v_calc = hc.minor_loss_v(hm, kl)

        assert pytest.approx(kl, rel=1e-9) == kl_calc
        assert pytest.approx(v, rel=1e-9) == v_calc

    def test_joukowsky_roundtrip(self):
        a = 1200.0
        dv = 1.5
        rho = 1000.0

        dp = hc.joukowsky_dp(a, dv, rho)
        dv_calc = hc.joukowsky_dv(dp, a, rho)
        a_calc = hc.joukowsky_a(dp, dv, rho)

        assert pytest.approx(dv, rel=1e-9) == dv_calc
        assert pytest.approx(a, rel=1e-9) == a_calc

    def test_critical_closure_roundtrip(self):
        l = 800.0
        a = 1100.0

        tc = hc.critical_closure_tc(l, a)
        l_calc = hc.critical_closure_l(tc, a)
        a_calc = hc.critical_closure_a(tc, l)

        assert pytest.approx(l, rel=1e-9) == l_calc
        assert pytest.approx(a, rel=1e-9) == a_calc

    def test_water_power_roundtrip(self):
        q = 0.25
        h = 45.0

        pw = hc.water_power_pw(q, h)
        q_calc = hc.water_power_q(pw, h)
        h_calc = hc.water_power_h(pw, q)

        assert pytest.approx(q, rel=1e-9) == q_calc
        assert pytest.approx(h, rel=1e-9) == h_calc

    def test_pump_power_roundtrip(self):
        pw = 110.0
        eta = 0.82

        pb = hc.pump_power_pb(pw, eta)
        pw_calc = hc.pump_power_pw(pb, eta)
        eta_calc = hc.pump_power_eta(pw, pb)

        assert pytest.approx(pw, rel=1e-9) == pw_calc
        assert pytest.approx(eta, rel=1e-9) == eta_calc


class TestHydrologyInversions:
    """Tests forward and inverse relationships for catchment hydrology."""

    def test_rational_roundtrip(self):
        c = 0.65
        i = 45.0
        a = 12.0

        q = hc.rational_q(c, i, a)
        c_calc = hc.rational_c(q, i, a)
        i_calc = hc.rational_i(q, c, a)
        a_calc = hc.rational_a(q, c, i)

        assert pytest.approx(c, rel=1e-9) == c_calc
        assert pytest.approx(i, rel=1e-9) == i_calc
        assert pytest.approx(a, rel=1e-9) == a_calc

    def test_scs_cn_retention_and_p_roundtrip(self):
        cn = 78.0
        s = hc.scs_cn_s(cn)
        cn_calc = hc.scs_cn_cn(s)
        assert pytest.approx(cn, rel=1e-9) == cn_calc

        p = 85.0
        q = hc.scs_cn_q(p, s)
        p_calc = hc.scs_cn_p(q, s)
        assert pytest.approx(p, rel=1e-9) == p_calc

    def test_horton_roundtrip(self):
        f0 = 50.0
        fc = 10.0
        k = 1.2
        t = 1.5

        fp = hc.horton_rate_fp(f0, fc, k, t)
        f0_calc = hc.horton_rate_f0(fp, fc, k, t)
        fc_calc = hc.horton_rate_fc(fp, f0, k, t)
        k_calc = hc.horton_rate_k(fp, f0, fc, t)

        assert pytest.approx(f0, rel=1e-9) == f0_calc
        assert pytest.approx(fc, rel=1e-9) == fc_calc
        assert pytest.approx(k, rel=1e-9) == k_calc

    def test_kirpich_roundtrip(self):
        l = 1500.0
        s = 0.02

        tc = hc.kirpich_tc(l, s)
        s_calc = hc.kirpich_s(tc, l)
        l_calc = hc.kirpich_l(tc, s)

        assert pytest.approx(s, rel=1e-9) == s_calc
        assert pytest.approx(l, rel=1e-9) == l_calc

    def test_scs_amc_roundtrip(self):
        cn_ii = 75.0
        cn_i = hc.scs_amc_cni(cn_ii)
        cn_ii_from_i = hc.scs_amc_cnii_from_i(cn_i)
        assert pytest.approx(cn_ii, rel=1e-9) == cn_ii_from_i

        cn_iii = hc.scs_amc_cniii(cn_ii)
        cn_ii_from_iii = hc.scs_amc_cnii_from_iii(cn_iii)
        assert pytest.approx(cn_ii, rel=1e-9) == cn_ii_from_iii

    def test_tr55_shallow_roundtrip(self):
        s = 0.035
        v = hc.tr55_shallow_v(s, surface_type="unpaved")
        s_calc = hc.tr55_shallow_s(v, surface_type="unpaved")
        assert pytest.approx(s, rel=1e-9) == s_calc

    def test_hargreaves_roundtrip(self):
        tm = 22.0
        tmx = 30.0
        tmn = 14.0
        ra = 15.2

        et0 = hc.hargreaves_et0(tm, tmx, tmn, ra)
        ra_calc = hc.hargreaves_ra(et0, tm, tmx, tmn)
        assert pytest.approx(ra, rel=1e-9) == ra_calc


class TestStructuresAndGroundwaterInversions:
    """Tests forward and inverse relationships for structures, groundwater, and sediments."""

    def test_francis_weir_roundtrip(self):
        l = 4.5
        h = 0.65
        ne = 2.0

        q = hc.francis_weir_q(l, h, ne)
        l_calc = hc.francis_weir_l(q, h, ne)
        assert pytest.approx(l, rel=1e-9) == l_calc

    def test_v_notch_weir_roundtrip(self):
        theta_deg = 90.0
        h = 0.45
        cd = 0.585

        q = hc.v_notch_weir_q(theta_deg, h, cd)
        h_calc = hc.v_notch_weir_h(q, theta_deg, cd)
        cd_calc = hc.v_notch_weir_cd(q, theta_deg, h)
        theta_calc = hc.v_notch_weir_theta(q, h, cd)

        assert pytest.approx(h, rel=1e-9) == h_calc
        assert pytest.approx(cd, rel=1e-9) == cd_calc
        assert pytest.approx(theta_deg, rel=1e-9) == theta_calc

    def test_broad_crested_weir_roundtrip(self):
        l = 5.0
        h = 0.8
        cd = 0.848

        q = hc.broad_crested_weir_q(l, h, cd)
        h_calc = hc.broad_crested_weir_h(q, l, cd)
        l_calc = hc.broad_crested_weir_l(q, h, cd)

        assert pytest.approx(h, rel=1e-9) == h_calc
        assert pytest.approx(l, rel=1e-9) == l_calc

    def test_orifice_free_roundtrip(self):
        ao = 0.08
        h = 2.5
        cd = 0.62

        q = hc.orifice_free_q(ao, h, cd)
        h_calc = hc.orifice_free_h(q, ao, cd)
        ao_calc = hc.orifice_free_ao(q, h, cd)

        assert pytest.approx(h, rel=1e-9) == h_calc
        assert pytest.approx(ao, rel=1e-9) == ao_calc

    def test_sluice_gate_free_roundtrip(self):
        b = 3.0
        a = 0.4
        y1 = 2.2
        cd = 0.60

        q = hc.sluice_gate_free_q(b, a, y1, cd)
        a_calc = hc.sluice_gate_free_a(q, b, y1, cd)

        assert pytest.approx(a, rel=1e-9) == a_calc

    def test_darcy_flow_roundtrip(self):
        k = 1.5e-4
        a = 250.0
        grad = -0.005

        q = hc.darcy_flow_q(k, a, grad)
        k_calc = hc.darcy_flow_k(q, a, grad)
        grad_calc = hc.darcy_flow_dh_dl(q, k, a)

        assert pytest.approx(k, rel=1e-9) == k_calc
        assert pytest.approx(grad, rel=1e-9) == grad_calc

    def test_thiem_confined_roundtrip(self):
        t = 0.015
        h1 = 45.0
        h2 = 48.5
        r1 = 10.0
        r2 = 100.0

        q = hc.thiem_confined_q(t, h1, h2, r1, r2)
        t_calc = hc.thiem_confined_t(q, h1, h2, r1, r2)
        dh_calc = hc.thiem_confined_dh(q, t, r1, r2)

        assert pytest.approx(t, rel=1e-9) == t_calc
        assert pytest.approx(h2 - h1, rel=1e-9) == dh_calc

    def test_thiem_unconfined_roundtrip(self):
        k = 2.5e-4
        h1 = 18.0
        h2 = 22.0
        r1 = 5.0
        r2 = 50.0

        q = hc.thiem_unconfined_q(k, h1, h2, r1, r2)
        k_calc = hc.thiem_unconfined_k(q, h1, h2, r1, r2)

        assert pytest.approx(k, rel=1e-9) == k_calc

    def test_cooper_jacob_roundtrip(self):
        q = 0.035
        t = 0.012
        stor = 0.0005
        r = 30.0
        time_val = 86400.0

        s = hc.cooper_jacob_s(q, t, stor, r, time_val)
        q_calc = hc.cooper_jacob_q(s, t, stor, r, time_val)

        assert pytest.approx(q, rel=1e-9) == q_calc

    def test_boundary_shear_roundtrip(self):
        gam = 9806.65
        rh = 1.4
        s0 = 0.002

        tau0 = hc.boundary_shear_tau0(gam, rh, s0)
        s0_calc = hc.boundary_shear_s0(tau0, gam, rh)
        rh_calc = hc.boundary_shear_rh(tau0, gam, s0)

        assert pytest.approx(s0, rel=1e-9) == s0_calc
        assert pytest.approx(rh, rel=1e-9) == rh_calc

    def test_shields_parameter_roundtrip(self):
        tau0 = 35.0
        gs = 2650.0 * 9.80665
        gw = 1000.0 * 9.80665
        d50 = 0.025

        theta = hc.shields_param_theta(tau0, gs - gw, d50)
        tau0_calc = hc.shields_param_tau0(theta, gs, gw, d50)
        d50_calc = hc.shields_param_d50(theta, tau0, gs, gw)

        assert pytest.approx(tau0, rel=1e-9) == tau0_calc
        assert pytest.approx(d50, rel=1e-9) == d50_calc

    def test_lane_balance_roundtrip(self):
        qw = 45.0
        s = 0.0018
        d50 = 0.015

        qs = hc.lane_balance_qs(qw, s, d50)
        s_calc = hc.lane_balance_s(qs, d50, qw)

        assert pytest.approx(s, rel=1e-9) == s_calc

    def test_stokes_settling_roundtrip(self):
        d = 0.0001
        ss = 2.65
        nu = 1.004e-6

        ws = hc.stokes_settling_ws(d, ss, nu)
        d_calc = hc.stokes_settling_d(ws, ss, nu)

        assert pytest.approx(d, rel=1e-9) == d_calc

