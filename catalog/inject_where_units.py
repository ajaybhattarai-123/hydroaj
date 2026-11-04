"""
Comprehensive Unit Injection Script for hydrocivil modules.
Ensures every function provides immediate 'Where (Default SI Units):' details
in VS Code Signature Help and Hover tooltips.
"""

import os
import ast
import re

PARAM_INFO = {
    # Time & Timing
    "rainfall_duration": ("Excess rainfall storm duration D", "hours"),
    "duration": ("Rainfall storm duration t_d", "hours"),
    "lag_time": ("Basin lag time t_L", "hours"),
    "time_to_peak": ("Time to hydrograph peak T_p", "hours"),
    "tp": ("Time to peak / basin lag T_p", "hours"),
    "tc": ("Time of concentration T_c", "minutes"),
    "t_sheet": ("Sheet flow travel time", "minutes"),
    "t_shallow": ("Shallow concentrated flow travel time", "minutes"),
    "t_channel": ("Open channel reach travel time", "minutes"),
    "time": ("Elapsed infiltration or pumping time t", "hours"),
    
    # Geometry & Dimensions
    "length": ("Reach / conduit / flow path length L", "m"),
    "length_km": ("Main channel path length L", "km"),
    "length_to_centroid": ("Channel length to basin centroid L_c", "km"),
    "area": ("Cross-sectional flow area A", "m^2"),
    "area_km2": ("Catchment watershed drainage area A", "km^2"),
    "area_sq_mi": ("Catchment drainage area A", "sq. mi"),
    "drainage_area": ("Catchment drainage area A", "km^2 (or ha for Rational)"),
    "depth": ("Water flow depth y", "m"),
    "depth_1": ("Supercritical initial flow depth y_1", "m"),
    "depth_2": ("Subcritical sequent flow depth y_2", "m"),
    "initial_depth": ("Supercritical initial depth y_1", "m"),
    "sequent_depth": ("Subcritical conjugate depth y_2", "m"),
    "hydraulic_radius": ("Hydraulic radius R_h = A / P", "m"),
    "diameter": ("Internal conduit / pipe diameter D", "m"),
    "bottom_width": ("Channel base width b", "m"),
    "side_slope": ("Side slope ratio m (1V : mH)", "dimensionless"),
    "top_width": ("Channel free-surface top width T", "m"),
    "wetted_perimeter": ("Wetted perimeter P", "m"),
    "head": ("Upstream / operating hydraulic head H", "m"),
    "total_head": ("Total operating head H", "m"),
    "head_loss": ("Energy friction head loss h_f", "m"),
    "hf": ("Frictional head loss h_f", "m"),
    "pier_width": ("Bridge pier frontal width a", "m"),
    "flow_depth": ("Upstream approach flow depth y_1", "m"),
    "scour_depth": ("Maximum local scour depth y_s", "m"),
    "opening": ("Sluice gate vertical opening height w", "m"),
    "width": ("Flume / gate clear opening width b", "m"),
    "base_width": ("Sutro weir rectangular base width b", "m"),
    "base_height": ("Sutro weir base vertical crest height a", "m"),
    "throat_width": ("Venturi / flume constricted throat width b_2", "m"),
    "upstream_depth": ("Upstream approach flow depth y_1", "m"),
    "throat_depth": ("Contracted throat flow depth y_2", "m"),
    
    # Discharge & Velocity
    "discharge": ("Volumetric flow rate / discharge Q", "m^3/s"),
    "discharge_peak": ("Hydrograph peak discharge Q_p", "m^3/s"),
    "velocity": ("Mean cross-sectional flow velocity V", "m/s"),
    "flow_velocity": ("Upstream approach flow velocity V_1", "m/s"),
    "velocity_1": ("Upstream flow velocity V_1", "m/s"),
    "velocity_2": ("Downstream flow velocity V_2", "m/s"),
    "wind_speed_2m": ("Mean daily wind speed at 2 m height u_2", "m/s"),
    
    # Gradients & Slopes
    "slope": ("Longitudinal bed slope / hydraulic gradient S_0", "m/m (decimal)"),
    "slope_m_per_km": ("Main channel gradient S", "m/km"),
    "bed_slope": ("Longitudinal channel bed slope S_0", "m/m"),
    "friction_slope": ("Energy grade line friction slope S_f", "m/m"),
    "hydraulic_gradient": ("Piezometric gradient i = dh / dl", "m/m"),
    
    # Resistance & Coefficients
    "roughness": ("Manning roughness coefficient n", "s/m^(1/3)"),
    "roughness_n": ("Roughness coefficient n", "s/m^(1/3) (or Kerby retardance)"),
    "k_st": ("Strickler roughness coefficient k_st = 1 / n", "m^(1/3)/s"),
    "chezy_c": ("Chézy resistance coefficient C", "m^(1/2)/s"),
    "roughness_c": ("Hazen-Williams roughness coefficient C", "dimensionless (typically 80 - 150)"),
    "friction_factor": ("Darcy-Weisbach friction factor f", "dimensionless"),
    "minor_loss_k": ("Minor form loss coefficient K_L", "dimensionless"),
    "ke": ("Channel expansion loss coefficient K_e", "dimensionless"),
    "kc": ("Channel contraction loss coefficient K_c", "dimensionless"),
    "discharge_coeff": ("Discharge coefficient C_d", "dimensionless"),
    "cd": ("Discharge coefficient C_d", "dimensionless"),
    "c_d": ("Dicken's flood coefficient C_D", "dimensionless (11.4 - 28.0)"),
    "cr": ("Ryves' flood coefficient C_R", "dimensionless (6.8 - 10.2)"),
    "c_r": ("Ryves' flood coefficient C_R", "dimensionless (6.8 - 10.2)"),
    "cn": ("Nawab Jung coefficient C_N", "dimensionless (48.0 - 60.0)"),
    "c_n": ("Nawab Jung coefficient C_N", "dimensionless (48.0 - 60.0)"),
    "cf": ("Fuller's flood coefficient C_F", "dimensionless"),
    "c_f": ("Fuller's flood coefficient C_F", "dimensionless"),
    "c_t": ("Snyder's basin lag coefficient C_t", "dimensionless (1.0 - 2.2)"),
    "ct": ("Snyder's basin lag coefficient C_t", "dimensionless (1.0 - 2.2)"),
    "cp": ("Snyder's peak coefficient C_p", "dimensionless (0.4 - 0.8)"),
    "c_p": ("Snyder's peak coefficient C_p", "dimensionless (0.4 - 0.8)"),
    "cvr_m": ("Kennedy Critical Velocity Ratio m", "dimensionless (0.7 - 1.3)"),
    "silt_factor": ("Lacey's silt factor f", "dimensionless"),
    "d50_mm": ("Median sediment grain size d_50", "mm"),
    "reynolds": ("Reynolds number Re = V * D / nu", "dimensionless"),
    "froude_number": ("Froude number Fr = V / sqrt(g * D_h)", "dimensionless"),
    "froude_1": ("Supercritical inflow Froude number Fr_1", "dimensionless"),
    "k1": ("HEC-18 pier nose shape correction K_1", "dimensionless"),
    "k2": ("HEC-18 flow angle of attack correction K_2", "dimensionless"),
    "k3": ("HEC-18 bed condition correction K_3", "dimensionless"),
    "k4": ("HEC-18 armoring bed sediment correction K_4", "dimensionless"),
    
    # Hydrology Precipitaiton & Infiltration
    "intensity": ("Design rainfall intensity I", "mm/hr"),
    "runoff_coeff": ("Rational runoff coefficient C", "dimensionless (0.05 - 0.95)"),
    "curve_number": ("SCS Runoff Curve Number CN", "dimensionless (30 - 100)"),
    "precipitation": ("Cumulative rainfall storm depth P", "mm"),
    "p2_24hr": ("2-year, 24-hour design storm rainfall depth P_2", "mm"),
    "retention": ("Potential maximum soil retention S", "mm"),
    "initial_capacity": ("Initial Horton infiltration capacity f_0", "mm/hr"),
    "steady_capacity": ("Ultimate steady infiltration capacity f_c", "mm/hr"),
    "decay_constant": ("Horton recession decay constant k", "1/hr"),
    "sorptivity": ("Philip's soil sorptivity parameter S", "mm / hr^0.5"),
    "transmissivity_a": ("Philip's transmissivity factor A", "mm/hr"),
    "a_coeff": ("Kostiakov empirical infiltration coefficient a", "dimensionless or mm/hr^b"),
    "b_exponent": ("Kostiakov infiltration exponent b", "dimensionless (0 < b < 1)"),
    "conductivity_k": ("Saturated hydraulic conductivity K", "mm/hr"),
    "suction_psi": ("Wetting front soil suction head psi", "mm"),
    "moisture_deficit": ("Initial available soil moisture deficit Delta_theta", "dimensionless fraction"),
    "cumulative_f": ("Cumulative infiltrated water volume F", "mm"),
    
    # Evapotranspiration
    "net_radiation": ("Net radiation at the crop surface R_n", "MJ / m^2 / day"),
    "soil_heat_flux": ("Soil heat flux density G", "MJ / m^2 / day"),
    "temp_c": ("Mean daily air temperature at 2 m height T", "deg C"),
    "temp_mean_c": ("Mean air temperature T_mean", "deg C"),
    "temp_max_c": ("Daily maximum air temperature T_max", "deg C"),
    "temp_min_c": ("Daily minimum air temperature T_min", "deg C"),
    "es": ("Mean saturation vapor pressure e_s", "kPa"),
    "ea": ("Actual atmospheric vapor pressure e_a", "kPa"),
    "delta_slope": ("Slope of saturation vapor pressure curve Delta", "kPa / deg C"),
    "psychrometric_gamma": ("Psychrometric constant gamma", "kPa / deg C"),
    "alpha": ("Priestley-Taylor radiation coefficient alpha", "dimensionless (~1.26)"),
    "sunshine_p_percent": ("Percentage of annual daytime hours p", "dimensionless %"),
    "r_a": ("Extraterrestrial radiation R_a", "mm/day equivalent evaporation"),
    "et0": ("Reference evapotranspiration ET_0", "mm/day"),
    
    # Extreme Value & Frequency
    "return_period": ("Design recurrence interval / return period T", "years"),
    "reduced_variate": ("Gumbel EV1 reduced variate y_T", "dimensionless"),
    "mean": ("Sample arithmetic mean of flood series", "m^3/s"),
    "std_dev": ("Sample standard deviation of flood series", "m^3/s"),
    "observed_flood": ("Observed flood discharge magnitude x", "m^3/s"),
    "log_mean": ("Mean of base-10 logarithms of flood peaks", "log10(m^3/s)"),
    "log_std_dev": ("Standard deviation of base-10 logarithms", "log10(m^3/s)"),
    "skewness": ("Station skewness coefficient G", "dimensionless"),
    "rank": ("Statistical order rank m (1 for largest flood)", "integer"),
    "total_samples": ("Total record length / sample size N", "integer count"),
    
    # Groundwater & Wells
    "hydraulic_conductivity": ("Darcy saturated hydraulic conductivity K", "m/s"),
    "transmissivity": ("Aquifer transmissivity T", "m^2/s"),
    "storativity": ("Aquifer storativity / storage coefficient S", "dimensionless"),
    "freshwater_head": ("Freshwater water table elevation above sea level h_f", "m"),
    "interface_depth": ("Depth to freshwater-saltwater interface below sea level z", "m"),
    "rho_f": ("Density of freshwater rho_f", "kg/m^3 (~1000.0)"),
    "rho_s": ("Density of saltwater rho_s", "kg/m^3 (~1025.0)"),
    "b_coeff": ("Aquifer laminar formation loss coefficient B", "s / m^2"),
    "c_coeff": ("Well turbulent screen loss coefficient C", "s^2 / m^5"),
    "drawdown": ("Pumping well water level drawdown s_w", "m"),
    "aquitard_thickness": ("Leaky confining aquitard thickness b'", "m"),
    "aquitard_conductivity": ("Aquitard vertical hydraulic conductivity K'", "m/s"),
    "radius_1": ("Distance to near observation well r_1", "m"),
    "radius_2": ("Distance to far observation well r_2", "m"),
    "r1": ("Distance to observation well 1 (r_1)", "m"),
    "r2": ("Distance to observation well 2 (r_2)", "m"),
    "h1": ("Hydraulic head at well 1 (h_1)", "m"),
    "h2": ("Hydraulic head at well 2 (h_2)", "m"),
    "delta_head": ("Drawdown piezometric head difference (h_2 - h_1)", "m"),
    
    # Pressurized & Fluid Dynamics
    "pressure_abs": ("Absolute static fluid pressure P_abs", "Pa (N/m^2)"),
    "vapor_pressure": ("Water vapor pressure P_v", "Pa (N/m^2)"),
    "density": ("Fluid mass density rho", "kg/m^3 (~1000.0)"),
    "sigma_critical": ("Critical Thoma cavitation index sigma_c", "dimensionless"),
    "power": ("Mechanical / electrical pump power P", "Watts (W)"),
    "efficiency": ("Overall wire-to-water pump efficiency eta", "dimensionless decimal (0 - 1)"),
    
    # Controls
    "system": ("Unit system ('si' for standard metric units, 'us' for US customary units)", "default='si'"),
}


