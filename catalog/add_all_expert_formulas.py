"""
Adds 80+ essential water resources engineering formulas to hydrocivil.
Covers: Time of Concentration suite, empirical flood formulas, advanced infiltration models,
FAO-56 Penman-Monteith, Unit hydrographs, Lacey regime hydraulics, specialized weirs,
bridge pier scour, and coastal groundwater hydraulics.
"""

import os
import ast
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PY_DIR = os.path.join(BASE_DIR, "python", "hydrocivil")

# -----------------------------------------------------------------------------
# 1. HYDROLOGY EXTENSIONS CODE
# -----------------------------------------------------------------------------
HYDROLOGY_EXTENSIONS = '''

# =============================================================================
# TIME OF CONCENTRATION (Tc) COMPREHENSIVE SUITE
# =============================================================================

def faa_tc(
    length: FloatOrArray,
    slope: FloatOrArray,
    runoff_coeff: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes overland time of concentration Tc using the Federal Aviation Administration (FAA) equation.

    Formula:
        SI: T_c = (3.26 * (1.1 - C) * sqrt(L)) / (S^0.3333)  [L in m, S in %, Tc in min]
        US: T_c = (1.80 * (1.1 - C) * sqrt(L)) / (S^0.3333)  [L in ft, S in %, Tc in min]

    Parameters
    ----------
    length : FloatOrArray
        Overland flow path length L [m in SI, ft in US]. Bounds: > 0.
    slope : FloatOrArray
        Average basin surface slope S in percent (e.g., 1.5 for 1.5%). Bounds: > 0.
    runoff_coeff : FloatOrArray
        Rational runoff coefficient C (0.05 to 0.95).
    system : {'si', 'us'}, default='si'
        Unit system: 'si' uses k = 3.26; 'us' uses k = 1.80.

    Returns
    -------
    float | np.ndarray
        Time of concentration T_c in minutes.
    """
    (l, s, c), is_scalar = coerce_inputs(length, slope, runoff_coeff)
    k = 1.80 if system.lower() == "us" else 3.26
    with np.errstate(all='ignore'):
        tc = np.where((l <= 0) | (s <= 0) | (c < 0) | (c > 1.1), np.nan, (k * (1.1 - c) * np.sqrt(l)) / (s ** (1.0 / 3.0)))
    return format_output(tc, is_scalar)


def faa_l(
    tc: FloatOrArray,
    slope: FloatOrArray,
    runoff_coeff: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for flow length L from known FAA time of concentration."""
    (t, s, c), is_scalar = coerce_inputs(tc, slope, runoff_coeff)
    k = 1.80 if system.lower() == "us" else 3.26
    with np.errstate(all='ignore'):
        denom = k * (1.1 - c)
        l = np.where((t <= 0) | (s <= 0) | (denom <= 0), np.nan, ((t * (s ** (1.0 / 3.0))) / denom) ** 2)
    return format_output(l, is_scalar)


def faa_s(
    tc: FloatOrArray,
    length: FloatOrArray,
    runoff_coeff: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for slope S from known FAA time of concentration."""
    (t, l, c), is_scalar = coerce_inputs(tc, length, runoff_coeff)
    k = 1.80 if system.lower() == "us" else 3.26
    with np.errstate(all='ignore'):
        num = k * (1.1 - c) * np.sqrt(l)
        s = np.where((t <= 0) | (l <= 0) | (c < 0) | (c > 1.1), np.nan, (num / t) ** 3)
    return format_output(s, is_scalar)


def faa_c(
    tc: FloatOrArray,
    length: FloatOrArray,
    slope: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for runoff coefficient C from known FAA time of concentration."""
    (t, l, s), is_scalar = coerce_inputs(tc, length, slope)
    k = 1.80 if system.lower() == "us" else 3.26
    with np.errstate(all='ignore'):
        denom = k * np.sqrt(l)
        c = np.where((t <= 0) | (l <= 0) | (s <= 0), np.nan, 1.1 - (t * (s ** (1.0 / 3.0))) / denom)
    return format_output(c, is_scalar)


def kerby_tc(
    length: FloatOrArray,
    slope: FloatOrArray,
    roughness_n: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes overland sheet flow time of concentration Tc using the Kerby-Hathaway equation.

    Formula:
        SI: T_c = 1.439 * ((L * n) / sqrt(S))^0.467  [L in m, S in m/m, Tc in min]
        US: T_c = 0.828 * ((L * n) / sqrt(S))^0.467  [L in ft, S in ft/ft, Tc in min]

    Parameters
    ----------
    length : FloatOrArray
        Overland flow length L [m in SI, ft in US]. Bounds: > 0. Typically <= 100 m (300 ft).
    slope : FloatOrArray
        Surface slope S in m/m or ft/ft. Bounds: > 0.
    roughness_n : FloatOrArray
        Kerby retardance roughness coefficient (0.02 for smooth pavement to 0.80 for dense grass).
    system : {'si', 'us'}, default='si'
        Unit system: 'si' uses k = 1.439; 'us' uses k = 0.828.

    Returns
    -------
    float | np.ndarray
        Overland time of concentration T_c in minutes.
    """
    (l, s, n), is_scalar = coerce_inputs(length, slope, roughness_n)
    k = 0.828 if system.lower() == "us" else 1.439
    with np.errstate(all='ignore'):
        tc = np.where((l <= 0) | (s <= 0) | (n <= 0), np.nan, k * (((l * n) / np.sqrt(s)) ** 0.467))
    return format_output(tc, is_scalar)


def kerby_l(
    tc: FloatOrArray,
    slope: FloatOrArray,
    roughness_n: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for length L from known Kerby time of concentration."""
    (t, s, n), is_scalar = coerce_inputs(tc, slope, roughness_n)
    k = 0.828 if system.lower() == "us" else 1.439
    with np.errstate(all='ignore'):
        l = np.where((t <= 0) | (s <= 0) | (n <= 0), np.nan, (np.sqrt(s) / n) * ((t / k) ** (1.0 / 0.467)))
    return format_output(l, is_scalar)


def kerby_s(
    tc: FloatOrArray,
    length: FloatOrArray,
    roughness_n: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for slope S from known Kerby time of concentration."""
    (t, l, n), is_scalar = coerce_inputs(tc, length, roughness_n)
    k = 0.828 if system.lower() == "us" else 1.439
    with np.errstate(all='ignore'):
        s = np.where((t <= 0) | (l <= 0) | (n <= 0), np.nan, ((l * n) / ((t / k) ** (1.0 / 0.467))) ** 2)
    return format_output(s, is_scalar)


def kerby_n(
    tc: FloatOrArray,
    length: FloatOrArray,
    slope: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for Kerby retardance roughness n from known time of concentration."""
    (t, l, s), is_scalar = coerce_inputs(tc, length, slope)
    k = 0.828 if system.lower() == "us" else 1.439
    with np.errstate(all='ignore'):
        n = np.where((t <= 0) | (l <= 0) | (s <= 0), np.nan, (np.sqrt(s) / l) * ((t / k) ** (1.0 / 0.467)))
    return format_output(n, is_scalar)


def bransby_williams_tc(
    length_km: FloatOrArray,
    area_km2: FloatOrArray,
    slope_m_per_km: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes time of concentration Tc using the Bransby-Williams equation (Australian / Commonwealth standard).

    Formula:
        T_c = (58.5 * L) / (A^0.1 * S^0.2)  [L in km, A in km^2, S in m/km, Tc in min]

    Parameters
    ----------
    length_km : FloatOrArray
        Main channel flow path length L in km. Must be > 0.
    area_km2 : FloatOrArray
        Contributing catchment drainage area A in km^2. Must be > 0.
    slope_m_per_km : FloatOrArray
        Average mainstream slope S in m/km (or m per 1000 m). Must be > 0.

    Returns
    -------
    float | np.ndarray
        Time of concentration T_c in minutes.
    """
    (l, a, s), is_scalar = coerce_inputs(length_km, area_km2, slope_m_per_km)
    with np.errstate(all='ignore'):
        tc = np.where((l <= 0) | (a <= 0) | (s <= 0), np.nan, (58.5 * l) / ((a ** 0.1) * (s ** 0.2)))
    return format_output(tc, is_scalar)


def bransby_williams_l(
    tc: FloatOrArray,
    area_km2: FloatOrArray,
    slope_m_per_km: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for channel length L from known Bransby-Williams time of concentration."""
    (t, a, s), is_scalar = coerce_inputs(tc, area_km2, slope_m_per_km)
    with np.errstate(all='ignore'):
        l = np.where((t <= 0) | (a <= 0) | (s <= 0), np.nan, (t * (a ** 0.1) * (s ** 0.2)) / 58.5)
    return format_output(l, is_scalar)


def bransby_williams_a(
    tc: FloatOrArray,
    length_km: FloatOrArray,
    slope_m_per_km: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for catchment area A from known Bransby-Williams time of concentration."""
    (t, l, s), is_scalar = coerce_inputs(tc, length_km, slope_m_per_km)
    with np.errstate(all='ignore'):
        a = np.where((t <= 0) | (l <= 0) | (s <= 0), np.nan, ((58.5 * l) / (t * (s ** 0.2))) ** 10.0)
    return format_output(a, is_scalar)


def bransby_williams_s(
    tc: FloatOrArray,
    length_km: FloatOrArray,
    area_km2: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for slope S from known Bransby-Williams time of concentration."""
    (t, l, a), is_scalar = coerce_inputs(tc, length_km, area_km2)
    with np.errstate(all='ignore'):
        s = np.where((t <= 0) | (l <= 0) | (a <= 0), np.nan, ((58.5 * l) / (t * (a ** 0.1))) ** 5.0)
    return format_output(s, is_scalar)


def tr55_channel_tc(
    length: FloatOrArray,
    velocity: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes channel flow travel time Tt = L / (60 * V) [Tt in min].
    """
    (l, v), is_scalar = coerce_inputs(length, velocity)
    with np.errstate(all='ignore'):
        tt = np.where((l <= 0) | (v <= 0), np.nan, l / (60.0 * v))
    return format_output(tt, is_scalar)


def tr55_composite_tc(
    t_sheet: FloatOrArray,
    t_shallow: FloatOrArray,
    t_channel: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes total catchment time of concentration Tc = T_sheet + T_shallow + T_channel [min].
    """
    (t1, t2, t3), is_scalar = coerce_inputs(t_sheet, t_shallow, t_channel)
    out = t1 + t2 + t3
    return format_output(out, is_scalar)


# =============================================================================
# REGIONAL EMPIRICAL PEAK FLOOD RUNOFF FORMULAS
# =============================================================================

def dickens_q(
    area_km2: FloatOrArray,
    c_d: FloatOrArray = 14.0,
) -> Union[float, np.ndarray]:
    """
    Computes maximum flood peak discharge Q using Dicken's formula.

    Formula:
        Q = C_D * A^(3/4)  [A in km^2, Q in m^3/s]

    Parameters
    ----------
    area_km2 : FloatOrArray
        Catchment drainage area A in km^2. Bounds: > 0.
    c_d : FloatOrArray, default=14.0
        Dicken's runoff coefficient (typically 11.4 to 19.0 for North India / plains, up to 28.0 for hills).

    Returns
    -------
    float | np.ndarray
        Peak discharge Q in m^3/s.
    """
    (a, cd), is_scalar = coerce_inputs(area_km2, c_d)
    with np.errstate(all='ignore'):
        q = np.where((a <= 0) | (cd <= 0), np.nan, cd * (a ** 0.75))
    return format_output(q, is_scalar)


def dickens_cd(
    discharge: FloatOrArray,
    area_km2: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for Dicken's coefficient C_D = Q / A^(3/4)."""
    (q, a), is_scalar = coerce_inputs(discharge, area_km2)
    with np.errstate(all='ignore'):
        cd = np.where((q <= 0) | (a <= 0), np.nan, q / (a ** 0.75))
    return format_output(cd, is_scalar)


def dickens_area(
    discharge: FloatOrArray,
    c_d: FloatOrArray = 14.0,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for drainage area A = (Q / C_D)^(4/3)."""
    (q, cd), is_scalar = coerce_inputs(discharge, c_d)
    with np.errstate(all='ignore'):
        a = np.where((q <= 0) | (cd <= 0), np.nan, (q / cd) ** (4.0 / 3.0))
    return format_output(a, is_scalar)


def ryves_q(
    area_km2: FloatOrArray,
    c_r: FloatOrArray = 8.5,
) -> Union[float, np.ndarray]:
    """
    Computes maximum flood peak discharge Q using Ryves' formula (South India / flat plateau standard).

    Formula:
        Q = C_R * A^(2/3)  [A in km^2, Q in m^3/s]

    Parameters
    ----------
    area_km2 : FloatOrArray
        Catchment drainage area A in km^2. Bounds: > 0.
    c_r : FloatOrArray, default=8.5
        Ryves' runoff coefficient (typically 6.8 for flat terrain, 8.5 for undulating, up to 10.2 for hills).

    Returns
    -------
    float | np.ndarray
        Peak discharge Q in m^3/s.
    """
    (a, cr), is_scalar = coerce_inputs(area_km2, c_r)
    with np.errstate(all='ignore'):
        q = np.where((a <= 0) | (cr <= 0), np.nan, cr * (a ** (2.0 / 3.0)))
    return format_output(q, is_scalar)


def ryves_cr(
    discharge: FloatOrArray,
    area_km2: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for Ryves' coefficient C_R = Q / A^(2/3)."""
    (q, a), is_scalar = coerce_inputs(discharge, area_km2)
    with np.errstate(all='ignore'):
        cr = np.where((q <= 0) | (a <= 0), np.nan, q / (a ** (2.0 / 3.0)))
    return format_output(cr, is_scalar)


def ryves_area(
    discharge: FloatOrArray,
    c_r: FloatOrArray = 8.5,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for drainage area A = (Q / C_R)^(3/2)."""
    (q, cr), is_scalar = coerce_inputs(discharge, c_r)
    with np.errstate(all='ignore'):
        a = np.where((q <= 0) | (cr <= 0), np.nan, (q / cr) ** 1.5)
    return format_output(a, is_scalar)


def inglis_q(
    area_km2: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes maximum flood discharge Q using Inglis' formula for fan-shaped catchments.

    Formula:
        Q = (124 * A) / sqrt(A + 10.4)  [A in km^2, Q in m^3/s]
    """
    (a,), is_scalar = coerce_inputs(area_km2)
    with np.errstate(all='ignore'):
        q = np.where(a <= 0, np.nan, (124.0 * a) / np.sqrt(a + 10.4))
    return format_output(q, is_scalar)


def inglis_area(
    discharge: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for catchment area A algebraically from known Inglis discharge."""
    (q,), is_scalar = coerce_inputs(discharge)
    with np.errstate(all='ignore'):
        # 15376 A^2 - Q^2 A - 10.4 Q^2 = 0
        disc = (q ** 4) + (4.0 * 15376.0 * 10.4 * (q ** 2))
        a = np.where(q <= 0, np.nan, ((q ** 2) + np.sqrt(disc)) / (2.0 * 15376.0))
    return format_output(a, is_scalar)


def nawab_jung_q(
    area_km2: FloatOrArray,
    c_n: FloatOrArray = 48.0,
) -> Union[float, np.ndarray]:
    """
    Computes maximum flood discharge Q using Nawab Jung Bahadur formula (Deccan plateau).

    Formula:
        Q = C_N * A^(5/6)  [A in km^2, Q in m^3/s]
    """
    (a, cn), is_scalar = coerce_inputs(area_km2, c_n)
    with np.errstate(all='ignore'):
        q = np.where((a <= 0) | (cn <= 0), np.nan, cn * (a ** (5.0 / 6.0)))
    return format_output(q, is_scalar)


def nawab_jung_cn(
    discharge: FloatOrArray,
    area_km2: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for Nawab Jung coefficient C_N = Q / A^(5/6)."""
    (q, a), is_scalar = coerce_inputs(discharge, area_km2)
    with np.errstate(all='ignore'):
        cn = np.where((q <= 0) | (a <= 0), np.nan, q / (a ** (5.0 / 6.0)))
    return format_output(cn, is_scalar)


def nawab_jung_area(
    discharge: FloatOrArray,
    c_n: FloatOrArray = 48.0,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for drainage area A = (Q / C_N)^(6/5)."""
    (q, cn), is_scalar = coerce_inputs(discharge, c_n)
    with np.errstate(all='ignore'):
        a = np.where((q <= 0) | (cn <= 0), np.nan, (q / cn) ** 1.2)
    return format_output(a, is_scalar)


def fuller_flood_q(
    area_sq_mi: FloatOrArray,
    return_period: FloatOrArray,
    c_f: FloatOrArray = 1.5,
) -> Union[float, np.ndarray]:
    """
    Computes design flood peak discharge using Fuller's empirical frequency relationship.

    Formula:
        Q_T = C_F * A^0.8 * (1 + 0.8 * log10(T))  [A in sq. mi, T in years, Q in cfs]
    """
    (a, t, cf), is_scalar = coerce_inputs(area_sq_mi, return_period, c_f)
    with np.errstate(all='ignore'):
        q = np.where((a <= 0) | (t < 1.0) | (cf <= 0), np.nan, cf * (a ** 0.8) * (1.0 + 0.8 * np.log10(t)))
    return format_output(q, is_scalar)


def fuller_return_period(
    discharge: FloatOrArray,
    area_sq_mi: FloatOrArray,
    c_f: FloatOrArray = 1.5,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for return period T from known Fuller flood discharge."""
    (q, a, cf), is_scalar = coerce_inputs(discharge, area_sq_mi, c_f)
    with np.errstate(all='ignore'):
        term = ((q / (cf * (a ** 0.8))) - 1.0) / 0.8
        t = np.where((q <= 0) | (a <= 0) | (cf <= 0), np.nan, 10.0 ** term)
    return format_output(t, is_scalar)


# =============================================================================
# INFILTRATION ADVANCED MODELS (PHILIP & KOSTIAKOV)
# =============================================================================

def philip_rate(
    time: FloatOrArray,
    sorptivity: FloatOrArray,
    transmissivity_a: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes infiltration capacity fp(t) using Philip's Two-Term infiltration model (Philip, 1957).

    Formula:
        f_p(t) = 0.5 * S * t^(-1/2) + A  [S in mm/hr^0.5, A in mm/hr, t in hr]
    """
    (t, s, a), is_scalar = coerce_inputs(time, sorptivity, transmissivity_a)
    with np.errstate(all='ignore'):
        fp = np.where((t <= 0) | (s < 0) | (a < 0), np.nan, (0.5 * s) / np.sqrt(t) + a)
    return format_output(fp, is_scalar)


def philip_cumulative(
    time: FloatOrArray,
    sorptivity: FloatOrArray,
    transmissivity_a: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes cumulative infiltration depth F(t) using Philip's Two-Term equation.

    Formula:
        F(t) = S * t^(1/2) + A * t  [F in mm, t in hr]
    """
    (t, s, a), is_scalar = coerce_inputs(time, sorptivity, transmissivity_a)
    with np.errstate(all='ignore'):
        f = np.where((t < 0) | (s < 0) | (a < 0), np.nan, (s * np.sqrt(t)) + (a * t))
    return format_output(f, is_scalar)


def philip_sorptivity(
    cumulative_f: FloatOrArray,
    time: FloatOrArray,
    transmissivity_a: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for soil sorptivity S = (F - A * t) / sqrt(t)."""
    (f, t, a), is_scalar = coerce_inputs(cumulative_f, time, transmissivity_a)
    with np.errstate(all='ignore'):
        s = np.where((t <= 0) | (f < 0), np.nan, (f - (a * t)) / np.sqrt(t))
    return format_output(s, is_scalar)


def kostiakov_rate(
    time: FloatOrArray,
    a_coeff: FloatOrArray,
    b_exponent: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes infiltration capacity rate using Kostiakov's empirical equation (Kostiakov, 1932).

    Formula:
        f_p(t) = a * b * t^(b - 1)  [0 < b < 1, t in hr]
    """
    (t, a, b), is_scalar = coerce_inputs(time, a_coeff, b_exponent)
    with np.errstate(all='ignore'):
        fp = np.where((t <= 0) | (a <= 0) | (b <= 0) | (b >= 1.0), np.nan, a * b * (t ** (b - 1.0)))
    return format_output(fp, is_scalar)


def kostiakov_cumulative(
    time: FloatOrArray,
    a_coeff: FloatOrArray,
    b_exponent: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes cumulative infiltration depth using Kostiakov's power equation.

    Formula:
        F(t) = a * t^b  [F in mm or cm, t in hr]
    """
    (t, a, b), is_scalar = coerce_inputs(time, a_coeff, b_exponent)
    with np.errstate(all='ignore'):
        f = np.where((t < 0) | (a <= 0) | (b <= 0) | (b >= 1.0), np.nan, a * (t ** b))
    return format_output(f, is_scalar)


def kostiakov_time(
    cumulative_f: FloatOrArray,
    a_coeff: FloatOrArray,
    b_exponent: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for elapsed time t = (F / a)^(1 / b)."""
    (f, a, b), is_scalar = coerce_inputs(cumulative_f, a_coeff, b_exponent)
    with np.errstate(all='ignore'):
        t = np.where((f <= 0) | (a <= 0) | (b <= 0), np.nan, (f / a) ** (1.0 / b))
    return format_output(t, is_scalar)


def green_ampt_ponding_time(
    intensity: FloatOrArray,
    conductivity_k: FloatOrArray,
    suction_psi: FloatOrArray,
    moisture_deficit: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes time to surface ponding tp under constant rainfall intensity using Green-Ampt theory.

    Formula:
        t_p = (K * psi * Delta_theta) / (i * (i - K))  [Valid for i > K]
    """
    (i, k, psi, dtheta), is_scalar = coerce_inputs(intensity, conductivity_k, suction_psi, moisture_deficit)
    with np.errstate(all='ignore'):
        tp = np.where((i <= k) | (k <= 0) | (psi <= 0) | (dtheta <= 0), np.nan, (k * psi * dtheta) / (i * (i - k)))
    return format_output(tp, is_scalar)


# =============================================================================
# EVAPOTRANSPIRATION BENCHMARKS (FAO-56 PENMAN-MONTEITH, PRIESTLEY-TAYLOR)
# =============================================================================

def saturation_vapor_pressure(
    temp_c: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes saturation vapor pressure e_s(T) using the standard FAO-56 Tetens equation.

    Formula:
        e_s = 0.6108 * exp((17.27 * T) / (T + 237.3))  [e_s in kPa, T in deg C]
    """
    (t,), is_scalar = coerce_inputs(temp_c)
    with np.errstate(all='ignore'):
        es = 0.6108 * np.exp((17.27 * t) / (t + 237.3))
    return format_output(es, is_scalar)


def vapor_pressure_slope(
    temp_c: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes the slope of the saturation vapor pressure curve Delta = d(e_s)/dT [kPa / deg C].

    Formula:
        Delta = (4098 * e_s) / (T + 237.3)^2
    """
    (t,), is_scalar = coerce_inputs(temp_c)
    es = 0.6108 * np.exp((17.27 * t) / (t + 237.3))
    with np.errstate(all='ignore'):
        delta = (4098.0 * es) / ((t + 237.3) ** 2)
    return format_output(delta, is_scalar)


def fao56_penman_monteith(
    net_radiation: FloatOrArray,
    temp_c: FloatOrArray,
    wind_speed_2m: FloatOrArray,
    es: FloatOrArray,
    ea: FloatOrArray,
    delta_slope: FloatOrArray,
    psychrometric_gamma: FloatOrArray,
    soil_heat_flux: FloatOrArray = 0.0,
) -> Union[float, np.ndarray]:
    """
    Computes daily reference evapotranspiration ET_0 using the international FAO-56 Penman-Monteith equation.

    Formula:
        ET_0 = [0.408 * Delta * (R_n - G) + gamma * (900 / (T + 273)) * u_2 * (e_s - e_a)] / [Delta + gamma * (1 + 0.34 * u_2)]

    Parameters
    ----------
    net_radiation : FloatOrArray
        Net radiation at crop surface R_n [MJ / m^2 / day].
    temp_c : FloatOrArray
        Mean daily air temperature at 2 m height T [deg C].
    wind_speed_2m : FloatOrArray
        Wind speed at 2 m height u_2 [m/s]. Bounds: >= 0.
    es : FloatOrArray
        Saturation vapor pressure e_s [kPa].
    ea : FloatOrArray
        Actual vapor pressure e_a [kPa].
    delta_slope : FloatOrArray
        Slope of vapor pressure curve Delta [kPa / deg C].
    psychrometric_gamma : FloatOrArray
        Psychrometric constant gamma [kPa / deg C] (~0.067 at sea level).
    soil_heat_flux : FloatOrArray, default=0.0
        Soil heat flux density G [MJ / m^2 / day] (often ~0 for daily calculations).

    Returns
    -------
    float | np.ndarray
        Reference evapotranspiration ET_0 in mm/day.
    """
    (rn, t, u2, es_v, ea_v, delta, gamma, g), is_scalar = coerce_inputs(
        net_radiation, temp_c, wind_speed_2m, es, ea, delta_slope, psychrometric_gamma, soil_heat_flux
    )
    with np.errstate(all='ignore'):
        num = 0.408 * delta * (rn - g) + gamma * (900.0 / (t + 273.0)) * u2 * (es_v - ea_v)
        denom = delta + gamma * (1.0 + 0.34 * u2)
        et0 = np.where(denom <= 0, np.nan, num / denom)
    return format_output(et0, is_scalar)


def fao56_net_radiation(
    et0: FloatOrArray,
    temp_c: FloatOrArray,
    wind_speed_2m: FloatOrArray,
    es: FloatOrArray,
    ea: FloatOrArray,
    delta_slope: FloatOrArray,
    psychrometric_gamma: FloatOrArray,
    soil_heat_flux: FloatOrArray = 0.0,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for required net radiation R_n from known FAO-56 ET_0."""
    (et, t, u2, es_v, ea_v, delta, gamma, g), is_scalar = coerce_inputs(
        et0, temp_c, wind_speed_2m, es, ea, delta_slope, psychrometric_gamma, soil_heat_flux
    )
    with np.errstate(all='ignore'):
        denom_et = delta + gamma * (1.0 + 0.34 * u2)
        aero_term = gamma * (900.0 / (t + 273.0)) * u2 * (es_v - ea_v)
        rn = g + ((et * denom_et) - aero_term) / (0.408 * delta)
    return format_output(rn, is_scalar)


def priestley_taylor_et(
    net_radiation: FloatOrArray,
    temp_c: FloatOrArray,
    delta_slope: FloatOrArray,
    psychrometric_gamma: FloatOrArray,
    alpha: FloatOrArray = 1.26,
    soil_heat_flux: FloatOrArray = 0.0,
) -> Union[float, np.ndarray]:
    """
    Computes radiation-driven potential evapotranspiration using the Priestley-Taylor equation (1972).

    Formula:
        ET = alpha * [Delta / (Delta + gamma)] * [(R_n - G) / lambda]  [lambda = 2.45 MJ/kg]
    """
    (rn, t, delta, gamma, alf, g), is_scalar = coerce_inputs(
        net_radiation, temp_c, delta_slope, psychrometric_gamma, alpha, soil_heat_flux
    )
    with np.errstate(all='ignore'):
        et = alf * (delta / (delta + gamma)) * ((rn - g) / 2.45)
    return format_output(et, is_scalar)


def blaney_criddle_et(
    temp_c: FloatOrArray,
    sunshine_p_percent: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes monthly reference evapotranspiration ET_0 using the FAO Blaney-Criddle formula.

    Formula:
        ET_0 = p * (0.46 * T_mean + 8.13)  [ET_0 in mm/day, p is % of annual daytime hours]
    """
    (t, p), is_scalar = coerce_inputs(temp_c, sunshine_p_percent)
    with np.errstate(all='ignore'):
        et = p * (0.46 * t + 8.13)
    return format_output(et, is_scalar)


def blaney_criddle_temp(
    et0: FloatOrArray,
    sunshine_p_percent: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for mean temperature T = (ET_0 / p - 8.13) / 0.46."""
    (et, p), is_scalar = coerce_inputs(et0, sunshine_p_percent)
    with np.errstate(all='ignore'):
        t = np.where(p <= 0, np.nan, ((et / p) - 8.13) / 0.46)
    return format_output(t, is_scalar)


# =============================================================================
# SYNTHETIC UNIT HYDROGRAPHS & ROUTING
# =============================================================================

def scs_unit_hydrograph_peak(
    drainage_area: FloatOrArray,
    time_to_peak: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes peak discharge qp of the SCS / NRCS Dimensionless Unit Hydrograph.

    Formula:
        SI: q_p = (0.208 * A) / T_p  [A in km^2, T_p in hr, q_p in m^3/s]
        US: q_p = (484.0 * A) / T_p  [A in sq. mi, T_p in hr, q_p in cfs]
    """
    (a, tp), is_scalar = coerce_inputs(drainage_area, time_to_peak)
    k = 484.0 if system.lower() == "us" else 0.208
    with np.errstate(all='ignore'):
        qp = np.where((a <= 0) | (tp <= 0), np.nan, (k * a) / tp)
    return format_output(qp, is_scalar)


def scs_uh_tp(
    discharge_peak: FloatOrArray,
    drainage_area: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for time to peak T_p = (k * A) / q_p."""
    (qp, a), is_scalar = coerce_inputs(discharge_peak, drainage_area)
    k = 484.0 if system.lower() == "us" else 0.208
    with np.errstate(all='ignore'):
        tp = np.where((qp <= 0) | (a <= 0), np.nan, (k * a) / qp)
    return format_output(tp, is_scalar)


def scs_uh_area(
    discharge_peak: FloatOrArray,
    time_to_peak: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for drainage area A = (q_p * T_p) / k."""
    (qp, tp), is_scalar = coerce_inputs(discharge_peak, time_to_peak)
    k = 484.0 if system.lower() == "us" else 0.208
    with np.errstate(all='ignore'):
        a = np.where((qp <= 0) | (tp <= 0), np.nan, (qp * tp) / k)
    return format_output(a, is_scalar)


def scs_lag_time(
    tc: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Computes SCS basin lag time t_L = 0.6 * T_c."""
    (t,), is_scalar = coerce_inputs(tc)
    out = 0.6 * t
    return format_output(out, is_scalar)


def scs_time_to_peak(
    rainfall_duration: FloatOrArray,
    lag_time: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Computes time to peak T_p = 0.5 * D + t_L."""
    (d, tl), is_scalar = coerce_inputs(rainfall_duration, lag_time)
    out = (0.5 * d) + tl
    return format_output(out, is_scalar)


def snyder_lag_time(
    length: FloatOrArray,
    length_to_centroid: FloatOrArray,
    c_t: FloatOrArray = 1.5,
) -> Union[float, np.ndarray]:
    """
    Computes Snyder's unit hydrograph basin lag time tp.

    Formula:
        t_p = C_t * (L * L_c)^0.3  [t_p in hours]
    """
    (l, lc, ct), is_scalar = coerce_inputs(length, length_to_centroid, c_t)
    with np.errstate(all='ignore'):
        tp = np.where((l <= 0) | (lc <= 0) | (ct <= 0), np.nan, ct * ((l * lc) ** 0.3))
    return format_output(tp, is_scalar)


def snyder_peak_discharge(
    drainage_area: FloatOrArray,
    lag_time: FloatOrArray,
    c_p: FloatOrArray = 0.6,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes Snyder's unit hydrograph peak discharge Qp.

    Formula:
        SI: Q_p = (2.78 * C_p * A) / t_p  [A in km^2, t_p in hr, Q_p in m^3/s]
        US: Q_p = (640.0 * C_p * A) / t_p  [A in sq. mi, t_p in hr, Q_p in cfs]
    """
    (a, tp, cp), is_scalar = coerce_inputs(drainage_area, lag_time, c_p)
    k = 640.0 if system.lower() == "us" else 2.78
    with np.errstate(all='ignore'):
        qp = np.where((a <= 0) | (tp <= 0) | (cp <= 0), np.nan, (k * cp * a) / tp)
    return format_output(qp, is_scalar)


def snyder_hydrograph_widths(
    unit_peak_q: FloatOrArray,
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Computes USACE Snyder unit hydrograph widths at 50% and 75% of peak discharge.

    Formula:
        W_50 = 5.87 / (q_p)^1.08  [hr]
        W_75 = 3.35 / (q_p)^1.08  [hr]
    """
    (qp,), is_scalar = coerce_inputs(unit_peak_q)
    with np.errstate(all='ignore'):
        w50 = np.where(qp <= 0, np.nan, 5.87 / (qp ** 1.08))
        w75 = np.where(qp <= 0, np.nan, 3.35 / (qp ** 1.08))
    return format_outputs((w50, w75), is_scalar)


def muskingum_cunge_parameters(
    length: FloatOrArray,
    slope: FloatOrArray,
    bottom_width: FloatOrArray,
    discharge: FloatOrArray,
    roughness_n: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Tuple[Union[float, np.ndarray], ...]:
    """
    Computes physically-based Muskingum-Cunge routing parameters: wave celerity c, travel time K, and weighting factor X.
    Returns (celerity, K, X).
    """
    (l, s, b, q, n), is_scalar = coerce_inputs(length, slope, bottom_width, discharge, roughness_n)
    k_manning = 1.486 if system.lower() == "us" else 1.0
    with np.errstate(all='ignore'):
        # Normal depth approx for wide channel: y = ((q * n) / (k * b * sqrt(s)))^(3/5)
        y = ((q * n) / (k_manning * b * np.sqrt(s))) ** 0.6
        v = q / (b * y)
        c = (5.0 / 3.0) * v
        k = l / c
        x = 0.5 * (1.0 - (q / (b * s * c * l)))
        x = np.clip(x, 0.0, 0.5)
    return format_outputs((c, k, x), is_scalar)


def baseflow_lyne_hollick(
    streamflow: Sequence[float],
    alpha: float = 0.925,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Separates total streamflow into quickflow (direct runoff) and baseflow using the Lyne-Hollick digital filter.
    Returns (quickflow, baseflow).
    """
    y = np.asarray(streamflow, dtype=np.float64)
    n = len(y)
    q = np.zeros(n, dtype=np.float64)
    b = np.zeros(n, dtype=np.float64)
    
    for i in range(1, n):
        term = y[i] - y[i-1]
        q_val = alpha * q[i-1] + ((1.0 + alpha) / 2.0) * term
        q[i] = max(0.0, min(y[i], q_val))
        b[i] = y[i] - q[i]
        
    b[0] = y[0]
    return q, b


# =============================================================================
# EXTREME VALUE & STATISTICAL HYDROLOGY
# =============================================================================

def gumbel_reduced_variate(
    return_period: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Computes Gumbel EV1 reduced variate y_T = -ln(-ln(1 - 1/T))."""
    (t,), is_scalar = coerce_inputs(return_period)
    with np.errstate(all='ignore'):
        yt = np.where(t <= 1.0, np.nan, -np.log(-np.log(1.0 - (1.0 / t))))
    return format_output(yt, is_scalar)


def gumbel_return_period(
    reduced_variate: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for return period T = 1 / (1 - exp(-exp(-y_T)))."""
    (yt,), is_scalar = coerce_inputs(reduced_variate)
    with np.errstate(all='ignore'):
        t = 1.0 / (1.0 - np.exp(-np.exp(-yt)))
    return format_output(t, is_scalar)


def gumbel_frequency_factor(
    return_period: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Computes Chow frequency factor K_T for Gumbel distribution."""
    (t,), is_scalar = coerce_inputs(return_period)
    with np.errstate(all='ignore'):
        yt = np.where(t <= 1.0, np.nan, -np.log(-np.log(1.0 - (1.0 / t))))
        kt = (yt - 0.5772156649) / (np.pi / np.sqrt(6.0))
    return format_output(kt, is_scalar)


def gumbel_design_flood(
    mean: FloatOrArray,
    std_dev: FloatOrArray,
    return_period: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Computes design flood peak magnitude x_T = mean + K_T * std_dev."""
    (x_bar, sx, t), is_scalar = coerce_inputs(mean, std_dev, return_period)
    with np.errstate(all='ignore'):
        yt = -np.log(-np.log(1.0 - (1.0 / t)))
        kt = (yt - 0.5772156649) / (np.pi / np.sqrt(6.0))
        xt = x_bar + (kt * sx)
    return format_output(xt, is_scalar)


def gumbel_return_period_from_flood(
    observed_flood: FloatOrArray,
    mean: FloatOrArray,
    std_dev: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Back-calculates return period T from observed flood discharge magnitude."""
    (xt, x_bar, sx), is_scalar = coerce_inputs(observed_flood, mean, std_dev)
    with np.errstate(all='ignore'):
        kt = (xt - x_bar) / sx
        yt = 0.5772156649 + (kt * (np.pi / np.sqrt(6.0)))
        t = 1.0 / (1.0 - np.exp(-np.exp(-yt)))
    return format_output(t, is_scalar)


def log_pearson_3_flood(
    log_mean: FloatOrArray,
    log_std_dev: FloatOrArray,
    skewness: FloatOrArray,
    return_period: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes design flood using Log-Pearson Type III distribution (USGS Bulletin 17C standard).
    Uses Wilson-Hilferty transformation for frequency factor K_T.
    """
    (y_bar, sy, g, t), is_scalar = coerce_inputs(log_mean, log_std_dev, skewness, return_period)
    with np.errstate(all='ignore'):
        # Normal standard deviate z approximation from return period
        p = 1.0 / t
        # Hastings rational approx for z
        w = np.sqrt(-2.0 * np.log(p))
        z = w - ((2.515517 + 0.802853 * w + 0.010328 * (w ** 2)) / (1.0 + 1.432788 * w + 0.189269 * (w ** 2) + 0.001308 * (w ** 3)))
        
        # Wilson-Hilferty transformation
        kt = np.where(
            np.abs(g) < 1e-4,
            z,
            (2.0 / g) * ((((1.0 + ((g * z) / 6.0) - ((g ** 2) / 36.0))) ** 3) - 1.0)
        )
        log_xt = y_bar + (kt * sy)
        xt = 10.0 ** log_xt
    return format_output(xt, is_scalar)


def weibull_plotting_position(
    rank: FloatOrArray,
    total_samples: FloatOrArray,
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Computes empirical exceedance probability P and return period T using Weibull plotting position: P = m / (N + 1).
    Returns (probability, return_period).
    """
    (m, n), is_scalar = coerce_inputs(rank, total_samples)
    with np.errstate(all='ignore'):
        p = m / (n + 1.0)
        t = (n + 1.0) / m
    return format_outputs((p, t), is_scalar)


def gringorten_plotting_position(
    rank: FloatOrArray,
    total_samples: FloatOrArray,
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Computes empirical plotting position using Gringorten formula: P = (m - 0.44) / (N + 0.12).
    Returns (probability, return_period).
    """
    (m, n), is_scalar = coerce_inputs(rank, total_samples)
    with np.errstate(all='ignore'):
        p = (m - 0.44) / (n + 0.12)
        t = (n + 0.12) / (m - 0.44)
    return format_outputs((p, t), is_scalar)


def cunnane_plotting_position(
    rank: FloatOrArray,
    total_samples: FloatOrArray,
) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray]]:
    """
    Computes empirical plotting position using Cunnane formula: P = (m - 0.4) / (N + 0.2).
    Returns (probability, return_period).
    """
    (m, n), is_scalar = coerce_inputs(rank, total_samples)
    with np.errstate(all='ignore'):
        p = (m - 0.4) / (n + 0.2)
        t = (n + 0.2) / (m - 0.4)
    return format_outputs((p, t), is_scalar)
'''


