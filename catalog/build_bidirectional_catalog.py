#!/usr/bin/env python3
"""
Bidirectional Formula Catalog Generator for Project HydroCivil.
Expands every governing equation family into dedicated explicit forward and inverse
functions according to Approach 1 and the `<base_family>_<symbol>` suffix standard.
"""

import json
import os
import sys

def build_bidirectional_catalog():
    catalog = []

    def add_entry(
        formula_id, function_name, family, domain, subdomain, target_variable,
        governing_equation, inversion_proof, parameters, outputs, guardrails, reference
    ):
        entry = {
            "formula_id": formula_id,
            "function_name": function_name,
            "canonical_name": function_name,
            "family": family,
            "domain": domain,
            "subdomain": subdomain,
            "target_variable": target_variable,
            "governing_equation": governing_equation,
            "solver_type": "explicit",
            "solvers_supported": ["explicit"],
            "mathematical_inversion_proof": inversion_proof,
            "parameters": parameters,
            "outputs": outputs,
            "guardrail_checks": guardrails,
            "literature_reference": reference,
            "literature_source": reference
        }
        catalog.append(entry)

    # =========================================================================
    # PILLAR 1: OPEN CHANNEL HYDRAULICS & SEDIMENTS
    # =========================================================================

    # --- Family: manning ---
    add_entry(
        "HYD_OC_MANNING_Q", "manning_q", "manning", "open_channel", "uniform_flow", "discharge",
        "Q = (k / n) * A * R_h^(2/3) * S_0^(1/2)",
        "Forward Gauckler-Manning-Strickler equation for open channel conveyance.",
        [
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0, "max": None},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.0, "max": 1.0},
            {"name": "roughness", "symbol": "n", "units_si": "s/m^(1/3)", "units_us": "s/ft^(1/3)", "min": 0.001, "max": 0.3}
        ],
        [{"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s"}],
        ["n > 0.0", "A >= 0.0", "R_h >= 0.0", "S_0 >= 0.0"],
        "Chow, V.T. (1959), Open-Channel Hydraulics; Subramanya (2009) 2.txt"
    )

    add_entry(
        "HYD_OC_MANNING_V", "manning_v", "manning", "open_channel", "uniform_flow", "velocity",
        "V = (k / n) * R_h^(2/3) * S_0^(1/2)",
        "Mean flow velocity derived by dividing Manning discharge by cross-sectional area A.",
        [
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.0, "max": 1.0},
            {"name": "roughness", "symbol": "n", "units_si": "s/m^(1/3)", "units_us": "s/ft^(1/3)", "min": 0.001, "max": 0.3}
        ],
        [{"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s"}],
        ["n > 0.0", "R_h >= 0.0", "S_0 >= 0.0"],
        "Chow (1959); French (1985)"
    )

    add_entry(
        "HYD_OC_MANNING_N", "manning_n", "manning", "open_channel", "uniform_flow", "roughness",
        "n = (k / Q) * A * R_h^(2/3) * S_0^(1/2)",
        "Algebraically isolated Manning n: n = (k / Q) * A * R_h^(2/3) * S_0^(1/2) for observed flow calibration.",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0001, "max": None},
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0, "max": None},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.0, "max": 1.0}
        ],
        [{"name": "roughness", "symbol": "n", "units_si": "s/m^(1/3)", "units_us": "s/ft^(1/3)"}],
        ["Q > 0.0", "A >= 0.0", "R_h >= 0.0", "S_0 >= 0.0", "denominator_guard: Q != 0.0"],
        "Chow (1959); Subramanya (2009)"
    )

    add_entry(
        "HYD_OC_MANNING_S0", "manning_s0", "manning", "open_channel", "uniform_flow", "slope",
        "S_0 = ((Q * n) / (k * A * R_h^(2/3)))^2",
        "Inversion solving for longitudinal bed slope: S_0 = ((Q * n) / (k * A * R_h^(2/3)))^2.",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0001, "max": None},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "roughness", "symbol": "n", "units_si": "s/m^(1/3)", "units_us": "s/ft^(1/3)", "min": 0.001, "max": 0.3}
        ],
        [{"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft"}],
        ["A > 0.0", "R_h > 0.0", "n > 0.0", "Q >= 0.0", "denominator_guard: (k * A * R_h^(2/3)) != 0.0"],
        "Chow (1959); USACE HEC-RAS Reference"
    )

    add_entry(
        "HYD_OC_MANNING_A", "manning_a", "manning", "open_channel", "uniform_flow", "area",
        "A = (Q * n) / (k * R_h^(2/3) * S_0^(1/2))",
        "Inversion for required flow area A = (Q * n) / (k * R_h^(2/3) * S_0^(1/2)).",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.00001, "max": 1.0},
            {"name": "roughness", "symbol": "n", "units_si": "s/m^(1/3)", "units_us": "s/ft^(1/3)", "min": 0.001, "max": 0.3}
        ],
        [{"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2"}],
        ["R_h > 0.0", "S_0 > 0.0", "n > 0.0", "denominator_guard: (R_h^(2/3) * S_0^(1/2)) != 0.0"],
        "Chow (1959)"
    )

    add_entry(
        "HYD_OC_MANNING_RH", "manning_rh", "manning", "open_channel", "uniform_flow", "hydraulic_radius",
        "R_h = ((Q * n) / (k * A * S_0^(1/2)))^(3/2)",
        "Inversion for required hydraulic radius R_h = ((Q * n) / (k * A * S_0^(1/2)))^(3/2).",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0001, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.00001, "max": 1.0},
            {"name": "roughness", "symbol": "n", "units_si": "s/m^(1/3)", "units_us": "s/ft^(1/3)", "min": 0.001, "max": 0.3}
        ],
        [{"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft"}],
        ["A > 0.0", "S_0 > 0.0", "n > 0.0", "denominator_guard: (A * S_0^(1/2)) != 0.0"],
        "Chow (1959)"
    )

    # --- Family: strickler ---
    add_entry(
        "HYD_OC_STRICKLER_V", "strickler_v", "strickler", "open_channel", "uniform_flow", "velocity",
        "V = k_st * R_h^(2/3) * S_0^(1/2)",
        "Forward Strickler formula for velocity in alpine and stony channels.",
        [
            {"name": "strickler_k", "symbol": "k_st", "units_si": "m^(1/3)/s", "units_us": "ft^(1/3)/s", "min": 1.0, "max": 150.0},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.0, "max": 1.0}
        ],
        [{"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s"}],
        ["k_st > 0.0", "R_h >= 0.0", "S_0 >= 0.0"],
        "Strickler, A. (1923); Subramanya (2009) 2.txt"
    )

    add_entry(
        "HYD_OC_STRICKLER_KST", "strickler_kst", "strickler", "open_channel", "uniform_flow", "roughness",
        "k_st = V / (R_h^(2/3) * S_0^(1/2))",
        "Inversion for Strickler conveyance factor k_st = V / (R_h^(2/3) * S_0^(1/2)).",
        [
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0, "max": None},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.00001, "max": 1.0}
        ],
        [{"name": "strickler_k", "symbol": "k_st", "units_si": "m^(1/3)/s", "units_us": "ft^(1/3)/s"}],
        ["R_h > 0.0", "S_0 > 0.0", "denominator_guard: (R_h^(2/3) * S_0^(1/2)) != 0.0"],
        "Strickler (1923)"
    )

    add_entry(
        "HYD_OC_STRICKLER_S0", "strickler_s0", "strickler", "open_channel", "uniform_flow", "slope",
        "S_0 = (V / (k_st * R_h^(2/3)))^2",
        "Inversion for bed slope S_0 = (V / (k_st * R_h^(2/3)))^2.",
        [
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0, "max": None},
            {"name": "strickler_k", "symbol": "k_st", "units_si": "m^(1/3)/s", "units_us": "ft^(1/3)/s", "min": 1.0, "max": 150.0},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None}
        ],
        [{"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft"}],
        ["k_st > 0.0", "R_h > 0.0", "denominator_guard: (k_st * R_h^(2/3)) != 0.0"],
        "Strickler (1923)"
    )

    # --- Family: chezy ---
    add_entry(
        "HYD_OC_CHEZY_V", "chezy_v", "chezy", "open_channel", "uniform_flow", "velocity",
        "V = C * sqrt(R_h * S_0)",
        "Forward Chezy formula for open channel uniform flow velocity.",
        [
            {"name": "chezy_c", "symbol": "C", "units_si": "m^(1/2)/s", "units_us": "ft^(1/2)/s", "min": 1.0, "max": 150.0},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.0, "max": 1.0}
        ],
        [{"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s"}],
        ["C > 0.0", "R_h >= 0.0", "S_0 >= 0.0"],
        "Chezy, A. (1775); Chow (1959)"
    )

    add_entry(
        "HYD_OC_CHEZY_C", "chezy_c", "chezy", "open_channel", "uniform_flow", "roughness",
        "C = V / sqrt(R_h * S_0)",
        "Inversion for Chezy resistance coefficient C = V / sqrt(R_h * S_0).",
        [
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0, "max": None},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft", "min": 0.00001, "max": 1.0}
        ],
        [{"name": "chezy_c", "symbol": "C", "units_si": "m^(1/2)/s", "units_us": "ft^(1/2)/s"}],
        ["R_h > 0.0", "S_0 > 0.0", "denominator_guard: (R_h * S_0) != 0.0"],
        "Chezy (1775)"
    )

    add_entry(
        "HYD_OC_CHEZY_S0", "chezy_s0", "chezy", "open_channel", "uniform_flow", "slope",
        "S_0 = V^2 / (C^2 * R_h)",
        "Inversion for bed slope S_0 = V^2 / (C^2 * R_h).",
        [
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0, "max": None},
            {"name": "chezy_c", "symbol": "C", "units_si": "m^(1/2)/s", "units_us": "ft^(1/2)/s", "min": 1.0, "max": 150.0},
            {"name": "hydraulic_radius", "symbol": "R_h", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None}
        ],
        [{"name": "slope", "symbol": "S_0", "units_si": "m/m", "units_us": "ft/ft"}],
        ["C > 0.0", "R_h > 0.0", "denominator_guard: (C^2 * R_h) != 0.0"],
        "Chezy (1775)"
    )

    # --- Family: specific_energy ---
    add_entry(
        "HYD_OC_SPEC_ENERGY_E", "specific_energy_e", "specific_energy", "open_channel", "energy_momentum", "specific_energy",
        "E = y + Q^2 / (2 * g * A^2)",
        "Forward calculation of specific energy head E relative to channel bottom.",
        [
            {"name": "depth", "symbol": "y", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0001, "max": None}
        ],
        [{"name": "specific_energy", "symbol": "E", "units_si": "m", "units_us": "ft"}],
        ["A > 0.0", "y >= 0.0", "g > 0.0"],
        "Bakhmeteff (1932); Chow (1959)"
    )

    add_entry(
        "HYD_OC_SPEC_ENERGY_V", "specific_energy_v", "specific_energy", "open_channel", "energy_momentum", "velocity",
        "V = sqrt(2 * g * (E - y))",
        "Inversion for cross-sectional flow velocity V from specific energy E and flow depth y.",
        [
            {"name": "energy", "symbol": "E", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "depth", "symbol": "y", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None}
        ],
        [{"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s"}],
        ["E >= y", "radicand_guard: (E - y) >= 0.0"],
        "Chow (1959)"
    )

    add_entry(
        "HYD_OC_SPEC_ENERGY_Q", "specific_energy_q", "specific_energy", "open_channel", "energy_momentum", "discharge",
        "Q = A * sqrt(2 * g * (E - y))",
        "Inversion for discharge Q corresponding to specific energy E and flow depth y.",
        [
            {"name": "energy", "symbol": "E", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "depth", "symbol": "y", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0, "max": None}
        ],
        [{"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s"}],
        ["E >= y", "A >= 0.0"],
        "Chow (1959)"
    )

    # --- Family: froude ---
    add_entry(
        "HYD_OC_FROUDE_FR", "froude_fr", "froude", "open_channel", "energy_momentum", "froude_number",
        "Fr = (Q / A) / sqrt(g * (A / T))",
        "Forward dimensionless Froude number Fr representing ratio of inertial to gravitational forces.",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0001, "max": None},
            {"name": "top_width", "symbol": "T", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None}
        ],
        [{"name": "froude_number", "symbol": "Fr", "units_si": "dimensionless", "units_us": "dimensionless"}],
        ["A > 0.0", "T > 0.0", "g > 0.0"],
        "Chow (1959); French (1985)"
    )

    add_entry(
        "HYD_OC_FROUDE_V", "froude_v", "froude", "open_channel", "energy_momentum", "velocity",
        "V = Fr * sqrt(g * D_h)",
        "Inversion for mean velocity corresponding to a specified target Froude number.",
        [
            {"name": "froude", "symbol": "Fr", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.0, "max": None},
            {"name": "hydraulic_depth", "symbol": "D_h", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None}
        ],
        [{"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s"}],
        ["Fr >= 0.0", "D_h >= 0.0"],
        "Chow (1959)"
    )

    # --- Family: hydraulic_jump ---
    add_entry(
        "HYD_OC_JUMP_Y2", "hydraulic_jump_y2", "hydraulic_jump", "open_channel", "hydraulic_jump", "sequent_depth",
        "y_2 = (y_1 / 2) * (sqrt(1 + 8 * Fr_1^2) - 1)",
        "Belanger momentum equation solving for subcritical conjugate sequent depth y_2.",
        [
            {"name": "initial_depth", "symbol": "y_1", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "froude_1", "symbol": "Fr_1", "units_si": "dimensionless", "units_us": "dimensionless", "min": 1.0, "max": 30.0}
        ],
        [{"name": "sequent_depth", "symbol": "y_2", "units_si": "m", "units_us": "ft"}],
        ["y_1 > 0.0", "Fr_1 >= 1.0"],
        "Belanger, J.B. (1828); Chow (1959)"
    )

    add_entry(
        "HYD_OC_JUMP_Y1", "hydraulic_jump_y1", "hydraulic_jump", "open_channel", "hydraulic_jump", "initial_depth",
        "y_1 = (y_2 / 2) * (sqrt(1 + 8 * Fr_2^2) - 1)",
        "Belanger equation solving for supercritical initial depth y_1 from sequent depth and Fr_2.",
        [
            {"name": "sequent_depth", "symbol": "y_2", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "froude_2", "symbol": "Fr_2", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.001, "max": 1.0}
        ],
        [{"name": "initial_depth", "symbol": "y_1", "units_si": "m", "units_us": "ft"}],
        ["y_2 > 0.0", "Fr_2 <= 1.0"],
        "Belanger (1828); Subramanya (2009)"
    )

    add_entry(
        "HYD_OC_JUMP_FR1", "hydraulic_jump_fr1", "hydraulic_jump", "open_channel", "hydraulic_jump", "froude_number",
        "Fr_1 = sqrt(0.125 * ((2 * y_2 / y_1 + 1)^2 - 1))",
        "Inversion solving for inflow Froude number Fr_1 given conjugate depths y_1 and y_2.",
        [
            {"name": "initial_depth", "symbol": "y_1", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "sequent_depth", "symbol": "y_2", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None}
        ],
        [{"name": "froude_1", "symbol": "Fr_1", "units_si": "dimensionless", "units_us": "dimensionless"}],
        ["y_1 > 0.0", "y_2 >= y_1"],
        "Chow (1959)"
    )

    add_entry(
        "HYD_OC_JUMP_DE", "hydraulic_jump_de", "hydraulic_jump", "open_channel", "hydraulic_jump", "energy_loss",
        "Delta_E = (y_2 - y_1)^3 / (4 * y_1 * y_2)",
        "Energy head dissipation across a classical hydraulic jump in a rectangular channel.",
        [
            {"name": "initial_depth", "symbol": "y_1", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "sequent_depth", "symbol": "y_2", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None}
        ],
        [{"name": "head_loss", "symbol": "Delta_E", "units_si": "m", "units_us": "ft"}],
        ["y_1 > 0.0", "y_2 > 0.0", "y_2 >= y_1"],
        "Chow (1959)"
    )

    # =========================================================================
    # PILLAR 2: PRESSURIZED PIPE FLOW, NETWORKS & CULVERTS
    # =========================================================================

    # --- Family: darcy_weisbach ---
    add_entry(
        "HYD_PF_DARCY_HF", "darcy_weisbach_hf", "darcy_weisbach", "pipe_flow", "friction_loss", "head_loss",
        "h_f = f * (L / D) * (V^2 / (2 * g))",
        "Forward Darcy-Weisbach head loss equation.",
        [
            {"name": "friction_factor", "symbol": "f", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.001, "max": 0.2},
            {"name": "length", "symbol": "L", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None},
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0, "max": None}
        ],
        [{"name": "head_loss", "symbol": "h_f", "units_si": "m", "units_us": "ft"}],
        ["f > 0.0", "L >= 0.0", "D > 0.0", "V >= 0.0"],
        "Weisbach (1845); Darcy (1857); Streeter & Wylie (1979)"
    )

    add_entry(
        "HYD_PF_DARCY_F", "darcy_weisbach_f", "darcy_weisbach", "pipe_flow", "friction_loss", "friction_factor",
        "f = h_f * (2 * g * D) / (L * V^2)",
        "Inversion for Darcy friction factor f = h_f * (2 * g * D) / (L * V^2).",
        [
            {"name": "head_loss", "symbol": "h_f", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "length", "symbol": "L", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None},
            {"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None},
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0001, "max": None}
        ],
        [{"name": "friction_factor", "symbol": "f", "units_si": "dimensionless", "units_us": "dimensionless"}],
        ["L > 0.0", "V > 0.0", "D > 0.0", "denominator_guard: (L * V^2) != 0.0"],
        "Streeter & Wylie (1979)"
    )

    add_entry(
        "HYD_PF_DARCY_V", "darcy_weisbach_v", "darcy_weisbach", "pipe_flow", "friction_loss", "velocity",
        "V = sqrt((2 * g * D * h_f) / (f * L))",
        "Inversion for mean pipe flow velocity V = sqrt((2 * g * D * h_f) / (f * L)).",
        [
            {"name": "head_loss", "symbol": "h_f", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "friction_factor", "symbol": "f", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.001, "max": 0.2},
            {"name": "length", "symbol": "L", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None},
            {"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None}
        ],
        [{"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s"}],
        ["f > 0.0", "L > 0.0", "D > 0.0", "h_f >= 0.0", "radicand_guard: (2*g*D*h_f)/(f*L) >= 0.0"],
        "Streeter & Wylie (1979)"
    )

    add_entry(
        "HYD_PF_DARCY_D", "darcy_weisbach_d", "darcy_weisbach", "pipe_flow", "friction_loss", "diameter",
        "D = f * (L / h_f) * (V^2 / (2 * g))",
        "Inversion for required pipe diameter given velocity and head loss: D = f * (L / h_f) * (V^2 / (2 * g)).",
        [
            {"name": "head_loss", "symbol": "h_f", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "friction_factor", "symbol": "f", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.001, "max": 0.2},
            {"name": "length", "symbol": "L", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0, "max": None}
        ],
        [{"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft"}],
        ["h_f > 0.0", "f > 0.0", "denominator_guard: h_f != 0.0"],
        "Streeter & Wylie (1979)"
    )

    add_entry(
        "HYD_PF_DARCY_Q", "darcy_weisbach_q", "darcy_weisbach", "pipe_flow", "friction_loss", "discharge",
        "Q = (pi * D^2 / 4) * sqrt((2 * g * D * h_f) / (f * L))",
        "Inversion solving for pipe volumetric discharge Q under available friction head loss.",
        [
            {"name": "head_loss", "symbol": "h_f", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "friction_factor", "symbol": "f", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.001, "max": 0.2},
            {"name": "length", "symbol": "L", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None},
            {"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None}
        ],
        [{"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s"}],
        ["f > 0.0", "L > 0.0", "D > 0.0", "h_f >= 0.0"],
        "Streeter & Wylie (1979)"
    )

    # --- Family: reynolds ---
    add_entry(
        "HYD_PF_REYNOLDS_RE", "reynolds_re", "reynolds", "pipe_flow", "flow_regime", "reynolds_number",
        "Re = (V * D) / nu",
        "Forward Reynolds number characterizing laminar vs turbulent regime.",
        [
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0, "max": None},
            {"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None},
            {"name": "kinematic_viscosity", "symbol": "nu", "units_si": "m^2/s", "units_us": "ft^2/s", "min": 1e-8, "max": 0.01}
        ],
        [{"name": "reynolds_number", "symbol": "Re", "units_si": "dimensionless", "units_us": "dimensionless"}],
        ["nu > 0.0", "D > 0.0", "V >= 0.0"],
        "Reynolds, O. (1883); Rapp (2022) 1.txt"
    )

    add_entry(
        "HYD_PF_REYNOLDS_V", "reynolds_v", "reynolds", "pipe_flow", "flow_regime", "velocity",
        "V = (Re * nu) / D",
        "Inversion for required flow velocity to achieve target Reynolds number.",
        [
            {"name": "reynolds", "symbol": "Re", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.0, "max": None},
            {"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None},
            {"name": "kinematic_viscosity", "symbol": "nu", "units_si": "m^2/s", "units_us": "ft^2/s", "min": 1e-8, "max": 0.01}
        ],
        [{"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s"}],
        ["D > 0.0", "nu > 0.0", "Re >= 0.0"],
        "Rapp (2022)"
    )

    # --- Family: hazen_williams ---
    add_entry(
        "HYD_PF_HW_HF", "hazen_williams_hf", "hazen_williams", "pipe_flow", "friction_loss", "head_loss",
        "h_f = (k_hw * L * Q^1.852) / (C^1.852 * D^4.87)",
        "Forward Hazen-Williams friction loss equation.",
        [
            {"name": "length", "symbol": "L", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "c_factor", "symbol": "C", "units_si": "dimensionless", "units_us": "dimensionless", "min": 20.0, "max": 180.0},
            {"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None}
        ],
        [{"name": "head_loss", "symbol": "h_f", "units_si": "m", "units_us": "ft"}],
        ["C > 0.0", "D > 0.0", "L >= 0.0", "Q >= 0.0"],
        "Hazen & Williams (1905); Mays (2010)"
    )

    add_entry(
        "HYD_PF_HW_Q", "hazen_williams_q", "hazen_williams", "pipe_flow", "friction_loss", "discharge",
        "Q = ((h_f * C^1.852 * D^4.87) / (k_hw * L))^(1 / 1.852)",
        "Inversion for discharge Q = ((h_f * C^1.852 * D^4.87) / (k_hw * L))^(1 / 1.852).",
        [
            {"name": "head_loss", "symbol": "h_f", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "length", "symbol": "L", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None},
            {"name": "c_factor", "symbol": "C", "units_si": "dimensionless", "units_us": "dimensionless", "min": 20.0, "max": 180.0},
            {"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None}
        ],
        [{"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s"}],
        ["L > 0.0", "C > 0.0", "D > 0.0", "h_f >= 0.0", "denominator_guard: L != 0.0"],
        "Hazen & Williams (1905)"
    )

    add_entry(
        "HYD_PF_HW_D", "hazen_williams_d", "hazen_williams", "pipe_flow", "friction_loss", "diameter",
        "D = ((k_hw * L * Q^1.852) / (h_f * C^1.852))^(1 / 4.87)",
        "Inversion for required pipe diameter D = ((k_hw * L * Q^1.852) / (h_f * C^1.852))^(1 / 4.87).",
        [
            {"name": "head_loss", "symbol": "h_f", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "length", "symbol": "L", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "c_factor", "symbol": "C", "units_si": "dimensionless", "units_us": "dimensionless", "min": 20.0, "max": 180.0}
        ],
        [{"name": "diameter", "symbol": "D", "units_si": "m", "units_us": "ft"}],
        ["h_f > 0.0", "C > 0.0", "denominator_guard: (h_f * C^1.852) != 0.0"],
        "Hazen & Williams (1905)"
    )

    # --- Family: minor_loss ---
    add_entry(
        "HYD_PF_MINOR_HM", "minor_loss_hm", "minor_loss", "pipe_flow", "minor_losses", "head_loss",
        "h_m = K_L * V^2 / (2 * g)",
        "Forward localized minor head loss equation.",
        [
            {"name": "loss_coefficient", "symbol": "K_L", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.0, "max": 100.0},
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0, "max": None}
        ],
        [{"name": "minor_loss", "symbol": "h_m", "units_si": "m", "units_us": "ft"}],
        ["K_L >= 0.0", "V >= 0.0"],
        "Streeter & Wylie (1979)"
    )

    add_entry(
        "HYD_PF_MINOR_KL", "minor_loss_kl", "minor_loss", "pipe_flow", "minor_losses", "loss_coefficient",
        "K_L = 2 * g * h_m / V^2",
        "Inversion for minor loss resistance coefficient K_L = 2 * g * h_m / V^2.",
        [
            {"name": "minor_loss", "symbol": "h_m", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "velocity", "symbol": "V", "units_si": "m/s", "units_us": "ft/s", "min": 0.0001, "max": None}
        ],
        [{"name": "loss_coefficient", "symbol": "K_L", "units_si": "dimensionless", "units_us": "dimensionless"}],
        ["V > 0.0", "h_m >= 0.0", "denominator_guard: V^2 != 0.0"],
        "Streeter & Wylie (1979)"
    )

    # --- Family: water_power ---
    add_entry(
        "HYD_PF_POWER_PW", "water_power_pw", "water_power", "pipe_flow", "pumps", "water_power",
        "P_w = (gamma * Q * H) / k_pow",
        "Forward theoretical hydraulic power.",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "head", "symbol": "H", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "specific_weight", "symbol": "gamma", "units_si": "N/m^3", "units_us": "lbf/ft^3", "min": 1000.0, "max": 20000.0}
        ],
        [{"name": "water_power", "symbol": "P_w", "units_si": "kW", "units_us": "hp"}],
        ["Q >= 0.0", "H >= 0.0", "gamma > 0.0"],
        "Hydraulic Institute Standards"
    )

    add_entry(
        "HYD_PF_POWER_Q", "water_power_q", "water_power", "pipe_flow", "pumps", "discharge",
        "Q = (P_w * k_pow) / (gamma * H)",
        "Inversion for pump flow delivery under available hydraulic power: Q = (P_w * k_pow) / (gamma * H).",
        [
            {"name": "water_power", "symbol": "P_w", "units_si": "kW", "units_us": "hp", "min": 0.0, "max": None},
            {"name": "head", "symbol": "H", "units_si": "m", "units_us": "ft", "min": 0.0001, "max": None},
            {"name": "specific_weight", "symbol": "gamma", "units_si": "N/m^3", "units_us": "lbf/ft^3", "min": 1000.0, "max": 20000.0}
        ],
        [{"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s"}],
        ["H > 0.0", "gamma > 0.0", "denominator_guard: (gamma * H) != 0.0"],
        "Hydraulic Institute Standards"
    )

    # =========================================================================
    # PILLAR 3: SURFACE WATER HYDROLOGY & RUNOFF
    # =========================================================================

    # --- Family: rational ---
    add_entry(
        "HYD_HY_RATIONAL_Q", "rational_q", "rational", "hydrology", "peak_flow", "discharge",
        "Q = k_rat * C * I * A",
        "Forward Rational Method peak discharge equation.",
        [
            {"name": "runoff_coefficient", "symbol": "C", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.01, "max": 1.0},
            {"name": "rainfall_intensity", "symbol": "I", "units_si": "mm/hr", "units_us": "in/hr", "min": 0.0, "max": None},
            {"name": "drainage_area", "symbol": "A", "units_si": "km^2", "units_us": "acres", "min": 0.0, "max": None}
        ],
        [{"name": "peak_discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "cfs"}],
        ["C > 0.0", "I >= 0.0", "A >= 0.0"],
        "Mulvaney (1850); Kuichling (1889); Subramanya (2009)"
    )

    add_entry(
        "HYD_HY_RATIONAL_C", "rational_c", "rational", "hydrology", "peak_flow", "runoff_coefficient",
        "C = Q / (k_rat * I * A)",
        "Inversion for catchment runoff coefficient C = Q / (k_rat * I * A).",
        [
            {"name": "peak_discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "cfs", "min": 0.0, "max": None},
            {"name": "rainfall_intensity", "symbol": "I", "units_si": "mm/hr", "units_us": "in/hr", "min": 0.001, "max": None},
            {"name": "drainage_area", "symbol": "A", "units_si": "km^2", "units_us": "acres", "min": 0.001, "max": None}
        ],
        [{"name": "runoff_coefficient", "symbol": "C", "units_si": "dimensionless", "units_us": "dimensionless"}],
        ["I > 0.0", "A > 0.0", "denominator_guard: (I * A) != 0.0"],
        "Subramanya (2009)"
    )

    add_entry(
        "HYD_HY_RATIONAL_A", "rational_a", "rational", "hydrology", "peak_flow", "drainage_area",
        "A = Q / (k_rat * C * I)",
        "Inversion for maximum allowable watershed drainage area A = Q / (k_rat * C * I).",
        [
            {"name": "peak_discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "cfs", "min": 0.0, "max": None},
            {"name": "runoff_coefficient", "symbol": "C", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.01, "max": 1.0},
            {"name": "rainfall_intensity", "symbol": "I", "units_si": "mm/hr", "units_us": "in/hr", "min": 0.001, "max": None}
        ],
        [{"name": "drainage_area", "symbol": "A", "units_si": "km^2", "units_us": "acres"}],
        ["C > 0.0", "I > 0.0", "denominator_guard: (C * I) != 0.0"],
        "Subramanya (2009)"
    )

    # --- Family: scs_cn ---
    add_entry(
        "HYD_HY_SCS_CN_S", "scs_cn_s", "scs_cn", "hydrology", "runoff", "potential_retention",
        "S = (k_cn1 / CN) - k_cn2",
        "NRCS soil potential maximum retention S from Curve Number CN.",
        [
            {"name": "curve_number", "symbol": "CN", "units_si": "dimensionless", "units_us": "dimensionless", "min": 30.0, "max": 100.0}
        ],
        [{"name": "potential_retention", "symbol": "S", "units_si": "mm", "units_us": "in"}],
        ["CN > 0.0", "CN <= 100.0"],
        "USDA-SCS (1972) NEH-4"
    )

    add_entry(
        "HYD_HY_SCS_CN_CN", "scs_cn_cn", "scs_cn", "hydrology", "runoff", "curve_number",
        "CN = k_cn1 / (S + k_cn2)",
        "Inversion solving for Curve Number CN = k_cn1 / (S + k_cn2) from potential retention S.",
        [
            {"name": "potential_retention", "symbol": "S", "units_si": "mm", "units_us": "in", "min": 0.0, "max": 1000.0}
        ],
        [{"name": "curve_number", "symbol": "CN", "units_si": "dimensionless", "units_us": "dimensionless"}],
        ["S >= 0.0"],
        "USDA-SCS (1972) NEH-4"
    )

    add_entry(
        "HYD_HY_SCS_CN_Q", "scs_cn_q", "scs_cn", "hydrology", "runoff", "runoff_depth",
        "Q = (P - I_a)^2 / (P - I_a + S) for P > I_a, else 0",
        "NRCS direct storm runoff depth calculation with initial abstraction I_a = lambda * S.",
        [
            {"name": "precipitation", "symbol": "P", "units_si": "mm", "units_us": "in", "min": 0.0, "max": None},
            {"name": "potential_retention", "symbol": "S", "units_si": "mm", "units_us": "in", "min": 0.0, "max": None}
        ],
        [{"name": "runoff_depth", "symbol": "Q", "units_si": "mm", "units_us": "in"}],
        ["P >= 0.0", "S >= 0.0"],
        "USDA-SCS (1972) NEH-4; Reddy (2006) 6.txt"
    )

    add_entry(
        "HYD_HY_SCS_CN_P", "scs_cn_p", "scs_cn", "hydrology", "runoff", "precipitation",
        "P = lambda * S + (Q + sqrt(Q^2 + 4 * Q * S)) / 2",
        "Exact analytical algebraic solution of the quadratic SCS equation for required storm precipitation P.",
        [
            {"name": "runoff_depth", "symbol": "Q", "units_si": "mm", "units_us": "in", "min": 0.0, "max": None},
            {"name": "potential_retention", "symbol": "S", "units_si": "mm", "units_us": "in", "min": 0.0, "max": None}
        ],
        [{"name": "precipitation", "symbol": "P", "units_si": "mm", "units_us": "in"}],
        ["Q >= 0.0", "S >= 0.0", "radicand_guard: (Q^2 + 4*Q*S) >= 0.0"],
        "USDA-SCS (1972)"
    )

    # --- Family: horton ---
    add_entry(
        "HYD_HY_HORTON_FP", "horton_rate_fp", "horton", "hydrology", "infiltration", "infiltration_rate",
        "f_p = f_c + (f_0 - f_c) * exp(-k * t)",
        "Forward Horton infiltration rate undergoing exponential decay.",
        [
            {"name": "initial_capacity", "symbol": "f_0", "units_si": "mm/hr", "units_us": "in/hr", "min": 0.0, "max": None},
            {"name": "steady_capacity", "symbol": "f_c", "units_si": "mm/hr", "units_us": "in/hr", "min": 0.0, "max": None},
            {"name": "decay_constant", "symbol": "k", "units_si": "1/hr", "units_us": "1/hr", "min": 0.0, "max": None},
            {"name": "time", "symbol": "t", "units_si": "hr", "units_us": "hr", "min": 0.0, "max": None}
        ],
        [{"name": "infiltration_rate", "symbol": "f_p", "units_si": "mm/hr", "units_us": "in/hr"}],
        ["k >= 0.0", "t >= 0.0", "f_0 >= f_c"],
        "Horton, R.E. (1939); Subramanya (2009)"
    )

    add_entry(
        "HYD_HY_HORTON_K", "horton_rate_k", "horton", "hydrology", "infiltration", "decay_constant",
        "k = -ln((f_p - f_c) / (f_0 - f_c)) / t",
        "Inversion for Horton decay coefficient k from observed infiltrometer capacity readings.",
        [
            {"name": "current_rate", "symbol": "f_p", "units_si": "mm/hr", "units_us": "in/hr", "min": 0.0, "max": None},
            {"name": "initial_capacity", "symbol": "f_0", "units_si": "mm/hr", "units_us": "in/hr", "min": 0.0, "max": None},
            {"name": "steady_capacity", "symbol": "f_c", "units_si": "mm/hr", "units_us": "in/hr", "min": 0.0, "max": None},
            {"name": "time", "symbol": "t", "units_si": "hr", "units_us": "hr", "min": 0.0001, "max": None}
        ],
        [{"name": "decay_constant", "symbol": "k", "units_si": "1/hr", "units_us": "1/hr"}],
        ["t > 0.0", "f_0 > f_c", "(f_p - f_c) > 0.0", "log_guard: (f_p - f_c)/(f_0 - f_c) > 0.0"],
        "Horton (1939)"
    )

    # =========================================================================
    # PILLAR 4: HYDRAULIC STRUCTURES, SPILLWAYS & DAMS
    # =========================================================================

    # --- Family: v_notch_weir ---
    add_entry(
        "HYD_ST_VNOTCH_Q", "v_notch_weir_q", "v_notch_weir", "structures", "weirs", "discharge",
        "Q = (8 / 15) * C_d * sqrt(2 * g) * tan(theta / 2) * H^(5/2)",
        "Forward triangular V-notch weir discharge.",
        [
            {"name": "notch_angle_deg", "symbol": "theta", "units_si": "deg", "units_us": "deg", "min": 10.0, "max": 120.0},
            {"name": "head", "symbol": "H", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "discharge_coeff", "symbol": "C_d", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.5, "max": 0.8}
        ],
        [{"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "cfs"}],
        ["H >= 0.0", "C_d > 0.0", "theta > 0.0"],
        "Shen (1981); USBR (1997)"
    )

    add_entry(
        "HYD_ST_VNOTCH_H", "v_notch_weir_h", "v_notch_weir", "structures", "weirs", "head",
        "H = (Q / ((8 / 15) * C_d * sqrt(2 * g) * tan(theta / 2)))^(2/5)",
        "Inversion for head on V-notch crest H = (Q / ((8/15) * C_d * sqrt(2g) * tan(theta/2)))^(0.4).",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "cfs", "min": 0.0, "max": None},
            {"name": "notch_angle_deg", "symbol": "theta", "units_si": "deg", "units_us": "deg", "min": 10.0, "max": 120.0},
            {"name": "discharge_coeff", "symbol": "C_d", "units_si": "dimensionless", "units_us": "dimensionless", "min": 0.5, "max": 0.8}
        ],
        [{"name": "head", "symbol": "H", "units_si": "m", "units_us": "ft"}],
        ["Q >= 0.0", "C_d > 0.0", "theta > 0.0", "denominator_guard: tan(theta/2) != 0.0"],
        "Shen (1981)"
    )

    # --- Family: ogee_spillway ---
    add_entry(
        "HYD_ST_OGEE_Q", "ogee_spillway_q", "ogee_spillway", "structures", "spillways", "discharge",
        "Q = C_o * L_e * H_e^(3/2)",
        "Forward ogee spillway discharge formula.",
        [
            {"name": "discharge_coeff", "symbol": "C_o", "units_si": "m^(1/2)/s", "units_us": "ft^(1/2)/s", "min": 1.5, "max": 4.5},
            {"name": "effective_length", "symbol": "L_e", "units_si": "m", "units_us": "ft", "min": 0.1, "max": None},
            {"name": "total_head", "symbol": "H_e", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None}
        ],
        [{"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s"}],
        ["C_o > 0.0", "L_e > 0.0", "H_e >= 0.0"],
        "USBR Design of Small Dams (1987)"
    )

    add_entry(
        "HYD_ST_OGEE_HE", "ogee_spillway_he", "ogee_spillway", "structures", "spillways", "total_head",
        "H_e = (Q / (C_o * L_e))^(2/3)",
        "Inversion for operating energy head on ogee crest: H_e = (Q / (C_o * L_e))^(2/3).",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "discharge_coeff", "symbol": "C_o", "units_si": "m^(1/2)/s", "units_us": "ft^(1/2)/s", "min": 1.5, "max": 4.5},
            {"name": "effective_length", "symbol": "L_e", "units_si": "m", "units_us": "ft", "min": 0.1, "max": None}
        ],
        [{"name": "total_head", "symbol": "H_e", "units_si": "m", "units_us": "ft"}],
        ["C_o > 0.0", "L_e > 0.0", "Q >= 0.0", "denominator_guard: (C_o * L_e) != 0.0"],
        "USBR (1987)"
    )

    add_entry(
        "HYD_ST_OGEE_LE", "ogee_spillway_le", "ogee_spillway", "structures", "spillways", "effective_length",
        "L_e = Q / (C_o * H_e^(3/2))",
        "Inversion for required spillway effective crest length L_e = Q / (C_o * H_e^(3/2)).",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0, "max": None},
            {"name": "discharge_coeff", "symbol": "C_o", "units_si": "m^(1/2)/s", "units_us": "ft^(1/2)/s", "min": 1.5, "max": 4.5},
            {"name": "total_head", "symbol": "H_e", "units_si": "m", "units_us": "ft", "min": 0.001, "max": None}
        ],
        [{"name": "effective_length", "symbol": "L_e", "units_si": "m", "units_us": "ft"}],
        ["C_o > 0.0", "H_e > 0.0", "denominator_guard: (C_o * H_e^(3/2)) != 0.0"],
        "USBR (1987)"
    )

    # --- Family: stilling_basin ---
    add_entry(
        "HYD_ST_BASIN_LSB", "stilling_basin_lsb", "stilling_basin", "structures", "energy_dissipation", "basin_length",
        "L_sb = k_basin * y_2",
        "Forward calculation of hydraulic jump stilling basin length.",
        [
            {"name": "sequent_depth", "symbol": "y_2", "units_si": "m", "units_us": "ft", "min": 0.01, "max": None},
            {"name": "basin_coefficient", "symbol": "k_basin", "units_si": "dimensionless", "units_us": "dimensionless", "min": 1.0, "max": 10.0}
        ],
        [{"name": "basin_length", "symbol": "L_sb", "units_si": "m", "units_us": "ft"}],
        ["y_2 > 0.0", "k_basin > 0.0"],
        "USBR Monograph No. 25; Peterka (1984)"
    )

    add_entry(
        "HYD_ST_BASIN_Y2", "stilling_basin_y2", "stilling_basin", "structures", "energy_dissipation", "sequent_depth",
        "y_2 = L_sb / k_basin",
        "Inversion for required incoming sequent depth accommodated by an existing stilling basin.",
        [
            {"name": "basin_length", "symbol": "L_sb", "units_si": "m", "units_us": "ft", "min": 0.1, "max": None},
            {"name": "basin_coefficient", "symbol": "k_basin", "units_si": "dimensionless", "units_us": "dimensionless", "min": 1.0, "max": 10.0}
        ],
        [{"name": "sequent_depth", "symbol": "y_2", "units_si": "m", "units_us": "ft"}],
        ["k_basin > 0.0", "L_sb > 0.0"],
        "Peterka (1984)"
    )

    # =========================================================================
    # PILLAR 5: SEEPAGE & SUBSURFACE GROUNDWATER HYDRAULICS
    # =========================================================================

    # --- Family: darcy_flow ---
    add_entry(
        "HYD_GW_DARCY_Q", "darcy_flow_q", "darcy_flow", "groundwater", "porous_flow", "discharge",
        "Q = -K * A * dh_dl",
        "Forward Darcy 1D discharge through porous media.",
        [
            {"name": "hydraulic_conductivity", "symbol": "K", "units_si": "m/s", "units_us": "ft/s", "min": 1e-12, "max": 1.0},
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0, "max": None},
            {"name": "hydraulic_gradient", "symbol": "dh_dl", "units_si": "m/m", "units_us": "ft/ft", "min": -10.0, "max": 10.0}
        ],
        [{"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s"}],
        ["K > 0.0", "A >= 0.0"],
        "Darcy, H. (1856); Bear, J. (1979)"
    )

    add_entry(
        "HYD_GW_DARCY_K", "darcy_flow_k", "darcy_flow", "groundwater", "porous_flow", "hydraulic_conductivity",
        "K = -Q / (A * dh_dl)",
        "Inversion for aquifer hydraulic conductivity K = -Q / (A * dh_dl).",
        [
            {"name": "discharge", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": -1e6, "max": 1e6},
            {"name": "area", "symbol": "A", "units_si": "m^2", "units_us": "ft^2", "min": 0.0001, "max": None},
            {"name": "hydraulic_gradient", "symbol": "dh_dl", "units_si": "m/m", "units_us": "ft/ft", "min": -10.0, "max": 10.0}
        ],
        [{"name": "hydraulic_conductivity", "symbol": "K", "units_si": "m/s", "units_us": "ft/s"}],
        ["A > 0.0", "dh_dl != 0.0", "denominator_guard: (A * dh_dl) != 0.0"],
        "Darcy (1856)"
    )

    add_entry(
        "HYD_GW_THIEM_Q", "thiem_confined_q", "thiem_confined", "groundwater", "well_hydraulics", "discharge",
        "Q = 2 * pi * T * (h_2 - h_1) / ln(r_2 / r_1)",
        "Forward Thiem equilibrium well discharge in a confined aquifer.",
        [
            {"name": "transmissivity", "symbol": "T", "units_si": "m^2/s", "units_us": "ft^2/s", "min": 1e-6, "max": 1.0},
            {"name": "head_obs_1", "symbol": "h_1", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "head_obs_2", "symbol": "h_2", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "radius_obs_1", "symbol": "r_1", "units_si": "m", "units_us": "ft", "min": 0.01, "max": None},
            {"name": "radius_obs_2", "symbol": "r_2", "units_si": "m", "units_us": "ft", "min": 0.01, "max": None}
        ],
        [{"name": "pumping_rate", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s"}],
        ["T > 0.0", "r_2 > r_1", "r_1 > 0.0", "log_guard: (r_2 / r_1) > 1.0"],
        "Thiem, G. (1906); Todd & Mays (2005)"
    )

    add_entry(
        "HYD_GW_THIEM_T", "thiem_confined_t", "thiem_confined", "groundwater", "well_hydraulics", "transmissivity",
        "T = Q * ln(r_2 / r_1) / (2 * pi * (h_2 - h_1))",
        "Inversion for aquifer transmissivity T = Q * ln(r_2 / r_1) / (2 * pi * (h_2 - h_1)).",
        [
            {"name": "pumping_rate", "symbol": "Q", "units_si": "m^3/s", "units_us": "ft^3/s", "min": 0.0001, "max": None},
            {"name": "head_obs_1", "symbol": "h_1", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "head_obs_2", "symbol": "h_2", "units_si": "m", "units_us": "ft", "min": 0.0, "max": None},
            {"name": "radius_obs_1", "symbol": "r_1", "units_si": "m", "units_us": "ft", "min": 0.01, "max": None},
            {"name": "radius_obs_2", "symbol": "r_2", "units_si": "m", "units_us": "ft", "min": 0.01, "max": None}
        ],
        [{"name": "transmissivity", "symbol": "T", "units_si": "m^2/s", "units_us": "ft^2/s"}],
        ["Q > 0.0", "h_2 > h_1", "r_2 > r_1", "denominator_guard: (h_2 - h_1) != 0.0"],
        "Thiem (1906)"
    )

    return catalog

if __name__ == "__main__":
    cat = build_bidirectional_catalog()
    catalog_path = r"E:\python\Water_Resource_Library\hydrocivil\catalog\formula_catalog.json"
    
    # Merge with existing catalog to ensure complete backward compatibility
    with open(catalog_path, "r", encoding="utf-8") as f:
        existing = json.load(f)
    
    existing_ids = {item["formula_id"] for item in existing}
    merged = list(existing)
    new_added = 0
    for item in cat:
        if item["formula_id"] not in existing_ids:
            merged.append(item)
            existing_ids.add(item["formula_id"])
            new_added += 1
            
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
        
    print(f"Total entries in master catalog: {len(merged)} (Added {new_added} dedicated bidirectional inversions)")