def get_param_entry(pname: str) -> str:
    clean = pname.lower().strip()
    if clean in PARAM_INFO:
        desc, unit = PARAM_INFO[clean]
        return f"        - {pname} : {desc} [{unit}]"
    
    # Heuristics based on name patterns
    if "slope" in clean:
        return f"        - {pname} : Longitudinal bed slope / gradient [{ 'm/km' if 'km' in clean else 'm/m' }]"
    if "tc" in clean or "time" in clean:
        return f"        - {pname} : Time parameter [{ 'minutes' if 'tc' in clean else 'hours' }]"
    if "area" in clean:
        return f"        - {pname} : Area [{ 'km^2' if 'km' in clean else 'm^2' }]"
    if "length" in clean:
        return f"        - {pname} : Length [{ 'km' if 'km' in clean else 'm' }]"
    if "discharge" in clean or clean.startswith("q"):
        return f"        - {pname} : Volumetric discharge rate [m^3/s]"
    if "velocity" in clean or clean.startswith("v"):
        return f"        - {pname} : Flow velocity [m/s]"
    if "depth" in clean or clean.startswith("y"):
        return f"        - {pname} : Flow depth [m]"
    if "head" in clean or clean.startswith("h"):
        return f"        - {pname} : Hydraulic head [m]"
    if "diameter" in clean or clean == "d":
        return f"        - {pname} : Pipe internal diameter [m]"
    
    return f"        - {pname} : Input parameter [{ 'dimensionless' if 'coeff' in clean else 'SI units' }]"