# -----------------------------------------------------------------------------
# 2. HYDRAULICS EXTENSIONS CODE
# -----------------------------------------------------------------------------
HYDRAULICS_EXTENSIONS = '''

# =============================================================================
# ALLUVIAL CANAL REGIME HYDRAULICS (LACEY & KENNEDY)
# =============================================================================

def lacey_silt_factor(
    d50_mm: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes Lacey's silt factor f from median alluvial sediment grain size.

    Formula:
        f = 1.76 * sqrt(d_50)  [d_50 in mm]
    """
    (d,), is_scalar = coerce_inputs(d50_mm)
    with np.errstate(all='ignore'):
        f = np.where(d <= 0, np.nan, 1.76 * np.sqrt(d))
    return format_output(f, is_scalar)


def lacey_d50(
    silt_factor: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for sediment grain size d_50 = (f / 1.76)^2 [mm]."""
    (f,), is_scalar = coerce_inputs(silt_factor)
    with np.errstate(all='ignore'):
        d = np.where(f <= 0, np.nan, (f / 1.76) ** 2)
    return format_output(d, is_scalar)


def lacey_regime_velocity(
    discharge: FloatOrArray,
    silt_factor: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes Lacey's regime non-silting, non-scouring velocity V.

    Formula:
        V = ((Q * f^2) / 140)^(1/6)  [Q in m^3/s, V in m/s]
    """
    (q, f), is_scalar = coerce_inputs(discharge, silt_factor)
    with np.errstate(all='ignore'):
        v = np.where((q <= 0) | (f <= 0), np.nan, ((q * (f ** 2)) / 140.0) ** (1.0 / 6.0))
    return format_output(v, is_scalar)


def lacey_velocity_discharge(
    velocity: FloatOrArray,
    silt_factor: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for regime discharge Q = (140 * V^6) / f^2."""
    (v, f), is_scalar = coerce_inputs(velocity, silt_factor)
    with np.errstate(all='ignore'):
        q = np.where((v <= 0) | (f <= 0), np.nan, (140.0 * (v ** 6)) / (f ** 2))
    return format_output(q, is_scalar)


def lacey_wetted_perimeter(
    discharge: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes Lacey's regime wetted perimeter P = 4.75 * sqrt(Q) [m].
    """
    (q,), is_scalar = coerce_inputs(discharge)
    with np.errstate(all='ignore'):
        p = np.where(q <= 0, np.nan, 4.75 * np.sqrt(q))
    return format_output(p, is_scalar)


def lacey_perimeter_discharge(
    wetted_perimeter: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for regime discharge Q = (P / 4.75)^2."""
    (p,), is_scalar = coerce_inputs(wetted_perimeter)
    with np.errstate(all='ignore'):
        q = np.where(p <= 0, np.nan, (p / 4.75) ** 2)
    return format_output(q, is_scalar)


def lacey_hydraulic_radius(
    discharge: FloatOrArray,
    silt_factor: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes Lacey's regime hydraulic radius R = 0.48 * (Q / f)^(1/3) [m].
    """
    (q, f), is_scalar = coerce_inputs(discharge, silt_factor)
    with np.errstate(all='ignore'):
        r = np.where((q <= 0) | (f <= 0), np.nan, 0.48 * ((q / f) ** (1.0 / 3.0)))
    return format_output(r, is_scalar)


def lacey_regime_slope(
    discharge: FloatOrArray,
    silt_factor: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes Lacey's regime channel bed slope S.

    Formula:
        S = f^(5/3) / (3340 * Q^(1/6))  [dimensionless m/m]
    """
    (q, f), is_scalar = coerce_inputs(discharge, silt_factor)
    with np.errstate(all='ignore'):
        s = np.where((q <= 0) | (f <= 0), np.nan, (f ** (5.0 / 3.0)) / (3340.0 * (q ** (1.0 / 6.0))))
    return format_output(s, is_scalar)


def lacey_slope_discharge(
    slope: FloatOrArray,
    silt_factor: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for regime discharge Q = (f^(5/3) / (3340 * S))^6."""
    (s, f), is_scalar = coerce_inputs(slope, silt_factor)
    with np.errstate(all='ignore'):
        q = np.where((s <= 0) | (f <= 0), np.nan, ((f ** (5.0 / 3.0)) / (3340.0 * s)) ** 6.0)
    return format_output(q, is_scalar)


def lacey_regime_scour_depth(
    discharge: FloatOrArray,
    silt_factor: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes Lacey's normal regime scour depth R_scour = 0.473 * (Q / f)^(1/3) [m].
    """
    (q, f), is_scalar = coerce_inputs(discharge, silt_factor)
    with np.errstate(all='ignore'):
        r = np.where((q <= 0) | (f <= 0), np.nan, 0.473 * ((q / f) ** (1.0 / 3.0)))
    return format_output(r, is_scalar)


def kennedy_critical_velocity(
    depth: FloatOrArray,
    cvr_m: FloatOrArray = 1.0,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes non-silting critical velocity V_0 using Kennedy's formula.

    Formula:
        SI: V_0 = 0.55 * m * y^0.64  [y in m, V_0 in m/s]
        US: V_0 = 0.84 * m * y^0.64  [y in ft, V_0 in ft/s]
    """
    (y, m), is_scalar = coerce_inputs(depth, cvr_m)
    k = 0.84 if system.lower() == "us" else 0.55
    with np.errstate(all='ignore'):
        v = np.where((y <= 0) | (m <= 0), np.nan, k * m * (y ** 0.64))
    return format_output(v, is_scalar)


def kennedy_critical_depth(
    velocity: FloatOrArray,
    cvr_m: FloatOrArray = 1.0,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for flow depth y = (V_0 / (k * m))^(1 / 0.64)."""
    (v, m), is_scalar = coerce_inputs(velocity, cvr_m)
    k = 0.84 if system.lower() == "us" else 0.55
    with np.errstate(all='ignore'):
        y = np.where((v <= 0) | (m <= 0), np.nan, (v / (k * m)) ** (1.0 / 0.64))
    return format_output(y, is_scalar)


# =============================================================================
# TRANSITIONS, MINOR LOSSES & CAVITATION
# =============================================================================

def channel_expansion_loss(
    velocity_1: FloatOrArray,
    velocity_2: FloatOrArray,
    ke: FloatOrArray = 0.5,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes open channel expansion transition energy head loss h_L = K_e * (V_1 - V_2)^2 / (2g).
    """
    (v1, v2, k_val), is_scalar = coerce_inputs(velocity_1, velocity_2, ke)
    g = 32.17405 if system.lower() == "us" else 9.80665
    with np.errstate(all='ignore'):
        hl = k_val * ((v1 - v2) ** 2) / (2.0 * g)
    return format_output(hl, is_scalar)


def channel_contraction_loss(
    velocity_1: FloatOrArray,
    velocity_2: FloatOrArray,
    kc: FloatOrArray = 0.1,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes open channel contraction transition energy head loss h_L = K_c * |V_2^2 - V_1^2| / (2g).
    """
    (v1, v2, k_val), is_scalar = coerce_inputs(velocity_1, velocity_2, kc)
    g = 32.17405 if system.lower() == "us" else 9.80665
    with np.errstate(all='ignore'):
        hl = k_val * np.abs((v2 ** 2) - (v1 ** 2)) / (2.0 * g)
    return format_output(hl, is_scalar)


def blasius_friction_factor(
    reynolds: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes Darcy friction factor for smooth pipes in turbulent flow (Re < 10^5) using Blasius' formula:
    f = 0.3164 / Re^0.25
    """
    (re,), is_scalar = coerce_inputs(reynolds)
    with np.errstate(all='ignore'):
        f = np.where(re <= 0, np.nan, 0.3164 / (re ** 0.25))
    return format_output(f, is_scalar)


def cavitation_index(
    pressure_abs: FloatOrArray,
    vapor_pressure: FloatOrArray,
    velocity: FloatOrArray,
    density: FloatOrArray = 1000.0,
) -> Union[float, np.ndarray]:
    """
    Computes Thoma cavitation index sigma = (P_abs - P_v) / (0.5 * rho * V^2).
    """
    (p, pv, v, rho), is_scalar = coerce_inputs(pressure_abs, vapor_pressure, velocity, density)
    with np.errstate(all='ignore'):
        sig = np.where(v <= 0, np.nan, (p - pv) / (0.5 * rho * (v ** 2)))
    return format_output(sig, is_scalar)


def cavitation_velocity(
    pressure_abs: FloatOrArray,
    vapor_pressure: FloatOrArray,
    sigma_critical: FloatOrArray,
    density: FloatOrArray = 1000.0,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for maximum permissible velocity before cavitation occurs."""
    (p, pv, sig, rho), is_scalar = coerce_inputs(pressure_abs, vapor_pressure, sigma_critical, density)
    with np.errstate(all='ignore'):
        v = np.where((p <= pv) | (sig <= 0), np.nan, np.sqrt((p - pv) / (0.5 * rho * sig)))
    return format_output(v, is_scalar)
'''


