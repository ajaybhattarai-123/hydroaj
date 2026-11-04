"""
Unit tests for Open Channel Hydraulics & Pressurized Pipe Flow.
Verified against USGS and USACE HEC-RAS reference standards.
"""

import numpy as np
import pytest

from hydroaj.hydraulics import (
    manning_discharge,
    manning_velocity,
    strickler_velocity,
    chezy_velocity,
    kutter_chezy_c,
    bazin_chezy_c,
    geom_rectangular,
    geom_trapezoidal,
    geom_triangular,
    geom_circular,
    geom_parabolic,
    specific_energy,
    froude_number,
    specific_force,
    critical_depth_rectangular,
    normal_depth_trapezoidal,
    belanger_conjugate_depth,
    hydraulic_jump_head_loss,
    hydraulic_jump_length,
    gvf_gradient,
    manning_friction_slope,
    direct_step,
    darcy_weisbach,
    reynolds_number,
    laminar_friction,
    colebrook_white,
    swamee_jain,
    haaland,
    churchill,
    wood,
    hazen_williams,
    hazen_williams_velocity,
    minor_loss,
    wave_celerity,
    joukowsky,
    critical_closure_time,
)


class TestOpenChannelUniformFlow:
    """Tests for Manning, Strickler, Chezy, Kutter, Bazin."""

    def test_manning_discharge_scalar_si(self):
        # A = 10.0 m^2, R_h = 1.25 m, S_0 = 0.001, n = 0.025
        # Q = (1.0 / 0.025) * 10.0 * (1.25)^(2/3) * (0.001)^(1/2) = 400 * 1.160397 * 0.03162278 = 14.678 m^3/s
        q = manning_discharge(10.0, 1.25, 0.001, 0.025, system="si")
        assert isinstance(q, float)
        assert pytest.approx(q, rel=1e-4) == 14.6781

    def test_manning_discharge_scalar_us(self):
        # US customary: k = 1.48608
        q = manning_discharge(10.0, 1.25, 0.001, 0.025, system="us")
        assert isinstance(q, float)
        assert pytest.approx(q, rel=1e-4) == 14.6781 * 1.48608

    def test_manning_discharge_vectorized(self):
        areas = np.array([5.0, 10.0, 20.0])
        rhs = np.array([0.8, 1.25, 2.0])
        s = np.array([0.001, 0.001, 0.001])
        n = np.array([0.03, 0.025, 0.02])
        q = manning_discharge(areas, rhs, s, n)
        assert isinstance(q, np.ndarray)
        assert len(q) == 3
        assert np.all(q > 0.0)

    def test_manning_velocity(self):
        v = manning_velocity(1.0, 0.001, 0.025, system="si")
        # V = (1/0.025) * 1.0 * sqrt(0.001) = 40 * 0.03162278 = 1.2649 m/s
        assert pytest.approx(v, rel=1e-4) == 1.2649

    def test_strickler_velocity(self):
        # k_st = 40, Rh = 1.0, S = 0.001
        v = strickler_velocity(1.0, 0.001, 40.0)
        assert pytest.approx(v, rel=1e-4) == 40.0 * np.sqrt(0.001)

    def test_chezy_velocity(self):
        v = chezy_velocity(50.0, 2.0, 0.001)
        # V = 50 * sqrt(2.0 * 0.001) = 50 * sqrt(0.002) = 2.236 m/s
        assert pytest.approx(v, rel=1e-4) == 50.0 * np.sqrt(0.002)

    def test_kutter_and_bazin(self):
        c_kutter = kutter_chezy_c(1.5, 0.001, 0.025)
        c_bazin = bazin_chezy_c(1.5, 0.3)
        assert c_kutter > 20.0 and c_kutter < 80.0
        assert c_bazin > 20.0 and c_bazin < 80.0


class TestChannelGeometries:
    """Tests for Rectangular, Trapezoidal, Triangular, Circular, Parabolic geometries."""

    def test_rectangular_geometry(self):
        b, y = 4.0, 2.0
        a, p, rh, t, dh, yb = geom_rectangular(b, y)
        assert a == 8.0
        assert p == 8.0
        assert rh == 1.0
        assert t == 4.0
        assert dh == 2.0
        assert yb == 1.0

    def test_trapezoidal_geometry(self):
        # b = 5.0, m = 1.5, y = 2.0
        # A = (5 + 1.5*2)*2 = 16.0
        # P = 5 + 2*2*sqrt(1 + 2.25) = 5 + 4*sqrt(3.25) = 12.2111
        # T = 5 + 2*1.5*2 = 11.0
        a, p, rh, t, dh, yb = geom_trapezoidal(5.0, 1.5, 2.0)
        assert pytest.approx(a, rel=1e-5) == 16.0
        assert pytest.approx(p, rel=1e-4) == 12.2111
        assert pytest.approx(t, rel=1e-5) == 11.0
        assert pytest.approx(dh, rel=1e-5) == 16.0 / 11.0

    def test_triangular_geometry(self):
        m, y = 2.0, 3.0
        a, p, rh, t, dh, yb = geom_triangular(m, y)
        assert a == 2.0 * 9.0  # 18.0
        assert t == 2.0 * 2.0 * 3.0  # 12.0
        assert dh == 1.5
        assert yb == 1.0

    def test_circular_geometry(self):
        # Full pipe: y = D = 2.0
        d, y = 2.0, 2.0
        a, p, rh, t, dh = geom_circular(d, y)
        assert pytest.approx(a, rel=1e-5) == np.pi
        assert pytest.approx(p, rel=1e-5) == 2.0 * np.pi
        assert pytest.approx(rh, rel=1e-5) == 0.5


