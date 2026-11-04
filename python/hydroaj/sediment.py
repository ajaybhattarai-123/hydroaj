"""
Sediment Transport & River Mechanics API.
Provides polymorphic scalar and vectorized calculations for bed shear stress,
entrainment criteria, settling velocities, and bedload transport rates.
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
G_SI = 9.80665
G_US = 32.17405

def _get_gravity(system: str) -> float:
    return G_US if system.lower() == 'us' else G_SI

def boundary_shear_stress(unit_weight: FloatOrArray, hydraulic_radius: FloatOrArray, slope: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes boundary shear stress.
    Units (Default SI): unit_weight [SI units], hydraulic_radius [m], slope [m/m (decimal)] -> returns [standard SI units]

    Formula:
    tau_0 = gamma * R_h * S_0

    Where (Default SI Units):
    - unit_weight : Input parameter [unit = SI units]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    unit_weight : FloatOrArray
        unit_weight [SI units].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (gam, rh, s), is_scalar = coerce_inputs(unit_weight, hydraulic_radius, slope)
    out = _core.boundary_shear_stress(gam, rh, s)
    return format_output(out, is_scalar)

def shear_velocity(hydraulic_radius: FloatOrArray, slope: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes shear velocity.
    Units (Default SI): hydraulic_radius [m], slope [m/m (decimal)] -> returns [m/s]

    Formula:
    u_star = sqrt(g * R_h * S_0)

    Where (Default SI Units):
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (rh, s), is_scalar = coerce_inputs(hydraulic_radius, slope)
    g = _get_gravity(system)
    out = _core.shear_velocity(rh, s, g)
    return format_output(out, is_scalar)

def shields_parameter(shear_stress: FloatOrArray, submerged_unit_weight: FloatOrArray, grain_size_d50: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes shields parameter.
    Units (Default SI): shear_stress [SI units], submerged_unit_weight [SI units], grain_size_d50 [SI units] -> returns [standard SI units]

    Formula:
    theta_star = tau_0 / ((gamma_s - gamma) * d_50)

    Where (Default SI Units):
    - shear_stress : Input parameter [unit = SI units]
    - submerged_unit_weight : Input parameter [unit = SI units]
    - grain_size_d50 : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    shear_stress : FloatOrArray
        shear_stress [SI units].
    submerged_unit_weight : FloatOrArray
        submerged_unit_weight [SI units].
    grain_size_d50 : FloatOrArray
        grain_size_d50 [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (tau, dg, d50), is_scalar = coerce_inputs(shear_stress, submerged_unit_weight, grain_size_d50)
    out = _core.shields_parameter(tau, dg, d50)
    return format_output(out, is_scalar)

def critical_shear_stress(critical_shields_param: FloatOrArray, submerged_unit_weight: FloatOrArray, grain_size_d50: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes critical shear stress.
    Units (Default SI): critical_shields_param [SI units], submerged_unit_weight [SI units], grain_size_d50 [SI units] -> returns [standard SI units]

    Formula:
    tau_c = theta_c * (gamma_s - gamma) * d_50

    Where (Default SI Units):
    - critical_shields_param : Input parameter [unit = SI units]
    - submerged_unit_weight : Input parameter [unit = SI units]
    - grain_size_d50 : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    critical_shields_param : FloatOrArray
        critical_shields_param [SI units].
    submerged_unit_weight : FloatOrArray
        submerged_unit_weight [SI units].
    grain_size_d50 : FloatOrArray
        grain_size_d50 [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (tc, dg, d50), is_scalar = coerce_inputs(critical_shields_param, submerged_unit_weight, grain_size_d50)
    out = _core.critical_shear_stress(tc, dg, d50)
    return format_output(out, is_scalar)

def lane_sediment_balance(water_discharge: FloatOrArray, channel_slope: FloatOrArray, grain_size_d50: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes lane sediment balance.
    Units (Default SI): water_discharge [m^3/s], channel_slope [m/m], grain_size_d50 [SI units] -> returns [standard SI units]

    Formula:
    Q_s_ratio = (Q * S) / d_50

    Where (Default SI Units):
    - water_discharge : Volumetric discharge rate [unit = m^3/s]
    - channel_slope : Longitudinal bed slope / gradient [unit = m/m]
    - grain_size_d50 : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    water_discharge : FloatOrArray
        water_discharge [SI units].
    channel_slope : FloatOrArray
        channel_slope [SI units].
    grain_size_d50 : FloatOrArray
        grain_size_d50 [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (q, s, d50), is_scalar = coerce_inputs(water_discharge, channel_slope, grain_size_d50)
    out = _core.lane_sediment_balance(q, s, d50)
    return format_output(out, is_scalar)

def meyer_peter_muller_bedload(shields_parameter: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Computes meyer peter muller bedload.
    Units (Default SI): shields_parameter [SI units] -> returns [standard SI units]

    Formula:
    q_b_star = 8.0 * max(0.0, theta_star - 0.047)^1.5

    Where (Default SI Units):
    - shields_parameter : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    shields_parameter : FloatOrArray
        shields_parameter [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (th,), is_scalar = coerce_inputs(shields_parameter)
    out = _core.meyer_peter_muller_bedload(th)
    return format_output(out, is_scalar)

def rubey_settling_velocity(grain_diameter: FloatOrArray, specific_gravity: FloatOrArray=2.65, kinematic_viscosity: FloatOrArray=1e-06, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes rubey settling velocity.
    Units (Default SI): grain_diameter [m], specific_gravity [SI units], kinematic_viscosity [SI units] -> returns [m/s]

    Formula:
    w_s = sqrt((2/3) * g * (S_s - 1) * d + (36 * nu^2 / d^2)) - (6 * nu / d)

    Where (Default SI Units):
    - grain_diameter : Pipe internal diameter [unit = m]
    - specific_gravity : Input parameter [unit = SI units]
    - kinematic_viscosity : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    grain_diameter : FloatOrArray
        grain_diameter [SI units].
    specific_gravity : FloatOrArray
        specific_gravity [SI units].
    kinematic_viscosity : FloatOrArray
        kinematic_viscosity [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (d, ss, nu), is_scalar = coerce_inputs(grain_diameter, specific_gravity, kinematic_viscosity)
    g = _get_gravity(system)
    out = _core.rubey_settling_velocity(d, ss, nu, g)
    return format_output(out, is_scalar)

def stokes_settling_velocity(grain_diameter: FloatOrArray, specific_gravity: FloatOrArray=2.65, kinematic_viscosity: FloatOrArray=1e-06, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Computes stokes settling velocity.
    Units (Default SI): grain_diameter [m], specific_gravity [SI units], kinematic_viscosity [SI units] -> returns [m/s]

    Formula:
    w_s = (g * (S_s - 1) * d^2) / (18 * nu)

    Where (Default SI Units):
    - grain_diameter : Pipe internal diameter [unit = m]
    - specific_gravity : Input parameter [unit = SI units]
    - kinematic_viscosity : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Flow velocity [unit = m/s]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    grain_diameter : FloatOrArray
        grain_diameter [SI units].
    specific_gravity : FloatOrArray
        specific_gravity [SI units].
    kinematic_viscosity : FloatOrArray
        kinematic_viscosity [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Flow velocity [m/s]. Returns float for scalar inputs.
    """
    (d, ss, nu), is_scalar = coerce_inputs(grain_diameter, specific_gravity, kinematic_viscosity)
    g = _get_gravity(system)
    out = _core.stokes_settling_velocity(d, ss, nu, g)
    return format_output(out, is_scalar)