# -----------------------------------------------------------------------------
# 3. STRUCTURES EXTENSIONS CODE
# -----------------------------------------------------------------------------
STRUCTURES_EXTENSIONS = '''

# =============================================================================
# SPECIALIZED WEIRS, FLUMES & BRIDGE PIER SCOUR
# =============================================================================

def cipoletti_weir_q(
    length: FloatOrArray,
    head: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes discharge Q over a Cipoletti (trapezoidal 4V:1H) weir.

    Formula:
        SI: Q = 1.860 * L * H^(3/2)  [L in m, H in m, Q in m^3/s]
        US: Q = 3.367 * L * H^(3/2)  [L in ft, H in ft, Q in cfs]
    """
    (l, h), is_scalar = coerce_inputs(length, head)
    k = 3.367 if system.lower() == "us" else 1.860
    with np.errstate(all='ignore'):
        q = np.where((l <= 0) | (h <= 0), np.nan, k * l * (h ** 1.5))
    return format_output(q, is_scalar)


def cipoletti_weir_l(
    discharge: FloatOrArray,
    head: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for required Cipoletti crest length L = Q / (k * H^1.5)."""
    (q, h), is_scalar = coerce_inputs(discharge, head)
    k = 3.367 if system.lower() == "us" else 1.860
    with np.errstate(all='ignore'):
        l = np.where((q <= 0) | (h <= 0), np.nan, q / (k * (h ** 1.5)))
    return format_output(l, is_scalar)


def cipoletti_weir_h(
    discharge: FloatOrArray,
    length: FloatOrArray,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for head H = (Q / (k * L))^(2/3)."""
    (q, l), is_scalar = coerce_inputs(discharge, length)
    k = 3.367 if system.lower() == "us" else 1.860
    with np.errstate(all='ignore'):
        h = np.where((q <= 0) | (l <= 0), np.nan, (q / (k * l)) ** (2.0 / 3.0))
    return format_output(h, is_scalar)


def sutro_weir_q(
    base_width: FloatOrArray,
    base_height: FloatOrArray,
    head: FloatOrArray,
    cd: FloatOrArray = 0.62,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes discharge Q for a Sutro (proportional linear) weir.

    Formula:
        Q = C_d * b * sqrt(2 * g * a) * (H - a/3)
    """
    (b, a, h, cd_v), is_scalar = coerce_inputs(base_width, base_height, head, cd)
    g = 32.17405 if system.lower() == "us" else 9.80665
    with np.errstate(all='ignore'):
        q = np.where((b <= 0) | (a <= 0) | (h < a), np.nan, cd_v * b * np.sqrt(2.0 * g * a) * (h - (a / 3.0)))
    return format_output(q, is_scalar)


def sutro_weir_h(
    discharge: FloatOrArray,
    base_width: FloatOrArray,
    base_height: FloatOrArray,
    cd: FloatOrArray = 0.62,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for required head H on Sutro weir."""
    (q, b, a, cd_v), is_scalar = coerce_inputs(discharge, base_width, base_height, cd)
    g = 32.17405 if system.lower() == "us" else 9.80665
    with np.errstate(all='ignore'):
        denom = cd_v * b * np.sqrt(2.0 * g * a)
        h = np.where((q <= 0) | (denom <= 0), np.nan, (q / denom) + (a / 3.0))
    return format_output(h, is_scalar)


def hec18_pier_scour(
    pier_width: FloatOrArray,
    flow_depth: FloatOrArray,
    flow_velocity: FloatOrArray,
    k1: FloatOrArray = 1.0,
    k2: FloatOrArray = 1.0,
    k3: FloatOrArray = 1.0,
    k4: FloatOrArray = 1.0,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """
    Computes bridge pier scour depth ys using the FHWA HEC-18 (Richardson & Davis CSU) formula.

    Formula:
        y_s = 2.0 * K_1 * K_2 * K_3 * K_4 * y_1 * (a / y_1)^0.65 * Fr_1^0.43
    """
    (a, y, v, k1_v, k2_v, k3_v, k4_v), is_scalar = coerce_inputs(
        pier_width, flow_depth, flow_velocity, k1, k2, k3, k4
    )
    g = 32.17405 if system.lower() == "us" else 9.80665
    with np.errstate(all='ignore'):
        fr = v / np.sqrt(g * y)
        ys = 2.0 * k1_v * k2_v * k3_v * k4_v * y * ((a / y) ** 0.65) * (fr ** 0.43)
    return format_output(ys, is_scalar)


def hec18_pier_width(
    scour_depth: FloatOrArray,
    flow_depth: FloatOrArray,
    flow_velocity: FloatOrArray,
    k1: FloatOrArray = 1.0,
    k2: FloatOrArray = 1.0,
    k3: FloatOrArray = 1.0,
    k4: FloatOrArray = 1.0,
    system: Literal["si", "us"] = "si",
) -> Union[float, np.ndarray]:
    """Inversion: Solves for maximum permissible pier width 'a' for a given allowable scour depth."""
    (ys, y, v, k1_v, k2_v, k3_v, k4_v), is_scalar = coerce_inputs(
        scour_depth, flow_depth, flow_velocity, k1, k2, k3, k4
    )
    g = 32.17405 if system.lower() == "us" else 9.80665
    with np.errstate(all='ignore'):
        fr = v / np.sqrt(g * y)
        denom = 2.0 * k1_v * k2_v * k3_v * k4_v * y * (fr ** 0.43)
        a = y * ((ys / denom) ** (1.0 / 0.65))
    return format_output(a, is_scalar)
'''