def deduce_output_info(func_name: str) -> str:
    fn = func_name.lower()
    if "tc" in fn or "time_to_peak" in fn or "lag_time" in fn or fn.endswith("_tc") or "travel_time" in fn:
        unit = "hours" if ("time_to_peak" in fn or "lag_time" in fn or "snyder" in fn) else "minutes"
        return f"Time parameter [{unit}]"
    if fn.endswith("_q") or "discharge" in fn or fn.endswith("_peak"):
        return "Volumetric flow discharge [m^3/s]"
    if fn.endswith("_v") or "velocity" in fn:
        return "Flow velocity [m/s]"
    if fn.endswith("_l") or fn.endswith("_length"):
        return "Length [km if 'km' in fn else 'm']"
    if fn.endswith("_a") or fn.endswith("_area"):
        return "Area [km^2 if 'km' in fn else 'm^2']"
    if fn.endswith("_s") or fn.endswith("_slope") or fn.endswith("_s0"):
        return "Longitudinal bed slope [m/m]"
    if fn.endswith("_n") or fn.endswith("_roughness"):
        return "Roughness coefficient [s/m^(1/3) or dimensionless]"
    if fn.endswith("_h") or fn.endswith("_head") or fn.endswith("_hf") or fn.endswith("_depth"):
        return "Hydraulic head / depth [m]"
    if fn.endswith("_d") or fn.endswith("_diameter") or fn.endswith("_d50"):
        return "Diameter [mm if 'd50' in fn else 'm']"
    if fn.endswith("_c") or fn.endswith("_cd") or fn.endswith("_cr") or fn.endswith("_cn") or fn.endswith("_cf"):
        return "Runoff / discharge coefficient [dimensionless]"
    if fn.endswith("_t") or "transmissivity" in fn:
        return "Aquifer transmissivity [m^2/s (or m^2/day)]"
    if "et0" in fn or "evap" in fn:
        return "Reference evapotranspiration [mm/day]"
    if "geom_" in fn:
        return "Geometric properties tuple (Area [m^2], Perimeter [m], Hydraulic Radius [m], Top Width [m], Depth [m])"
    return "Computed numerical result [standard SI units]"


