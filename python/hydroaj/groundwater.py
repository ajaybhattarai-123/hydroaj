"""
Seepage & Groundwater Module API.
Provides polymorphic scalar and vectorized calculations for Darcy flow,
Thiem equilibrium well equations, and Theis transient well drawdown.
"""
from typing import Any, Tuple, Union, Sequence, Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import numpy as np
FloatOrArray = Union[float, int, Sequence[float], np.ndarray]
from . import _hydroaj_core as _core
from ._coercion import coerce_inputs, format_output

def darcy_flow_1d(hydraulic_conductivity: FloatOrArray, area: FloatOrArray, hydraulic_gradient: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes darcy flow 1d.
    Units (Default SI): hydraulic_conductivity [m/s], area [m^2], hydraulic_gradient [m/m] -> returns [standard SI units]

    Formula:
    Q = -K * A * (dh / dl)

    Where (Default SI Units):
    - hydraulic_conductivity : Darcy saturated hydraulic conductivity K [unit = m/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - hydraulic_gradient : Piezometric gradient i = dh / dl [unit = m/m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_conductivity : FloatOrArray
        Darcy saturated hydraulic conductivity K [m/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    hydraulic_gradient : FloatOrArray
        Piezometric gradient i = dh / dl [m/m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (k, a, grad), is_scalar = coerce_inputs(hydraulic_conductivity, area, hydraulic_gradient)
    out = _core.darcy_flow_1d(k, a, grad)
    return format_output(out, is_scalar)

def darcy_flux(hydraulic_conductivity: FloatOrArray, hydraulic_gradient: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes darcy flux.
    Units (Default SI): hydraulic_conductivity [m/s], hydraulic_gradient [m/m] -> returns [standard SI units]

    Formula:
    q = -K * (dh / dl)

    Where (Default SI Units):
    - hydraulic_conductivity : Darcy saturated hydraulic conductivity K [unit = m/s]
    - hydraulic_gradient : Piezometric gradient i = dh / dl [unit = m/m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_conductivity : FloatOrArray
        Darcy saturated hydraulic conductivity K [m/s].
    hydraulic_gradient : FloatOrArray
        Piezometric gradient i = dh / dl [m/m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (k, grad), is_scalar = coerce_inputs(hydraulic_conductivity, hydraulic_gradient)
    out = _core.darcy_flux(k, grad)
    return format_output(out, is_scalar)

def thiem_confined(transmissivity: FloatOrArray, h1: FloatOrArray, h2: FloatOrArray, r1: FloatOrArray, r2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Thiem steady-state pumping rate for confined aquifer:
    Units (Default SI): transmissivity [m^2/s], h1 [m], h2 [m], r1 [m], r2 [m] -> returns [standard SI units]

    Formula:
    Q = (2 * pi * T * (h_2 - h_1)) / ln(r_2 / r_1)

    Where (Default SI Units):
    - transmissivity : Aquifer transmissivity T [unit = m^2/s]
    - h1 : Hydraulic head at well 1 (h_1) [unit = m]
    - h2 : Hydraulic head at well 2 (h_2) [unit = m]
    - r1 : Distance to observation well 1 (r_1) [unit = m]
    - r2 : Distance to observation well 2 (r_2) [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    transmissivity : FloatOrArray
        Aquifer transmissivity T [m^2/s].
    h1 : FloatOrArray
        Hydraulic head at well 1 (h_1) [m].
    h2 : FloatOrArray
        Hydraulic head at well 2 (h_2) [m].
    r1 : FloatOrArray
        Distance to observation well 1 (r_1) [m].
    r2 : FloatOrArray
        Distance to observation well 2 (r_2) [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, head1, head2, rad1, rad2), is_scalar = coerce_inputs(transmissivity, h1, h2, r1, r2)
    out = _core.thiem_confined(t, head1, head2, rad1, rad2)
    return format_output(out, is_scalar)

def thiem_unconfined(hydraulic_conductivity: FloatOrArray, h1: FloatOrArray, h2: FloatOrArray, r1: FloatOrArray, r2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Thiem (Dupuit) steady-state pumping rate for unconfined aquifer:
    Units (Default SI): hydraulic_conductivity [m/s], h1 [m], h2 [m], r1 [m], r2 [m] -> returns [standard SI units]

    Formula:
    Q = (pi * K * (h_2^2 - h_1^2)) / ln(r_2 / r_1)

    Where (Default SI Units):
    - hydraulic_conductivity : Darcy saturated hydraulic conductivity K [unit = m/s]
    - h1 : Hydraulic head at well 1 (h_1) [unit = m]
    - h2 : Hydraulic head at well 2 (h_2) [unit = m]
    - r1 : Distance to observation well 1 (r_1) [unit = m]
    - r2 : Distance to observation well 2 (r_2) [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_conductivity : FloatOrArray
        Darcy saturated hydraulic conductivity K [m/s].
    h1 : FloatOrArray
        Hydraulic head at well 1 (h_1) [m].
    h2 : FloatOrArray
        Hydraulic head at well 2 (h_2) [m].
    r1 : FloatOrArray
        Distance to observation well 1 (r_1) [m].
    r2 : FloatOrArray
        Distance to observation well 2 (r_2) [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (k, head1, head2, rad1, rad2), is_scalar = coerce_inputs(hydraulic_conductivity, h1, h2, r1, r2)
    out = _core.thiem_unconfined(k, head1, head2, rad1, rad2)
    return format_output(out, is_scalar)

def theis_drawdown(pumping_rate: FloatOrArray, transmissivity: FloatOrArray, storativity: FloatOrArray, radius: FloatOrArray, time: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes theis drawdown.
    Units (Default SI): pumping_rate [SI units], transmissivity [m^2/s], storativity [dimensionless], radius [SI units], time [hours] -> returns [standard SI units]

    Formula:
    s = (Q / (4 * pi * T)) * W(u); u = (r^2 * S) / (4 * T * t)

    Where (Default SI Units):
    - pumping_rate : Input parameter [unit = SI units]
    - transmissivity : Aquifer transmissivity T [unit = m^2/s]
    - storativity : Aquifer storativity / storage coefficient S [unit = dimensionless]
    - radius : Input parameter [unit = SI units]
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    pumping_rate : FloatOrArray
        pumping_rate [SI units].
    transmissivity : FloatOrArray
        Aquifer transmissivity T [m^2/s].
    storativity : FloatOrArray
        Aquifer storativity / storage coefficient S [dimensionless].
    radius : FloatOrArray
        radius [SI units].
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, t, s, r, time_val), is_scalar = coerce_inputs(pumping_rate, transmissivity, storativity, radius, time)
    out = _core.theis_drawdown(q, t, s, r, time_val)
    return format_output(out, is_scalar)

def cooper_jacob_drawdown(pumping_rate: FloatOrArray, transmissivity: FloatOrArray, storativity: FloatOrArray, radius: FloatOrArray, time: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes cooper jacob drawdown.
    Units (Default SI): pumping_rate [SI units], transmissivity [m^2/s], storativity [dimensionless], radius [SI units], time [hours] -> returns [standard SI units]

    Formula:
    s = (2.303 * Q / (4 * pi * T)) * log10((2.25 * T * t) / (r^2 * S))

    Where (Default SI Units):
    - pumping_rate : Input parameter [unit = SI units]
    - transmissivity : Aquifer transmissivity T [unit = m^2/s]
    - storativity : Aquifer storativity / storage coefficient S [unit = dimensionless]
    - radius : Input parameter [unit = SI units]
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    pumping_rate : FloatOrArray
        pumping_rate [SI units].
    transmissivity : FloatOrArray
        Aquifer transmissivity T [m^2/s].
    storativity : FloatOrArray
        Aquifer storativity / storage coefficient S [dimensionless].
    radius : FloatOrArray
        radius [SI units].
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, t, s, r, time_val), is_scalar = coerce_inputs(pumping_rate, transmissivity, storativity, radius, time)
    out = _core.cooper_jacob_drawdown(q, t, s, r, time_val)
    return format_output(out, is_scalar)
darcy_flow_q = darcy_flow_1d

def darcy_flow_k(discharge: FloatOrArray, area: FloatOrArray, hydraulic_gradient: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes darcy flow k.
    Units (Default SI): discharge [m^3/s], area [m^2], hydraulic_gradient [m/m] -> returns [standard SI units]

    Formula:
    K = -Q / (A * dh_dl)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - hydraulic_gradient : Piezometric gradient i = dh / dl [unit = m/m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].
    hydraulic_gradient : FloatOrArray
        Piezometric gradient i = dh / dl [m/m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, a, grad), is_scalar = coerce_inputs(discharge, area, hydraulic_gradient)
    out = _core.darcy_flow_k(q, a, grad)
    return format_output(out, is_scalar)
darcy_hydraulic_conductivity = darcy_flow_k

def darcy_flow_dh_dl(discharge: FloatOrArray, hydraulic_conductivity: FloatOrArray, area: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Hydraulic gradient dh_dl = -Q / (K * A)
    Units (Default SI): discharge [m^3/s], hydraulic_conductivity [m/s], area [m^2] -> returns [standard SI units]

    Formula:
    Inversion: Hydraulic gradient dh_dl = -Q / (K * A)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - hydraulic_conductivity : Darcy saturated hydraulic conductivity K [unit = m/s]
    - area : Cross-sectional flow area A [unit = m^2]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    hydraulic_conductivity : FloatOrArray
        Darcy saturated hydraulic conductivity K [m/s].
    area : FloatOrArray
        Cross-sectional flow area A [m^2].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, k, a), is_scalar = coerce_inputs(discharge, hydraulic_conductivity, area)
    out = _core.darcy_flow_dh_dl(q, k, a)
    return format_output(out, is_scalar)
darcy_hydraulic_gradient = darcy_flow_dh_dl
thiem_confined_q = thiem_confined

def thiem_confined_t(discharge: FloatOrArray, head_1: FloatOrArray, head_2: FloatOrArray, radius_1: FloatOrArray, radius_2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes thiem confined t.
    Units (Default SI): discharge [m^3/s], head_1 [m], head_2 [m], radius_1 [m], radius_2 [m] -> returns [m^2/s (or m^2/day)]

    Formula:
    T = Q * ln(r_2 / r_1) / (2 * pi * (h_2 - h_1))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - head_1 : Hydraulic head [unit = m]
    - head_2 : Hydraulic head [unit = m]
    - radius_1 : Distance to near observation well r_1 [unit = m]
    - radius_2 : Distance to far observation well r_2 [unit = m]
    - Output : Aquifer transmissivity [unit = m^2/s (or m^2/day)]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    head_1 : FloatOrArray
        head_1 [SI units].
    head_2 : FloatOrArray
        head_2 [SI units].
    radius_1 : FloatOrArray
        Distance to near observation well r_1 [m].
    radius_2 : FloatOrArray
        Distance to far observation well r_2 [m].

    Returns
    -------
    float | np.ndarray
        Aquifer transmissivity [m^2/s (or m^2/day)]. Returns float for scalar inputs.
    """
    (q, h1, h2, r1, r2), is_scalar = coerce_inputs(discharge, head_1, head_2, radius_1, radius_2)
    out = _core.thiem_confined_t(q, h1, h2, r1, r2)
    return format_output(out, is_scalar)
thiem_confined_transmissivity = thiem_confined_t

def thiem_confined_dh(discharge: FloatOrArray, transmissivity: FloatOrArray, radius_1: FloatOrArray, radius_2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Head difference (h_2 - h_1) = (Q * ln(r_2 / r_1)) / (2 * pi * T)
    Units (Default SI): discharge [m^3/s], transmissivity [m^2/s], radius_1 [m], radius_2 [m] -> returns [standard SI units]

    Formula:
    Inversion: Head difference (h_2 - h_1) = (Q * ln(r_2 / r_1)) / (2 * pi * T)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - transmissivity : Aquifer transmissivity T [unit = m^2/s]
    - radius_1 : Distance to near observation well r_1 [unit = m]
    - radius_2 : Distance to far observation well r_2 [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    transmissivity : FloatOrArray
        Aquifer transmissivity T [m^2/s].
    radius_1 : FloatOrArray
        Distance to near observation well r_1 [m].
    radius_2 : FloatOrArray
        Distance to far observation well r_2 [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, t, r1, r2), is_scalar = coerce_inputs(discharge, transmissivity, radius_1, radius_2)
    out = _core.thiem_confined_dh(q, t, r1, r2)
    return format_output(out, is_scalar)
thiem_confined_drawdown_diff = thiem_confined_dh
thiem_unconfined_q = thiem_unconfined

def thiem_unconfined_k(discharge: FloatOrArray, head_1: FloatOrArray, head_2: FloatOrArray, radius_1: FloatOrArray, radius_2: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Hydraulic conductivity K = (Q * ln(r_2 / r_1)) / (pi * (h_2^2 - h_1^2))
    Units (Default SI): discharge [m^3/s], head_1 [m], head_2 [m], radius_1 [m], radius_2 [m] -> returns [standard SI units]

    Formula:
    Inversion: Hydraulic conductivity K = (Q * ln(r_2 / r_1)) / (pi * (h_2^2 - h_1^2))

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - head_1 : Hydraulic head [unit = m]
    - head_2 : Hydraulic head [unit = m]
    - radius_1 : Distance to near observation well r_1 [unit = m]
    - radius_2 : Distance to far observation well r_2 [unit = m]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    head_1 : FloatOrArray
        head_1 [SI units].
    head_2 : FloatOrArray
        head_2 [SI units].
    radius_1 : FloatOrArray
        Distance to near observation well r_1 [m].
    radius_2 : FloatOrArray
        Distance to far observation well r_2 [m].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, h1, h2, r1, r2), is_scalar = coerce_inputs(discharge, head_1, head_2, radius_1, radius_2)
    out = _core.thiem_unconfined_k(q, h1, h2, r1, r2)
    return format_output(out, is_scalar)
thiem_unconfined_conductivity = thiem_unconfined_k
cooper_jacob_s = cooper_jacob_drawdown

def cooper_jacob_q(drawdown: FloatOrArray, transmissivity: FloatOrArray, storativity: FloatOrArray, radius: FloatOrArray, time: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Equilibrium pumping rate Q = (4 * pi * T * s) / (2.302585 * log10((2.25 * T * t) / (r^2 * S)))
    Units (Default SI): drawdown [m], transmissivity [m^2/s], storativity [dimensionless], radius [SI units], time [hours] -> returns [m^3/s]

    Formula:
    Inversion: Equilibrium pumping rate Q = (4 * pi * T * s) / (2.302585 * log10((2.25 * T * t) / (r^2 * S)))

    Where (Default SI Units):
    - drawdown : Pumping well water level drawdown s_w [unit = m]
    - transmissivity : Aquifer transmissivity T [unit = m^2/s]
    - storativity : Aquifer storativity / storage coefficient S [unit = dimensionless]
    - radius : Input parameter [unit = SI units]
    - time : Elapsed infiltration or pumping time t [unit = hours]
    - Output : Volumetric flow discharge [unit = m^3/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    drawdown : FloatOrArray
        Pumping well water level drawdown s_w [m].
    transmissivity : FloatOrArray
        Aquifer transmissivity T [m^2/s].
    storativity : FloatOrArray
        Aquifer storativity / storage coefficient S [dimensionless].
    radius : FloatOrArray
        radius [SI units].
    time : FloatOrArray
        Elapsed infiltration or pumping time t [hours].

    Returns
    -------
    float | np.ndarray
        Volumetric flow discharge [m^3/s]. Returns float for scalar inputs.
    """
    (s, t, stor, r, time_val), is_scalar = coerce_inputs(drawdown, transmissivity, storativity, radius, time)
    out = _core.cooper_jacob_q(s, t, stor, r, time_val)
    return format_output(out, is_scalar)
cooper_jacob_pumping_rate = cooper_jacob_q

def ghyben_herzberg_depth(freshwater_head: FloatOrArray, rho_f: FloatOrArray=1000.0, rho_s: FloatOrArray=1025.0) -> Union[float, np.ndarray]:
    """
    Computes depth z to freshwater-saltwater interface below sea level via the Ghyben-Herzberg relation.
    Units (Default SI): freshwater_head [m], rho_f [kg/m^3 (~1000.0)], rho_s [kg/m^3 (~1025.0)] -> returns [m]

    Formula:
    z = (rho_f / (rho_s - rho_f)) * h_f ~ 40.0 * h_f

    Where (Default SI Units):
    - freshwater_head : Freshwater water table elevation above sea level h_f [unit = m]
    - rho_f : Density of freshwater rho_f [unit = kg/m^3 (~1000.0)]
    - rho_s : Density of saltwater rho_s [unit = kg/m^3 (~1025.0)]
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    freshwater_head : FloatOrArray
        Freshwater water table elevation above sea level h_f [m].
    rho_f : FloatOrArray
        Density of freshwater rho_f [kg/m^3 (~1000.0)].
    rho_s : FloatOrArray
        Density of saltwater rho_s [kg/m^3 (~1025.0)].

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (hf, rf, rs), is_scalar = coerce_inputs(freshwater_head, rho_f, rho_s)
    with np.errstate(all='ignore'):
        z = np.where((hf <= 0) | (rs <= rf), np.nan, rf / (rs - rf) * hf)
    return format_output(z, is_scalar)

def ghyben_herzberg_head(interface_depth: FloatOrArray, rho_f: FloatOrArray=1000.0, rho_s: FloatOrArray=1025.0) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for freshwater water table elevation h_f = ((rho_s - rho_f) / rho_f) * z.
    Units (Default SI): interface_depth [m], rho_f [kg/m^3 (~1000.0)], rho_s [kg/m^3 (~1025.0)] -> returns [m]

    Formula:
    Inversion: Solves for freshwater water table elevation h_f = ((rho_s - rho_f) / rho_f) * z.

    Where (Default SI Units):
    - interface_depth : Depth to freshwater-saltwater interface below sea level z [unit = m]
    - rho_f : Density of freshwater rho_f [unit = kg/m^3 (~1000.0)]
    - rho_s : Density of saltwater rho_s [unit = kg/m^3 (~1025.0)]
    - Output : Hydraulic head / depth [unit = m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    interface_depth : FloatOrArray
        Depth to freshwater-saltwater interface below sea level z [m].
    rho_f : FloatOrArray
        Density of freshwater rho_f [kg/m^3 (~1000.0)].
    rho_s : FloatOrArray
        Density of saltwater rho_s [kg/m^3 (~1025.0)].

    Returns
    -------
    float | np.ndarray
        Hydraulic head / depth [m]. Returns float for scalar inputs.
    """
    (z, rf, rs), is_scalar = coerce_inputs(interface_depth, rho_f, rho_s)
    with np.errstate(all='ignore'):
        hf = np.where((z <= 0) | (rs <= rf), np.nan, (rs - rf) / rf * z)
    return format_output(hf, is_scalar)

def jacob_well_drawdown(discharge: FloatOrArray, b_coeff: FloatOrArray, c_coeff: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes total well pumping drawdown sw using Jacob's well loss equation:
    Units (Default SI): discharge [m^3/s], b_coeff [s / m^2], c_coeff [s^2 / m^5] -> returns [standard SI units]

    Formula:
    s_w = B * Q + C * Q^2

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - b_coeff : Aquifer laminar formation loss coefficient B [unit = s / m^2]
    - c_coeff : Well turbulent screen loss coefficient C [unit = s^2 / m^5]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    b_coeff : FloatOrArray
        Aquifer laminar formation loss coefficient B [s / m^2].
    c_coeff : FloatOrArray
        Well turbulent screen loss coefficient C [s^2 / m^5].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, b, c), is_scalar = coerce_inputs(discharge, b_coeff, c_coeff)
    with np.errstate(all='ignore'):
        sw = b * q + c * q ** 2
    return format_output(sw, is_scalar)

def jacob_well_efficiency(discharge: FloatOrArray, b_coeff: FloatOrArray, c_coeff: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes pumping well efficiency Ew = (B * Q / (B * Q + C * Q^2)) * 100%.
    Units (Default SI): discharge [m^3/s], b_coeff [s / m^2], c_coeff [s^2 / m^5] -> returns [standard SI units]

    Formula:
    Computes pumping well efficiency Ew = (B * Q / (B * Q + C * Q^2)) * 100%.

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - b_coeff : Aquifer laminar formation loss coefficient B [unit = s / m^2]
    - c_coeff : Well turbulent screen loss coefficient C [unit = s^2 / m^5]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    b_coeff : FloatOrArray
        Aquifer laminar formation loss coefficient B [s / m^2].
    c_coeff : FloatOrArray
        Well turbulent screen loss coefficient C [s^2 / m^5].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, b, c), is_scalar = coerce_inputs(discharge, b_coeff, c_coeff)
    with np.errstate(all='ignore'):
        tot = b * q + c * q ** 2
        eff = np.where(tot <= 0, np.nan, b * q / tot * 100.0)
    return format_output(eff, is_scalar)

def jacob_well_b(drawdown: FloatOrArray, discharge: FloatOrArray, c_coeff: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for aquifer laminar loss coefficient B = (s_w - C * Q^2) / Q.
    Units (Default SI): drawdown [m], discharge [m^3/s], c_coeff [s^2 / m^5] -> returns [standard SI units]

    Formula:
    Inversion: Solves for aquifer laminar loss coefficient B = (s_w - C * Q^2) / Q.

    Where (Default SI Units):
    - drawdown : Pumping well water level drawdown s_w [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - c_coeff : Well turbulent screen loss coefficient C [unit = s^2 / m^5]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    drawdown : FloatOrArray
        Pumping well water level drawdown s_w [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    c_coeff : FloatOrArray
        Well turbulent screen loss coefficient C [s^2 / m^5].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (sw, q, c), is_scalar = coerce_inputs(drawdown, discharge, c_coeff)
    with np.errstate(all='ignore'):
        b = np.where(q <= 0, np.nan, (sw - c * q ** 2) / q)
    return format_output(b, is_scalar)

def jacob_well_c(drawdown: FloatOrArray, discharge: FloatOrArray, b_coeff: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Solves for well turbulence loss coefficient C = (s_w - B * Q) / Q^2.
    Units (Default SI): drawdown [m], discharge [m^3/s], b_coeff [s / m^2] -> returns [dimensionless]

    Formula:
    Inversion: Solves for well turbulence loss coefficient C = (s_w - B * Q) / Q^2.

    Where (Default SI Units):
    - drawdown : Pumping well water level drawdown s_w [unit = m]
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - b_coeff : Aquifer laminar formation loss coefficient B [unit = s / m^2]
    - Output : Runoff / discharge coefficient [unit = dimensionless]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    drawdown : FloatOrArray
        Pumping well water level drawdown s_w [m].
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    b_coeff : FloatOrArray
        Aquifer laminar formation loss coefficient B [s / m^2].

    Returns
    -------
    float | np.ndarray
        Runoff / discharge coefficient [dimensionless]. Returns float for scalar inputs.
    """
    (sw, q, b), is_scalar = coerce_inputs(drawdown, discharge, b_coeff)
    with np.errstate(all='ignore'):
        c = np.where(q <= 0, np.nan, (sw - b * q) / q ** 2)
    return format_output(c, is_scalar)

def hantush_leakage_factor(transmissivity: FloatOrArray, aquitard_thickness: FloatOrArray, aquitard_conductivity: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes Hantush-Jacob leakage factor B = sqrt(T * b' / K') [m] for a leaky confined aquifer.
    Units (Default SI): transmissivity [m^2/s], aquitard_thickness [m], aquitard_conductivity [m/s] -> returns [standard SI units]

    Formula:
    Computes Hantush-Jacob leakage factor B = sqrt(T * b' / K') [m] for a leaky confined aquifer.

    Where (Default SI Units):
    - transmissivity : Aquifer transmissivity T [unit = m^2/s]
    - aquitard_thickness : Leaky confining aquitard thickness b' [unit = m]
    - aquitard_conductivity : Aquitard vertical hydraulic conductivity K' [unit = m/s]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    transmissivity : FloatOrArray
        Aquifer transmissivity T [m^2/s].
    aquitard_thickness : FloatOrArray
        Leaky confining aquitard thickness b' [m].
    aquitard_conductivity : FloatOrArray
        Aquitard vertical hydraulic conductivity K' [m/s].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, b_prime, k_prime), is_scalar = coerce_inputs(transmissivity, aquitard_thickness, aquitard_conductivity)
    with np.errstate(all='ignore'):
        b = np.where((t <= 0) | (b_prime <= 0) | (k_prime <= 0), np.nan, np.sqrt(t * b_prime / k_prime))
    return format_output(b, is_scalar)

def specific_capacity_to_transmissivity(discharge: FloatOrArray, drawdown: FloatOrArray, aquifer_type: str='confined') -> Union[float, np.ndarray]:
    """
    Estimates aquifer transmissivity T from well specific capacity (Q / sw) using Thomasson / Driscoll empirical relations:
    Units (Default SI): discharge [m^3/s], drawdown [m], aquifer_type [SI units] -> returns [m^2/s (or m^2/day)]

    Formula:
    specific_capacity_to_transmissivity(discharge, drawdown, aquifer_type)

    Where (Default SI Units):
    - discharge : Volumetric flow rate / discharge Q [unit = m^3/s]
    - drawdown : Pumping well water level drawdown s_w [unit = m]
    - aquifer_type : Input parameter [unit = SI units]
    - Output : Aquifer transmissivity [unit = m^2/s (or m^2/day)]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    discharge : FloatOrArray
        Volumetric flow rate / discharge Q [m^3/s].
    drawdown : FloatOrArray
        Pumping well water level drawdown s_w [m].
    aquifer_type : FloatOrArray
        aquifer_type [SI units].

    Returns
    -------
    float | np.ndarray
        Aquifer transmissivity [m^2/s (or m^2/day)]. Returns float for scalar inputs.
    """
    (q, sw), is_scalar = coerce_inputs(discharge, drawdown)
    k = 1000.0 if 'unconfined' in aquifer_type.lower() else 1500.0
    with np.errstate(all='ignore'):
        t = np.where((q <= 0) | (sw <= 0), np.nan, k * (q / sw))
    return format_output(t, is_scalar)