# -----------------------------------------------------------------------------
# 4. GROUNDWATER EXTENSIONS CODE
# -----------------------------------------------------------------------------
GROUNDWATER_EXTENSIONS = '''

# =============================================================================
# EXTENDED GROUNDWATER & COASTAL AQUIFER HYDRAULICS
# =============================================================================

def ghyben_herzberg_depth(
    freshwater_head: FloatOrArray,
    rho_f: FloatOrArray = 1000.0,
    rho_s: FloatOrArray = 1025.0,
) -> Union[float, np.ndarray]:
    """
    Computes depth z to freshwater-saltwater interface below sea level via the Ghyben-Herzberg relation.

    Formula:
        z = (rho_f / (rho_s - rho_f)) * h_f ~ 40.0 * h_f
    """
    (hf, rf, rs), is_scalar = coerce_inputs(freshwater_head, rho_f, rho_s)
    with np.errstate(all='ignore'):
        z = np.where((hf <= 0) | (rs <= rf), np.nan, (rf / (rs - rf)) * hf)
    return format_output(z, is_scalar)


def ghyben_herzberg_head(
    interface_depth: FloatOrArray,
    rho_f: FloatOrArray = 1000.0,
    rho_s: FloatOrArray = 1025.0,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for freshwater water table elevation h_f = ((rho_s - rho_f) / rho_f) * z."""
    (z, rf, rs), is_scalar = coerce_inputs(interface_depth, rho_f, rho_s)
    with np.errstate(all='ignore'):
        hf = np.where((z <= 0) | (rs <= rf), np.nan, ((rs - rf) / rf) * z)
    return format_output(hf, is_scalar)


def jacob_well_drawdown(
    discharge: FloatOrArray,
    b_coeff: FloatOrArray,
    c_coeff: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes total well pumping drawdown sw using Jacob's well loss equation:
    s_w = B * Q + C * Q^2
    """
    (q, b, c), is_scalar = coerce_inputs(discharge, b_coeff, c_coeff)
    with np.errstate(all='ignore'):
        sw = (b * q) + (c * (q ** 2))
    return format_output(sw, is_scalar)


def jacob_well_efficiency(
    discharge: FloatOrArray,
    b_coeff: FloatOrArray,
    c_coeff: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes pumping well efficiency Ew = (B * Q / (B * Q + C * Q^2)) * 100%.
    """
    (q, b, c), is_scalar = coerce_inputs(discharge, b_coeff, c_coeff)
    with np.errstate(all='ignore'):
        tot = (b * q) + (c * (q ** 2))
        eff = np.where(tot <= 0, np.nan, ((b * q) / tot) * 100.0)
    return format_output(eff, is_scalar)


def jacob_well_b(
    drawdown: FloatOrArray,
    discharge: FloatOrArray,
    c_coeff: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for aquifer laminar loss coefficient B = (s_w - C * Q^2) / Q."""
    (sw, q, c), is_scalar = coerce_inputs(drawdown, discharge, c_coeff)
    with np.errstate(all='ignore'):
        b = np.where(q <= 0, np.nan, (sw - (c * (q ** 2))) / q)
    return format_output(b, is_scalar)


def jacob_well_c(
    drawdown: FloatOrArray,
    discharge: FloatOrArray,
    b_coeff: FloatOrArray,
) -> Union[float, np.ndarray]:
    """Inversion: Solves for well turbulence loss coefficient C = (s_w - B * Q) / Q^2."""
    (sw, q, b), is_scalar = coerce_inputs(drawdown, discharge, b_coeff)
    with np.errstate(all='ignore'):
        c = np.where(q <= 0, np.nan, (sw - (b * q)) / (q ** 2))
    return format_output(c, is_scalar)


def hantush_leakage_factor(
    transmissivity: FloatOrArray,
    aquitard_thickness: FloatOrArray,
    aquitard_conductivity: FloatOrArray,
) -> Union[float, np.ndarray]:
    """
    Computes Hantush-Jacob leakage factor B = sqrt(T * b' / K') [m] for a leaky confined aquifer.
    """
    (t, b_prime, k_prime), is_scalar = coerce_inputs(transmissivity, aquitard_thickness, aquitard_conductivity)
    with np.errstate(all='ignore'):
        b = np.where((t <= 0) | (b_prime <= 0) | (k_prime <= 0), np.nan, np.sqrt((t * b_prime) / k_prime))
    return format_output(b, is_scalar)


def specific_capacity_to_transmissivity(
    discharge: FloatOrArray,
    drawdown: FloatOrArray,
    aquifer_type: str = "confined",
) -> Union[float, np.ndarray]:
    """
    Estimates aquifer transmissivity T from well specific capacity (Q / sw) using Thomasson / Driscoll empirical relations:
    Confined: T ~ 1500 * (Q / sw) [m^2/day]
    Unconfined: T ~ 1000 * (Q / sw) [m^2/day]
    """
    (q, sw), is_scalar = coerce_inputs(discharge, drawdown)
    k = 1000.0 if "unconfined" in aquifer_type.lower() else 1500.0
    with np.errstate(all='ignore'):
        t = np.where((q <= 0) | (sw <= 0), np.nan, k * (q / sw))
    return format_output(t, is_scalar)
'''