def build_unified_docstring(func_name: str, args: list, old_doc: str) -> str:
    # Extract title
    title = ""
    formula_line = ""
    lines = [l.strip() for l in old_doc.strip().split("\n") if l.strip()]
    if lines:
        title = lines[0]
        for l in lines:
            if ("=" in l or "Formula:" in l) and not l.startswith("Where"):
                clean_l = l.replace("Formula:", "").strip()
                if clean_l and "=" in clean_l:
                    formula_line = clean_l
                    break
    if not title:
        title = f"Calculates {func_name.replace('_', ' ')}."
    if not formula_line:
        formula_line = f"{func_name}({', '.join(args)})"

    where_lines = [get_param_entry(a) for a in args if a != "self"]
    where_block = "\n".join(where_lines)
    out_desc = deduce_output_info(func_name)

    doc = f'''"""
    {title}

    Formula:
        {formula_line}

    Where (Default SI Units):
{where_block}
        - Output : {out_desc}

    Note:
        All calculations strictly default to standard SI metric units unless system='us' is selected.

    Parameters
    ----------'''
    
    # Append parameter types and return type
    param_sections = []
    for a in args:
        if a == "system":
            param_sections.append(f"    {a} : {{'si', 'us'}}, default='si'\n        Unit system to apply ('si' for metric units, 'us' for US customary units).")
        else:
            p_desc, p_unit = PARAM_INFO.get(a.lower(), (a, "SI units"))
            param_sections.append(f"    {a} : FloatOrArray\n        {p_desc} [{p_unit}].")
            
    doc += "\n" + "\n".join(param_sections)
    doc += f'''

    Returns
    -------
    float | np.ndarray
        {out_desc}. Returns float for scalar inputs.
    """'''
    return doc