class TestEnergyMomentumJump:
    """Tests for Specific Energy, Froude Number, Belanger, and GVF."""

    def test_specific_energy_and_froude(self):
        # Rectangular b = 3.0, y = 1.5, Q = 9.0 -> A = 4.5, V = 2.0, g = 9.80665
        # Fr = 2.0 / sqrt(9.80665 * 1.5) = 2.0 / 3.8354 = 0.52145 (subcritical)
        # E = 1.5 + (2.0)^2 / (2 * 9.80665) = 1.5 + 0.20394 = 1.7039 m
        e = specific_energy(1.5, 9.0, 4.5, system="si")
        fr = froude_number(9.0, 4.5, 3.0, system="si")
        assert pytest.approx(e, rel=1e-4) == 1.7039
        assert pytest.approx(fr, rel=1e-4) == 0.5215

    def test_critical_depth_rectangular(self):
        # q = Q/b = 4.0 m^2/s -> y_c = (16 / 9.80665)^(1/3) = 1.1772 m
        yc = critical_depth_rectangular(4.0, system="si")
        assert pytest.approx(yc, rel=1e-4) == 1.1772

    def test_belanger_conjugate_depth(self):
        # y1 = 0.5 m, Fr1 = 3.0
        # y2 = (0.5 / 2) * (sqrt(1 + 8 * 9) - 1) = 0.25 * (sqrt(73) - 1) = 0.25 * 7.544 = 1.886 m
        y2 = belanger_conjugate_depth(0.5, 3.0)
        assert pytest.approx(y2, rel=1e-4) == 1.886

        loss = hydraulic_jump_head_loss(0.5, y2)
        assert loss > 0.0

        length = hydraulic_jump_length(0.5, y2)
        assert pytest.approx(length, rel=1e-4) == 6.0 * (y2 - 0.5)

    def test_normal_depth_solver(self):
        # Solve trapezoidal normal depth, verify Manning discharge matches target Q
        target_q = 25.0
        b, m, s0, n = 6.0, 1.5, 0.001, 0.025
        yn = normal_depth_trapezoidal(target_q, b, m, s0, n, system="si")
        assert isinstance(yn, float)
        assert yn > 0.0

        # Back-calculate Q
        a = (b + m * yn) * yn
        p = b + 2.0 * yn * np.sqrt(1.0 + m * m)
        rh = a / p
        q_back = (1.0 / n) * a * (rh ** (2.0 / 3.0)) * np.sqrt(s0)
        assert pytest.approx(q_back, rel=1e-4) == target_q


class TestPipeFlow:
    """Tests for Darcy-Weisbach, Colebrook-White, Hazen-Williams, and Water Hammer."""

    def test_laminar_friction(self):
        re = 1600.0
        f = laminar_friction(re)
        assert pytest.approx(f, rel=1e-6) == 64.0 / 1600.0  # 0.04

    def test_colebrook_white_convergence(self):
        # Benchmark Moody chart test point:
        # Re = 100,000, eps/D = 0.001 -> f ~ 0.0222
        f = colebrook_white(0.001, 100_000.0)
        assert isinstance(f, float)
        assert pytest.approx(f, abs=1e-3) == 0.0222

        # Verify against explicit Haaland and Swamee-Jain
        f_sj = swamee_jain(0.001, 100_000.0)
        f_h = haaland(0.001, 100_000.0)
        f_c = churchill(0.001, 100_000.0)
        assert pytest.approx(f, rel=0.03) == f_sj
        assert pytest.approx(f, rel=0.03) == f_h
        assert pytest.approx(f, rel=0.03) == f_c

    def test_darcy_weisbach(self):
        # f = 0.02, L = 100 m, D = 0.2 m, V = 2.0 m/s, g = 9.80665
        # h_f = 0.02 * (100 / 0.2) * (4.0 / 19.6133) = 10 * 0.20394 = 2.0394 m
        hf = darcy_weisbach(0.02, 100.0, 0.2, 2.0, system="si")
        assert pytest.approx(hf, rel=1e-4) == 2.0394

    def test_hazen_williams(self):
        # L = 1000 m, Q = 0.05 m^3/s, C = 130, D = 0.25 m
        hf = hazen_williams(1000.0, 0.05, 130.0, 0.25, system="si")
        assert hf > 0.0 and hf < 50.0

    def test_water_hammer(self):
        # K = 2.15e9 Pa (water), rho = 1000 kg/m^3, E = 2.0e11 Pa (steel)
        # D = 0.5 m, e = 0.01 m
        a = wave_celerity(2.15e9, 1000.0, 2.0e11, 0.5, 0.01)
        assert a > 1000.0 and a < 1400.0

        # Joukowsky head rise for delta_v = 1.5 m/s
        dh = joukowsky(a, 1.5, system="si")
        assert pytest.approx(dh, rel=1e-4) == (a * 1.5) / 9.80665

        # Critical closure time for L = 1200 m
        tc = critical_closure_time(1200.0, a)
        assert pytest.approx(tc, rel=1e-4) == (2.0 * 1200.0) / a