def append_and_validate(filepath: str, code_to_append: str):
    with open(filepath, "r", encoding="utf-8") as f:
        existing = f.read()

    # Append code
    new_content = existing.strip() + "\n\n" + code_to_append.strip() + "\n"
    
    # Validate syntax with AST
    ast.parse(new_content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Successfully updated and validated: {filepath}")


def update_init_py():
    init_path = os.path.join(PY_DIR, "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Append imports to __init__.py
    additional_exports = '''
# --- Extended Hydrology Suite ---
from .hydrology import (
    faa_tc, faa_l, faa_s, faa_c,
    kerby_tc, kerby_l, kerby_s, kerby_n,
    bransby_williams_tc, bransby_williams_l, bransby_williams_a, bransby_williams_s,
    tr55_channel_tc, tr55_composite_tc,
    dickens_q, dickens_cd, dickens_area,
    ryves_q, ryves_cr, ryves_area,
    inglis_q, inglis_area,
    nawab_jung_q, nawab_jung_cn, nawab_jung_area,
    fuller_flood_q, fuller_return_period,
    philip_rate, philip_cumulative, philip_sorptivity,
    kostiakov_rate, kostiakov_cumulative, kostiakov_time,
    green_ampt_ponding_time,
    saturation_vapor_pressure, vapor_pressure_slope,
    fao56_penman_monteith, fao56_net_radiation,
    priestley_taylor_et, blaney_criddle_et, blaney_criddle_temp,
    scs_unit_hydrograph_peak, scs_uh_tp, scs_uh_area, scs_lag_time, scs_time_to_peak,
    snyder_lag_time, snyder_peak_discharge, snyder_hydrograph_widths,
    muskingum_cunge_parameters, baseflow_lyne_hollick,
    gumbel_reduced_variate, gumbel_return_period, gumbel_frequency_factor,
    gumbel_design_flood, gumbel_return_period_from_flood,
    log_pearson_3_flood, weibull_plotting_position, gringorten_plotting_position, cunnane_plotting_position,
)

# --- Extended Hydraulics & Alluvial Regime Suite ---
from .hydraulics import (
    lacey_silt_factor, lacey_d50, lacey_regime_velocity, lacey_velocity_discharge,
    lacey_wetted_perimeter, lacey_perimeter_discharge, lacey_hydraulic_radius,
    lacey_regime_slope, lacey_slope_discharge, lacey_regime_scour_depth,
    kennedy_critical_velocity, kennedy_critical_depth,
    channel_expansion_loss, channel_contraction_loss,
    blasius_friction_factor, cavitation_index, cavitation_velocity,
)

# --- Extended Structures Suite ---
from .structures import (
    cipoletti_weir_q, cipoletti_weir_l, cipoletti_weir_h,
    sutro_weir_q, sutro_weir_h,
    hec18_pier_scour, hec18_pier_width,
)

# --- Extended Groundwater Suite ---
from .groundwater import (
    ghyben_herzberg_depth, ghyben_herzberg_head,
    jacob_well_drawdown, jacob_well_efficiency, jacob_well_b, jacob_well_c,
    hantush_leakage_factor, specific_capacity_to_transmissivity,
)
'''
    new_init = content.strip() + "\n\n" + additional_exports.strip() + "\n"
    ast.parse(new_init)
    with open(init_path, "w", encoding="utf-8") as f:
        f.write(new_init)
    print("Successfully updated __init__.py")


def main():
    append_and_validate(os.path.join(PY_DIR, "hydrology.py"), HYDROLOGY_EXTENSIONS)
    append_and_validate(os.path.join(PY_DIR, "hydraulics.py"), HYDRAULICS_EXTENSIONS)
    append_and_validate(os.path.join(PY_DIR, "structures.py"), STRUCTURES_EXTENSIONS)
    append_and_validate(os.path.join(PY_DIR, "groundwater.py"), GROUNDWATER_EXTENSIONS)
    update_init_py()
    print("All modules expanded with expert formulas successfully!")


if __name__ == "__main__":
    main()