def update_module(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)

    class DocstringInjector(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            if node.name.startswith("_"):
                return node
                
            args = [a.arg for a in node.args.args]
            existing_doc = ""
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                existing_doc = node.body[0].value.value

            new_doc = build_unified_docstring(node.name, args, existing_doc)
            
            clean_lines = [l.strip() for l in new_doc.replace('"""', '').strip().split("\n")]
            formatted = "\n" + "\n".join("    " + l if l else "" for l in clean_lines) + "\n    "
            
            doc_node = ast.Expr(value=ast.Constant(value=formatted))
            if existing_doc:
                node.body[0] = doc_node
            else:
                node.body.insert(0, doc_node)
            return node

    transformer = DocstringInjector()
    new_tree = transformer.visit(tree)
    ast.fix_missing_locations(new_tree)
    new_src = ast.unparse(new_tree)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_src + "\n")
    print(f"Successfully injected unit documentation: {filepath}")


def main():
    module_dir = os.path.join(os.path.dirname(__file__), "..", "python", "hydrocivil")
    targets = [
        "hydrology.py",
        "hydraulics.py",
        "structures.py",
        "groundwater.py",
        "sediment.py"
    ]
    for t in targets:
        path = os.path.join(module_dir, t)
        if os.path.exists(path):
            update_module(path)


if __name__ == "__main__":
    main()