boundary_shear_tau0 = boundary_shear_stress

def boundary_shear_s0(shear_stress: FloatOrArray, unit_weight: FloatOrArray, hydraulic_radius: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Energy slope S_0 = tau_0 / (gamma * R_h)
    Units (Default SI): shear_stress [SI units], unit_weight [SI units], hydraulic_radius [m] -> returns [m/m]

    Formula:
    Inversion: Energy slope S_0 = tau_0 / (gamma * R_h)

    Where (Default SI Units):
    - shear_stress : Input parameter [unit = SI units]
    - unit_weight : Input parameter [unit = SI units]
    - hydraulic_radius : Hydraulic radius R_h = A / P [unit = m]
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    shear_stress : FloatOrArray
        shear_stress [SI units].
    unit_weight : FloatOrArray
        unit_weight [SI units].
    hydraulic_radius : FloatOrArray
        Hydraulic radius R_h = A / P [m].

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (t, gam, rh), is_scalar = coerce_inputs(shear_stress, unit_weight, hydraulic_radius)
    out = _core.boundary_shear_s0(t, gam, rh)
    return format_output(out, is_scalar)
boundary_shear_slope = boundary_shear_s0

def boundary_shear_rh(shear_stress: FloatOrArray, unit_weight: FloatOrArray, slope: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Hydraulic radius R_h = tau_0 / (gamma * S_0)
    Units (Default SI): shear_stress [SI units], unit_weight [SI units], slope [m/m (decimal)] -> returns [standard SI units]

    Formula:
    Inversion: Hydraulic radius R_h = tau_0 / (gamma * S_0)

    Where (Default SI Units):
    - shear_stress : Input parameter [unit = SI units]
    - unit_weight : Input parameter [unit = SI units]
    - slope : Longitudinal bed slope / hydraulic gradient S_0 [unit = m/m (decimal)]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    shear_stress : FloatOrArray
        shear_stress [SI units].
    unit_weight : FloatOrArray
        unit_weight [SI units].
    slope : FloatOrArray
        Longitudinal bed slope / hydraulic gradient S_0 [m/m (decimal)].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (t, gam, s), is_scalar = coerce_inputs(shear_stress, unit_weight, slope)
    out = _core.boundary_shear_rh(t, gam, s)
    return format_output(out, is_scalar)
boundary_shear_hydraulic_radius = boundary_shear_rh
shields_param_theta = shields_parameter

def shields_param_tau0(shields_param: FloatOrArray, specific_weight_sediment: FloatOrArray, specific_weight_water: FloatOrArray, grain_size_d50: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Bed shear stress tau_0 = theta_* * (gamma_s - gamma_w) * d_50
    Units (Default SI): shields_param [SI units], specific_weight_sediment [SI units], specific_weight_water [SI units], grain_size_d50 [SI units] -> returns [standard SI units]

    Formula:
    Inversion: Bed shear stress tau_0 = theta_* * (gamma_s - gamma_w) * d_50

    Where (Default SI Units):
    - shields_param : Input parameter [unit = SI units]
    - specific_weight_sediment : Input parameter [unit = SI units]
    - specific_weight_water : Input parameter [unit = SI units]
    - grain_size_d50 : Input parameter [unit = SI units]
    - Output : Computed numerical result [unit = standard SI units]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    shields_param : FloatOrArray
        shields_param [SI units].
    specific_weight_sediment : FloatOrArray
        specific_weight_sediment [SI units].
    specific_weight_water : FloatOrArray
        specific_weight_water [SI units].
    grain_size_d50 : FloatOrArray
        grain_size_d50 [SI units].

    Returns
    -------
    float | np.ndarray
        Computed numerical result [standard SI units]. Returns float for scalar inputs.
    """
    (th, gs, gw, d), is_scalar = coerce_inputs(shields_param, specific_weight_sediment, specific_weight_water, grain_size_d50)
    out = _core.shields_param_tau0(th, gs, gw, d)
    return format_output(out, is_scalar)
shields_shear_stress = shields_param_tau0

def shields_param_d50(shields_param: FloatOrArray, shear_stress: FloatOrArray, specific_weight_sediment: FloatOrArray, specific_weight_water: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Median grain size d_50 = tau_0 / (theta_* * (gamma_s - gamma_w))
    Units (Default SI): shields_param [SI units], shear_stress [SI units], specific_weight_sediment [SI units], specific_weight_water [SI units] -> returns [mm if 'd50' in fn else 'm']

    Formula:
    Inversion: Median grain size d_50 = tau_0 / (theta_* * (gamma_s - gamma_w))

    Where (Default SI Units):
    - shields_param : Input parameter [unit = SI units]
    - shear_stress : Input parameter [unit = SI units]
    - specific_weight_sediment : Input parameter [unit = SI units]
    - specific_weight_water : Input parameter [unit = SI units]
    - Output : Diameter [unit = mm if 'd50' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    shields_param : FloatOrArray
        shields_param [SI units].
    shear_stress : FloatOrArray
        shear_stress [SI units].
    specific_weight_sediment : FloatOrArray
        specific_weight_sediment [SI units].
    specific_weight_water : FloatOrArray
        specific_weight_water [SI units].

    Returns
    -------
    float | np.ndarray
        Diameter [mm if 'd50' in fn else 'm']. Returns float for scalar inputs.
    """
    (th, t, gs, gw), is_scalar = coerce_inputs(shields_param, shear_stress, specific_weight_sediment, specific_weight_water)
    out = _core.shields_param_d50(th, t, gs, gw)
    return format_output(out, is_scalar)
shields_grain_size = shields_param_d50
lane_balance_qs = lane_sediment_balance

def lane_balance_s(sediment_discharge: FloatOrArray, grain_size_d50: FloatOrArray, water_discharge: FloatOrArray) -> Union[float, np.ndarray]:
    """
    Inversion: Equilibrium channel slope S = (Q_s * d_50) / Q_w
    Units (Default SI): sediment_discharge [m^3/s], grain_size_d50 [SI units], water_discharge [m^3/s] -> returns [m/m]

    Formula:
    Inversion: Equilibrium channel slope S = (Q_s * d_50) / Q_w

    Where (Default SI Units):
    - sediment_discharge : Volumetric discharge rate [unit = m^3/s]
    - grain_size_d50 : Input parameter [unit = SI units]
    - water_discharge : Volumetric discharge rate [unit = m^3/s]
    - Output : Longitudinal bed slope [unit = m/m]

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    sediment_discharge : FloatOrArray
        sediment_discharge [SI units].
    grain_size_d50 : FloatOrArray
        grain_size_d50 [SI units].
    water_discharge : FloatOrArray
        water_discharge [SI units].

    Returns
    -------
    float | np.ndarray
        Longitudinal bed slope [m/m]. Returns float for scalar inputs.
    """
    (qs, d, qw), is_scalar = coerce_inputs(sediment_discharge, grain_size_d50, water_discharge)
    out = _core.lane_balance_s(qs, d, qw)
    return format_output(out, is_scalar)
lane_balance_slope = lane_balance_s
stokes_settling_ws = stokes_settling_velocity

def stokes_settling_d(settling_velocity: FloatOrArray, specific_gravity: FloatOrArray, kinematic_viscosity: FloatOrArray, system: Literal['si', 'us']='si') -> Union[float, np.ndarray]:
    """
    Inversion: Particle diameter d = sqrt((18 * nu * w_s) / (g * (S_s - 1)))
    Units (Default SI): settling_velocity [m/s], specific_gravity [SI units], kinematic_viscosity [SI units] -> returns [mm if 'd50' in fn else 'm']

    Formula:
    Inversion: Particle diameter d = sqrt((18 * nu * w_s) / (g * (S_s - 1)))

    Where (Default SI Units):
    - settling_velocity : Flow velocity [unit = m/s]
    - specific_gravity : Input parameter [unit = SI units]
    - kinematic_viscosity : Input parameter [unit = SI units]
    - system : Unit system ('si' for standard metric units, 'us' for US customary units) [unit = default='si']
    - Output : Diameter [unit = mm if 'd50' in fn else 'm']

    Note:
    All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------
    settling_velocity : FloatOrArray
        settling_velocity [SI units].
    specific_gravity : FloatOrArray
        specific_gravity [SI units].
    kinematic_viscosity : FloatOrArray
        kinematic_viscosity [SI units].
    system : {'si', 'us'}, default='si'
        Unit system to apply ('si' for metric units, 'us' for US customary units).

    Returns
    -------
    float | np.ndarray
        Diameter [mm if 'd50' in fn else 'm']. Returns float for scalar inputs.
    """
    (ws, ss, nu), is_scalar = coerce_inputs(settling_velocity, specific_gravity, kinematic_viscosity)
    g = _get_gravity(system)
    out = _core.stokes_settling_d(ws, ss, nu, g)
    return format_output(out, is_scalar)
stokes_settling_diameter = stokes_settling_d
