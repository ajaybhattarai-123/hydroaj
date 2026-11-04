#!/usr/bin/env python3
"""
Generates a comprehensive, textbook-grade Microsoft Word (.docx) document containing all 165 formulas
harvested and engineered for Project HydroCivil. Every equation is rendered in native Word
Equation Boxes (OMML oMath / oMathPara) using the official Microsoft MML2OMML.XSL transform with
display="block", producing vertical stacked fractions (numerator over denominator with horizontal bar)
and mathematical typography matching engineering textbooks.
"""

import json
import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml

import lxml.etree as ET
import latex2mathml.converter

# Microsoft Office official XSLT path
XSLT_PATH = r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL"
xslt_doc = ET.parse(XSLT_PATH)
transform_mml_to_omml = ET.XSLT(xslt_doc)

def latex_to_omml(latex_code: str):
    """Converts a LaTeX math string into an lxml OMML element with display='block'."""
    mathml_str = latex2mathml.converter.convert(latex_code, display="block")
    mml_tree = ET.fromstring(mathml_str)
    omml_tree = transform_mml_to_omml(mml_tree)
    omml_xml = ET.tostring(omml_tree, encoding="utf-8").decode("utf-8")
    return parse_xml(omml_xml)

def set_cell_background(cell, hex_color: str):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell internal padding."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table(table, col_widths, headers, data):
    """Populates and styles a clean data table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1F4E79")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=160, right=160)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.name = "Calibri"

    for row_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg_col = "F2F5F8" if row_idx % 2 == 1 else "FFFFFF"
        for i, val in enumerate(row_data):
            row_cells[i].text = str(val if val is not None else "—")
            set_cell_background(row_cells[i], bg_col)
            set_cell_margins(row_cells[i], top=90, bottom=90, left=140, right=140)
            p = row_cells[i].paragraphs[0]
            if i in (1, 2, 3, 4):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.name = "Calibri"

    # Set column widths
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w)


LATEX_MAP = {
    # -------------------------------------------------------------------------
    # Pillar 1: Open Channel Hydraulics & Sediment Mechanics
    # -------------------------------------------------------------------------
    "HYD_OC_MANNING_001": r"Q = \frac{k}{n} A R_h^{2/3} S_0^{1/2}",
    "HYD_OC_MANNING_002": r"V = \frac{k}{n} R_h^{2/3} S_0^{1/2}",
    "HYD_OC_STRICKLER_001": r"V = k_{st} R_h^{2/3} S_0^{1/2}",
    "HYD_OC_CHEZY_001": r"V = C \sqrt{R_h S_0}",
    "HYD_OC_KUTTER_001": r"C = \frac{23 + \frac{0.00155}{S_0} + \frac{1}{n}}{1 + \left(23 + \frac{0.00155}{S_0}\right) \frac{n}{\sqrt{R_h}}}",
    "HYD_OC_BAZIN_001": r"C = \frac{87}{1 + \frac{\gamma}{\sqrt{R_h}}}",
    "HYD_OC_GEOM_RECT_001": [
        r"A = b \cdot y",
        r"P = b + 2y",
        r"R_h = \frac{A}{P} = \frac{b \cdot y}{b + 2y}",
        r"T = b",
        r"D_h = \frac{A}{T} = y",
        r"\bar{y} = \frac{y}{2}"
    ],
    "HYD_OC_GEOM_TRAP_001": [
        r"A = (b + m y) y",
        r"P = b + 2 y \sqrt{1 + m^2}",
        r"R_h = \frac{A}{P}",
        r"T = b + 2 m y",
        r"D_h = \frac{A}{T}",
        r"\bar{y} = \frac{y(2b + m y)}{3(b + m y)}"
    ],
    "HYD_OC_GEOM_TRI_001": [
        r"A = m y^2",
        r"P = 2 y \sqrt{1 + m^2}",
        r"R_h = \frac{A}{P}",
        r"T = 2 m y",
        r"D_h = \frac{y}{2}",
        r"\bar{y} = \frac{y}{3}"
    ],
    "HYD_OC_GEOM_CIRC_001": [
        r"\theta = 2 \arccos\left(1 - \frac{2y}{D}\right)",
        r"A = \frac{D^2}{8} (\theta - \sin\theta)",
        r"P = \frac{D \theta}{2}",
        r"R_h = \frac{A}{P}",
        r"T = D \sin\left(\frac{\theta}{2}\right)",
        r"D_h = \frac{A}{T}"
    ],
    "HYD_OC_GEOM_PARA_001": [
        r"A = \frac{2}{3} T y",
        r"P \approx T + \frac{8 y^2}{3 T}",
        r"R_h = \frac{A}{P}",
        r"D_h = \frac{2}{3} y",
        r"\bar{y} = \frac{2}{5} y"
    ],
    "HYD_OC_SPEC_ENERGY_001": r"E = y + \frac{Q^2}{2 g A^2} = y + \frac{V^2}{2 g}",
    "HYD_OC_FROUDE_001": r"Fr = \frac{V}{\sqrt{g D_h}} = \frac{Q / A}{\sqrt{g (A / T)}}",
    "HYD_OC_SPEC_FORCE_001": r"M = \frac{Q^2}{g A} + \bar{y} A",
    "HYD_OC_CRIT_DEPTH_RECT_001": r"y_c = \sqrt[3]{\frac{q^2}{g}} = \sqrt[3]{\frac{(Q/b)^2}{g}}",
    "HYD_OC_BELANGER_001": r"y_2 = \frac{y_1}{2} \left(\sqrt{1 + 8 Fr_1^2} - 1\right)",
    "HYD_OC_JUMP_LOSS_001": r"\Delta E = E_1 - E_2 = \frac{(y_2 - y_1)^3}{4 y_1 y_2}",
    "HYD_OC_JUMP_LENGTH_001": r"L_j \approx 6.0 (y_2 - y_1)",
    "HYD_OC_GVF_DYNAMIC_001": r"\frac{dy}{dx} = \frac{S_0 - S_f}{1 - Fr^2}",
    "HYD_OC_FRICTION_SLOPE_001": r"S_f = \frac{n^2 Q^2}{k^2 A^2 R_h^{4/3}}",
    "HYD_OC_DIRECT_STEP_001": r"\Delta x = \frac{E_2 - E_1}{S_0 - \frac{1}{2}(S_{f1} + S_{f2})}",
    "HYD_OC_OPT_RECT_001": [
        r"b = 2 y",
        r"R_h = \frac{y}{2}",
        r"A = 2 y^2",
        r"P = 4 y"
    ],
    "HYD_OC_OPT_TRAP_001": [
        r"m = \frac{1}{\sqrt{3}}",
        r"b = \frac{2}{\sqrt{3}} y",
        r"R_h = \frac{y}{2}",
        r"A = \sqrt{3} y^2"
    ],
    "HYD_OC_OPT_TRI_001": [
        r"m = 1.0",
        r"R_h = \frac{y}{2 \sqrt{2}}",
        r"A = y^2",
        r"P = 2 \sqrt{2} y"
    ],
    "HYD_OC_CRIT_VEL_001": r"V_c = \sqrt{g D_h} = \sqrt{g \frac{A}{T}}",
    "HYD_OC_CRIT_SLOPE_001": r"S_c = \frac{g n^2}{k^2 R_{hc}^{4/3}}",
    "HYD_OC_WAVE_CELERITY_001": r"c = \sqrt{g D_h} = \sqrt{g \frac{A}{T}}",
    "HYD_OC_JUMP_EFF_001": r"\frac{E_2}{E_1} = \frac{(1 + 8 Fr_1^2)^{3/2} - 4 Fr_1^2 + 1}{8 Fr_1^2 (2 + Fr_1^2)}",
    "HYD_OC_JUMP_HEIGHT_001": r"h_j = y_2 - y_1",
    "HYD_OC_CRIT_DEPTH_TRI_001": r"y_c = \left(\frac{2 Q^2}{g m^2}\right)^{1/5}",
    "HYD_OC_COMP_N_HORTON_001": r"\bar{n} = \left(\frac{\sum_{i=1}^N P_i n_i^{3/2}}{\sum_{i=1}^N P_i}\right)^{2/3}",
    "HYD_OC_COMP_N_PAVLOVSKII_001": r"\bar{n} = \sqrt{\frac{\sum_{i=1}^N P_i n_i^2}{\sum_{i=1}^N P_i}}",
    "HYD_SED_SHEAR_STRESS_001": r"\tau_0 = \gamma R_h S_0",
    "HYD_SED_SHEAR_VEL_001": r"u_* = \sqrt{\frac{\tau_0}{\rho}} = \sqrt{g R_h S_0}",
    "HYD_SED_SHIELDS_PARAM_001": r"\theta_* = \frac{\tau_0}{(\gamma_s - \gamma) d_{50}}",
    "HYD_SED_CRIT_SHEAR_001": r"\tau_c = \theta_c (\gamma_s - \gamma) d_{50}",
    "HYD_SED_LANE_BALANCE_001": r"\text{Balance Ratio} = \frac{Q S}{d_{50}}",
    "HYD_SED_MPM_BEDLOAD_001": r"q_b^* = 8.0 \cdot \max(0, \theta_* - 0.047)^{3/2}",
    "HYD_SED_RUBEY_SETTLING_001": r"w_s = \sqrt{\frac{2}{3} g (S_s - 1) d + \frac{36 \nu^2}{d^2}} - \frac{6 \nu}{d}",
    "HYD_SED_STOKES_SETTLING_001": r"w_s = \frac{g (S_s - 1) d^2}{18 \nu}",

    # Open Channel Dedicated Inversions
    "HYD_OC_MANNING_Q": r"Q = \frac{k}{n} A R_h^{2/3} S_0^{1/2}",
    "HYD_OC_MANNING_V": r"V = \frac{k}{n} R_h^{2/3} S_0^{1/2}",
    "HYD_OC_MANNING_N": r"n = \frac{k}{Q} A R_h^{2/3} S_0^{1/2}",
    "HYD_OC_MANNING_S0": r"S_0 = \left( \frac{Q n}{k A R_h^{2/3}} \right)^2",
    "HYD_OC_MANNING_A": r"A = \frac{Q n}{k R_h^{2/3} S_0^{1/2}}",
    "HYD_OC_MANNING_RH": r"R_h = \left( \frac{Q n}{k A S_0^{1/2}} \right)^{3/2}",
    "HYD_OC_STRICKLER_V": r"V = k_{st} R_h^{2/3} S_0^{1/2}",
    "HYD_OC_STRICKLER_KST": r"k_{st} = \frac{V}{R_h^{2/3} S_0^{1/2}}",
    "HYD_OC_STRICKLER_S0": r"S_0 = \left( \frac{V}{k_{st} R_h^{2/3}} \right)^2",
    "HYD_OC_CHEZY_V": r"V = C \sqrt{R_h S_0}",
    "HYD_OC_CHEZY_C": r"C = \frac{V}{\sqrt{R_h S_0}}",
    "HYD_OC_CHEZY_S0": r"S_0 = \frac{V^2}{C^2 R_h}",
    "HYD_OC_SPEC_ENERGY_E": r"E = y + \frac{Q^2}{2 g A^2} = y + \frac{V^2}{2 g}",
    "HYD_OC_SPEC_ENERGY_V": r"V = \sqrt{2 g (E - y)}",
    "HYD_OC_SPEC_ENERGY_Q": r"Q = A \sqrt{2 g (E - y)}",
    "HYD_OC_FROUDE_FR": r"Fr = \frac{V}{\sqrt{g D_h}}",
    "HYD_OC_FROUDE_V": r"V = Fr \sqrt{g D_h}",
    "HYD_OC_JUMP_Y2": r"y_2 = \frac{y_1}{2} \left(\sqrt{1 + 8 Fr_1^2} - 1\right)",
    "HYD_OC_JUMP_Y1": r"y_1 = \frac{y_2}{2} \left(\sqrt{1 + 8 Fr_2^2} - 1\right)",
    "HYD_OC_JUMP_FR1": r"Fr_1 = \sqrt{\frac{1}{8} \left[ \left(\frac{2 y_2}{y_1} + 1\right)^2 - 1 \right]}",
    "HYD_OC_JUMP_DE": r"\Delta E = \frac{(y_2 - y_1)^3}{4 y_1 y_2}",

    # -------------------------------------------------------------------------
    # Pillar 2: Pressurized Pipe Flow, Networks & Culverts
    # -------------------------------------------------------------------------
    "HYD_PF_DARCY_WEISBACH_001": r"h_f = f \frac{L}{D} \frac{V^2}{2g}",
    "HYD_PF_REYNOLDS_001": r"Re = \frac{V D}{\nu} = \frac{\rho V D}{\mu}",
    "HYD_PF_LAMINAR_F_001": r"f = \frac{64}{Re}",
    "HYD_PF_COLEBROOK_001": r"\frac{1}{\sqrt{f}} = -2.0 \log_{10}\left(\frac{\epsilon / D}{3.7} + \frac{2.51}{Re \sqrt{f}}\right)",
    "HYD_PF_SWAMEE_JAIN_001": r"f = \frac{0.25}{\left[\log_{10}\left(\frac{\epsilon / D}{3.7} + \frac{5.74}{Re^{0.9}}\right)\right]^2}",
    "HYD_PF_HAALAND_001": r"\frac{1}{\sqrt{f}} = -1.8 \log_{10}\left[\left(\frac{\epsilon / D}{3.7}\right)^{1.11} + \frac{6.9}{Re}\right]",
    "HYD_PF_CHURCHILL_001": [
        r"f = 8 \left[ \left(\frac{8}{Re}\right)^{12} + (A + B)^{-1.5} \right]^{1/12}",
        r"A = \left[ -2.457 \ln\left( \left(\frac{7}{Re}\right)^{0.9} + 0.27 \frac{\epsilon}{D} \right) \right]^{16}",
        r"B = \left( \frac{37530}{Re} \right)^{16}"
    ],
    "HYD_PF_WOOD_001": [
        r"f = a + b \cdot Re^{-c}",
        r"a = 0.094 \left(\frac{\epsilon}{D}\right)^{0.225} + 0.53 \frac{\epsilon}{D}",
        r"b = 88 \left(\frac{\epsilon}{D}\right)^{0.44}",
        r"c = 1.62 \left(\frac{\epsilon}{D}\right)^{0.134}"
    ],
    "HYD_PF_HAZEN_WILLIAMS_001": r"h_f = \frac{k_{hw} L Q^{1.852}}{C^{1.852} D^{4.87}}",
    "HYD_PF_HAZEN_WILLIAMS_VEL_001": r"V = k_v C R_h^{0.63} S^{0.54}",
    "HYD_PF_MINOR_LOSS_001": r"h_m = K_L \frac{V^2}{2g}",
    "HYD_PF_WAVE_CELERITY_001": r"a = \sqrt{\frac{K / \rho}{1 + \left(\frac{K}{E}\right)\left(\frac{D}{e}\right)}}",
    "HYD_PF_JOUKOWSKY_001": [
        r"\Delta H = \frac{a \Delta V}{g}",
        r"\Delta P = \rho a \Delta V"
    ],
    "HYD_PF_CRIT_CLOSURE_001": r"T_c = \frac{2L}{a}",
    "HYD_PF_CULVERT_INLET_UNSUB_001": r"\frac{HW_i}{D} = \frac{H_c}{D} + K \left(\frac{Q}{A \sqrt{D}}\right)^M - 0.5 S",
    "HYD_PF_CULVERT_INLET_SUB_001": r"\frac{HW_i}{D} = c \left(\frac{Q}{A \sqrt{D}}\right)^2 + Y - 0.5 S",
    "HYD_PF_CULVERT_OUTLET_001": [
        r"HW_o = h_o + H - L S_0",
        r"H = \left( 1 + K_e + \frac{29 n^2 L}{R_h^{4/3}} \right) \frac{V^2}{2g}"
    ],
    "HYD_PF_CULVERT_ENTRANCE_001": r"h_e = K_e \frac{V^2}{2g}",
    "HYD_PF_HARDY_CROSS_001": r"\Delta Q = -\frac{\sum r Q |Q|^{n - 1}}{n \sum r |Q|^{n - 1}}",
    "HYD_PF_EQUIV_LENGTH_001": r"L_e = \frac{K_L D}{f}",
    "HYD_PF_SERIES_DIAMETER_001": r"D_e = \left( \frac{L_{total}}{\sum_{i=1}^N \frac{L_i}{D_i^5}} \right)^{1/5}",
    "HYD_PF_PARALLEL_FLOW_001": r"Q_i = Q_{total} \frac{\sqrt{D_i^5 / L_i}}{\sum_{j=1}^M \sqrt{D_j^5 / L_j}}",
    "HYD_PF_WATER_POWER_001": [
        r"P_w = \frac{\rho g Q H}{1000} \quad \text{(kW, SI)}",
        r"P_w = \frac{\gamma Q H}{550} \quad \text{(hp, US)}"
    ],
    "HYD_PF_BRAKE_POWER_001": r"P_b = \frac{P_w}{\eta}",

    # Pipe Flow Dedicated Inversions
    "HYD_PF_DARCY_HF": r"h_f = f \frac{L}{D} \frac{V^2}{2g}",
    "HYD_PF_DARCY_F": r"f = \frac{2 g D h_f}{L V^2}",
    "HYD_PF_DARCY_V": r"V = \sqrt{\frac{2 g D h_f}{f L}}",
    "HYD_PF_DARCY_D": r"D = \frac{f L V^2}{2 g h_f}",
    "HYD_PF_DARCY_Q": r"Q = \frac{\pi D^2}{4} \sqrt{\frac{2 g D h_f}{f L}}",
    "HYD_PF_REYNOLDS_RE": r"Re = \frac{V D}{\nu}",
    "HYD_PF_REYNOLDS_V": r"V = \frac{Re \cdot \nu}{D}",
    "HYD_PF_HW_HF": r"h_f = \frac{k_{hw} L Q^{1.852}}{C^{1.852} D^{4.87}}",
    "HYD_PF_HW_Q": r"Q = \left( \frac{h_f C^{1.852} D^{4.87}}{k_{hw} L} \right)^{\frac{1}{1.852}}",
    "HYD_PF_HW_D": r"D = \left( \frac{k_{hw} L Q^{1.852}}{h_f C^{1.852}} \right)^{\frac{1}{4.87}}",
    "HYD_PF_MINOR_HM": r"h_m = K_L \frac{V^2}{2g}",
    "HYD_PF_MINOR_KL": r"K_L = \frac{2 g h_m}{V^2}",
    "HYD_PF_POWER_PW": r"P_w = \frac{\gamma Q H}{k_{pow}}",
    "HYD_PF_POWER_Q": r"Q = \frac{P_w k_{pow}}{\gamma H}",

    # -------------------------------------------------------------------------
    # Pillar 3: Surface Water Hydrology & Watershed Modeling
    # -------------------------------------------------------------------------
    "HYD_HY_IDF_SHERMAN_001": r"i = \frac{a}{(t_d + b)^c}",
    "HYD_HY_THIESSEN_001": r"\bar{P} = \frac{\sum_{i=1}^N A_i P_i}{\sum_{i=1}^N A_i}",
    "HYD_HY_HORTON_INF_001": r"f_p(t) = f_c + (f_0 - f_c) e^{-k t}",
    "HYD_HY_HORTON_CUM_001": r"F(t) = f_c t + \frac{f_0 - f_c}{k} (1 - e^{-k t})",
    "HYD_HY_GREEN_AMPT_001": r"f(t) = K_s \left(1 + \frac{\psi \cdot \Delta\theta}{F}\right)",
    "HYD_HY_SCS_CN_STORAGE_001": [
        r"S = \frac{25400}{CN} - 254 \quad \text{(SI, mm)}",
        r"S = \frac{1000}{CN} - 10 \quad \text{(US, in)}"
    ],
    "HYD_HY_SCS_CN_RUNOFF_001": r"Q = \frac{(P - I_a)^2}{P - I_a + S} \quad \text{for } P > I_a, \quad I_a = 0.2 S",
    "HYD_HY_RATIONAL_001": [
        r"Q = 0.2778 \cdot C \cdot I \cdot A \quad \text{(SI, } \text{m}^3/\text{s)}",
        r"Q = C \cdot I \cdot A \quad \text{(US, cfs)}"
    ],
    "HYD_HY_KIRPICH_001": [
        r"t_c = 0.01947 \cdot L^{0.77} S^{-0.385} \quad \text{(SI, min)}",
        r"t_c = 0.0078 \cdot L^{0.77} S^{-0.385} \quad \text{(US, min)}"
    ],
    "HYD_HY_SNYDER_001": [
        r"t_p = C_t (L \cdot L_c)^{0.3}",
        r"q_p = \frac{C_p}{t_p}",
        r"Q_p = q_p A"
    ],
    "HYD_HY_SCS_DIM_UH_001": [
        r"q_p = \frac{0.208 A}{t_p} \quad \text{(SI, } \text{m}^3/\text{s)}",
        r"q_p = \frac{484 A}{t_p} \quad \text{(US, cfs)}"
    ],
    "HYD_HY_MUSKINGUM_001": [
        r"C_0 = \frac{\Delta t - 2 K X}{2 K (1 - X) + \Delta t}",
        r"C_1 = \frac{\Delta t + 2 K X}{2 K (1 - X) + \Delta t}",
        r"C_2 = \frac{2 K (1 - X) - \Delta t}{2 K (1 - X) + \Delta t}"
    ],
    "HYD_HY_MUSKINGUM_ROUTING_001": r"Q_{j+1} = C_0 I_{j+1} + C_1 I_j + C_2 Q_j",
    "HYD_HY_COMPOSITE_CN_001": r"\bar{CN} = \frac{\sum_{i=1}^M A_i CN_i}{\sum_{i=1}^M A_i}",
    "HYD_HY_SCS_AMC_I_001": r"CN_I = \frac{4.2 CN_{II}}{10 - 0.058 CN_{II}}",
    "HYD_HY_SCS_AMC_III_001": r"CN_{III} = \frac{23 CN_{II}}{10 + 0.13 CN_{II}}",
    "HYD_HY_TR55_SHEET_FLOW_001": r"T_t = \frac{0.007 (n L)^{0.8}}{P_2^{0.5} s^{0.4}}",
    "HYD_HY_TR55_SHALLOW_VEL_001": r"V = k_{surface} \sqrt{s}",
    "HYD_HY_GUMBEL_FLOOD_001": [
        r"X_T = \bar{X} + K_T \sigma_X",
        r"K_T = -\frac{\sqrt{6}}{\pi} \left[ 0.5772 + \ln\left( \ln\left(\frac{T}{T - 1}\right) \right) \right]"
    ],
    "HYD_HY_NASH_CASCADE_001": r"u(t) = \frac{1}{K \Gamma(n)} \left(\frac{t}{K}\right)^{n - 1} e^{-t / K}",
    "HYD_HY_HARGREAVES_ET0_001": r"ET_0 = 0.0023 R_a (\bar{T} + 17.8) \sqrt{T_{max} - T_{min}}",
    "HYD_HY_PENMAN_RAD_001": r"R_{n,mm} = \frac{R_n \cdot 10^6}{\rho_w \lambda_v}",
    "HYD_HY_TIME_AREA_RUNOFF_001": r"Q_j = k_{unit} \sum_{k=1}^j I_{j - k + 1} A_k",

    # Hydrology Dedicated Inversions
    "HYD_HY_RATIONAL_Q": r"Q = k_{rat} \cdot C \cdot I \cdot A",
    "HYD_HY_RATIONAL_C": r"C = \frac{Q}{k_{rat} \cdot I \cdot A}",
    "HYD_HY_RATIONAL_A": r"A = \frac{Q}{k_{rat} \cdot C \cdot I}",
    "HYD_HY_SCS_CN_S": r"S = \frac{k_{cn1}}{CN} - k_{cn2}",
    "HYD_HY_SCS_CN_CN": r"CN = \frac{k_{cn1}}{S + k_{cn2}}",
    "HYD_HY_SCS_CN_Q": r"Q = \frac{(P - I_a)^2}{P - I_a + S} \quad \text{for } P > I_a, \quad I_a = \lambda S",
    "HYD_HY_SCS_CN_P": r"P = \lambda S + \frac{Q + \sqrt{Q^2 + 4 Q S}}{2}",
    "HYD_HY_HORTON_FP": r"f_p = f_c + (f_0 - f_c) e^{-k t}",
    "HYD_HY_HORTON_K": r"k = -\frac{1}{t} \ln\left( \frac{f_p - f_c}{f_0 - f_c} \right)",

    # -------------------------------------------------------------------------
    # Pillar 4: Hydraulic Structures, Spillways & Dams
    # -------------------------------------------------------------------------
    "HYD_ST_RECT_WEIR_001": [
        r"Q = 1.84 (L - 0.1 n_e H) H^{3/2} \quad \text{(SI)}",
        r"Q = 3.33 (L - 0.1 n_e H) H^{3/2} \quad \text{(US)}"
    ],
    "HYD_ST_VNOTCH_WEIR_001": r"Q = \frac{8}{15} C_d \sqrt{2g} \tan\left(\frac{\theta}{2}\right) H^{5/2}",
    "HYD_ST_BROAD_WEIR_001": r"Q = C_d \left(\frac{2}{3}\right)^{3/2} \sqrt{g} L H^{3/2}",
    "HYD_ST_PARSHALL_001": r"Q = C W H^n",
    "HYD_ST_ORIFICE_FREE_001": r"Q = C_d A_o \sqrt{2gH}",
    "HYD_ST_ORIFICE_SUB_001": r"Q = C_d A_o \sqrt{2g (H_1 - H_2)}",
    "HYD_ST_SLUICE_FREE_001": r"Q = C_d b a \sqrt{2g y_1}",
    "HYD_ST_SLUICE_SUB_001": r"Q = C_s b a \sqrt{2g (y_1 - y_2)}",
    "HYD_ST_OGEE_SPILLWAY_001": r"Q = C_o L_e H_e^{3/2}",
    "HYD_ST_OGEE_COEFF_001": r"C = C_o \left(\frac{H_e}{H_o}\right)^{0.12}",
    "HYD_ST_EFF_CREST_LEN_001": r"L_e = L - 2 (N K_p + K_a) H_e",
    "HYD_ST_CHUTE_VELOCITY_001": r"V = \sqrt{2g (Z_{drop} - H_{loss})}",
    "HYD_ST_STILLING_BASIN_001": r"L_{sb} = k_{basin} y_2",
    "HYD_ST_MORNING_GLORY_001": r"Q = C (2 \pi R) H^{3/2}",
    "HYD_ST_SIPHON_SPILLWAY_001": r"Q = C_d A_{throat} \sqrt{2g H_{operating}}",
    "HYD_ST_DROP_STRUCT_001": r"y_1 = 0.54 h_d \left( \frac{q^2}{g h_d^3} \right)^{0.425}",
    "HYD_ST_TAILWATER_001": r"y_{tw} = a Q^b + z_0",

    # Structures Dedicated Inversions
    "HYD_ST_VNOTCH_Q": r"Q = \frac{8}{15} C_d \sqrt{2g} \tan\left(\frac{\theta}{2}\right) H^{5/2}",
    "HYD_ST_VNOTCH_H": r"H = \left[ \frac{Q}{\frac{8}{15} C_d \sqrt{2g} \tan\left(\frac{\theta}{2}\right)} \right]^{2/5}",
    "HYD_ST_OGEE_Q": r"Q = C_o L_e H_e^{3/2}",
    "HYD_ST_OGEE_HE": r"H_e = \left( \frac{Q}{C_o L_e} \right)^{2/3}",
    "HYD_ST_OGEE_LE": r"L_e = \frac{Q}{C_o H_e^{3/2}}",
    "HYD_ST_BASIN_LSB": r"L_{sb} = k_{basin} y_2",
    "HYD_ST_BASIN_Y2": r"y_2 = \frac{L_{sb}}{k_{basin}}",

    # -------------------------------------------------------------------------
    # Pillar 5: Subsurface Groundwater & Well Hydraulics
    # -------------------------------------------------------------------------
    "HYD_GW_DARCY_1D_001": r"Q = -K A \frac{dh}{dl}",
    "HYD_GW_DARCY_FLUX_001": r"q = -K \frac{dh}{dl}",
    "HYD_GW_THIEM_CONFINED_001": r"Q = \frac{2 \pi T (h_2 - h_1)}{\ln(r_2 / r_1)}",
    "HYD_GW_THIEM_UNCONFINED_001": r"Q = \frac{\pi K (h_2^2 - h_1^2)}{\ln(r_2 / r_1)}",
    "HYD_GW_THEIS_001": [
        r"s = \frac{Q}{4 \pi T} W(u)",
        r"u = \frac{r^2 S}{4 T t}",
        r"W(u) = \int_u^\infty \frac{e^{-x}}{x} dx"
    ],
    "HYD_GW_COOPER_JACOB_001": r"s = \frac{2.303 Q}{4 \pi T} \log_{10}\left( \frac{2.25 T t}{r^2 S} \right)",

    # Groundwater Dedicated Inversions
    "HYD_GW_DARCY_Q": r"Q = -K A \frac{dh}{dl}",
    "HYD_GW_DARCY_K": r"K = -\frac{Q}{A \cdot \frac{dh}{dl}}",
    "HYD_GW_THIEM_Q": r"Q = \frac{2 \pi T (h_2 - h_1)}{\ln(r_2 / r_1)}",
    "HYD_GW_THIEM_T": r"T = \frac{Q \ln(r_2 / r_1)}{2 \pi (h_2 - h_1)}"
}

FUNCTION_SIGNATURES = {
    # Open Channel Conveyance & Geometries
    "HYD_OC_MANNING_001": "hydrocivil.hydraulics.manning_discharge(area, hydraulic_radius, slope, roughness, system='si')",
    "HYD_OC_MANNING_002": "hydrocivil.hydraulics.manning_velocity(hydraulic_radius, slope, roughness, system='si')",
    "HYD_OC_STRICKLER_001": "hydrocivil.hydraulics.strickler_velocity(hydraulic_radius, slope, k_st)",
    "HYD_OC_CHEZY_001": "hydrocivil.hydraulics.chezy_velocity(chezy_c, hydraulic_radius, slope)",
    "HYD_OC_KUTTER_001": "hydrocivil.hydraulics.kutter_chezy_c(hydraulic_radius, slope, roughness)",
    "HYD_OC_BAZIN_001": "hydrocivil.hydraulics.bazin_chezy_c(hydraulic_radius, gamma)",
    "HYD_OC_GEOM_RECT_001": "hydrocivil.hydraulics.geom_rectangular(bottom_width, depth)",
    "HYD_OC_GEOM_TRAP_001": "hydrocivil.hydraulics.geom_trapezoidal(bottom_width, side_slope, depth)",
    "HYD_OC_GEOM_TRI_001": "hydrocivil.hydraulics.geom_triangular(side_slope, depth)",
    "HYD_OC_GEOM_CIRC_001": "hydrocivil.hydraulics.geom_circular(diameter, depth)",
    "HYD_OC_GEOM_PARA_001": "hydrocivil.hydraulics.geom_parabolic(top_width, depth)",
    "HYD_OC_SPEC_ENERGY_001": "hydrocivil.hydraulics.specific_energy(depth, discharge, area, system='si')",
    "HYD_OC_FROUDE_001": "hydrocivil.hydraulics.froude_number(discharge, area, top_width, system='si')",
    "HYD_OC_SPEC_FORCE_001": "hydrocivil.hydraulics.specific_force(discharge, area, centroid_depth, system='si')",
    "HYD_OC_CRIT_DEPTH_RECT_001": "hydrocivil.hydraulics.critical_depth_rectangular(unit_discharge, system='si')",
    "HYD_OC_BELANGER_001": "hydrocivil.hydraulics.belanger_conjugate_depth(initial_depth, froude_1)",
    "HYD_OC_JUMP_LOSS_001": "hydrocivil.hydraulics.hydraulic_jump_head_loss(initial_depth, sequent_depth)",
    "HYD_OC_JUMP_LENGTH_001": "hydrocivil.hydraulics.hydraulic_jump_length(initial_depth, sequent_depth)",
    "HYD_OC_GVF_DYNAMIC_001": "hydrocivil.hydraulics.gvf_gradient(bed_slope, friction_slope, froude_number)",
    "HYD_OC_FRICTION_SLOPE_001": "hydrocivil.hydraulics.manning_friction_slope(discharge, roughness, area, hydraulic_radius, system='si')",
    "HYD_OC_DIRECT_STEP_001": "hydrocivil.hydraulics.direct_step(energy_1, energy_2, bed_slope, friction_slope_1, friction_slope_2)",
    "HYD_OC_OPT_RECT_001": "hydrocivil.hydraulics.optimal_rectangular_section(depth)",
    "HYD_OC_OPT_TRAP_001": "hydrocivil.hydraulics.optimal_trapezoidal_section(depth)",
    "HYD_OC_OPT_TRI_001": "hydrocivil.hydraulics.optimal_triangular_section(depth)",
    "HYD_OC_CRIT_VEL_001": "hydrocivil.hydraulics.critical_velocity(hydraulic_depth, system='si')",
    "HYD_OC_CRIT_SLOPE_001": "hydrocivil.hydraulics.critical_slope(roughness, critical_r_h, system='si')",
    "HYD_OC_WAVE_CELERITY_001": "hydrocivil.hydraulics.gravity_wave_celerity(hydraulic_depth, system='si')",
    "HYD_OC_JUMP_EFF_001": "hydrocivil.hydraulics.hydraulic_jump_efficiency(froude_1)",
    "HYD_OC_JUMP_HEIGHT_001": "hydrocivil.hydraulics.hydraulic_jump_height(initial_depth, sequent_depth)",
    "HYD_OC_CRIT_DEPTH_TRI_001": "hydrocivil.hydraulics.critical_depth_triangular(discharge, side_slope, system='si')",
    "HYD_OC_COMP_N_HORTON_001": "hydrocivil.hydraulics.horton_einstein_composite_n(perimeters, roughnesses)",
    "HYD_OC_COMP_N_PAVLOVSKII_001": "hydrocivil.hydraulics.pavlovskii_composite_n(perimeters, roughnesses)",
    "HYD_SED_SHEAR_STRESS_001": "hydrocivil.sediment.boundary_shear_stress(unit_weight, hydraulic_radius, slope)",
    "HYD_SED_SHEAR_VEL_001": "hydrocivil.sediment.shear_velocity(hydraulic_radius, slope, system='si')",
    "HYD_SED_SHIELDS_PARAM_001": "hydrocivil.sediment.shields_parameter(shear_stress, submerged_unit_weight, grain_size_d50)",
    "HYD_SED_CRIT_SHEAR_001": "hydrocivil.sediment.critical_shear_stress(critical_shields_param, submerged_unit_weight, grain_size_d50)",
    "HYD_SED_LANE_BALANCE_001": "hydrocivil.sediment.lane_sediment_balance(water_discharge, channel_slope, grain_size_d50)",
    "HYD_SED_MPM_BEDLOAD_001": "hydrocivil.sediment.meyer_peter_muller_bedload(shields_parameter)",
    "HYD_SED_RUBEY_SETTLING_001": "hydrocivil.sediment.rubey_settling_velocity(grain_diameter, specific_gravity=2.65, kinematic_viscosity=1e-6, system='si')",
    "HYD_SED_STOKES_SETTLING_001": "hydrocivil.sediment.stokes_settling_velocity(grain_diameter, specific_gravity=2.65, kinematic_viscosity=1e-6, system='si')",

    # Open Channel Inversions
    "HYD_OC_MANNING_Q": "hydrocivil.hydraulics.manning_q(area, hydraulic_radius, slope, roughness, system='si')",
    "HYD_OC_MANNING_V": "hydrocivil.hydraulics.manning_v(hydraulic_radius, slope, roughness, system='si')",
    "HYD_OC_MANNING_N": "hydrocivil.hydraulics.manning_n(discharge, area, hydraulic_radius, slope, system='si')",
    "HYD_OC_MANNING_S0": "hydrocivil.hydraulics.manning_s0(discharge, area, hydraulic_radius, roughness, system='si')",
    "HYD_OC_MANNING_A": "hydrocivil.hydraulics.manning_a(discharge, hydraulic_radius, slope, roughness, system='si')",
    "HYD_OC_MANNING_RH": "hydrocivil.hydraulics.manning_rh(discharge, area, slope, roughness, system='si')",
    "HYD_OC_STRICKLER_V": "hydrocivil.hydraulics.strickler_v(hydraulic_radius, slope, k_st)",
    "HYD_OC_STRICKLER_KST": "hydrocivil.hydraulics.strickler_kst(velocity, hydraulic_radius, slope)",
    "HYD_OC_STRICKLER_S0": "hydrocivil.hydraulics.strickler_s0(velocity, hydraulic_radius, k_st)",
    "HYD_OC_CHEZY_V": "hydrocivil.hydraulics.chezy_v(chezy_c, hydraulic_radius, slope)",
    "HYD_OC_CHEZY_C": "hydrocivil.hydraulics.chezy_c(velocity, hydraulic_radius, slope)",
    "HYD_OC_CHEZY_S0": "hydrocivil.hydraulics.chezy_s0(velocity, hydraulic_radius, chezy_c)",
    "HYD_OC_SPEC_ENERGY_E": "hydrocivil.hydraulics.specific_energy_e(depth, discharge, area, system='si')",
    "HYD_OC_SPEC_ENERGY_V": "hydrocivil.hydraulics.specific_energy_v(energy, depth, system='si')",
    "HYD_OC_SPEC_ENERGY_Q": "hydrocivil.hydraulics.specific_energy_q(energy, depth, area, system='si')",
    "HYD_OC_FROUDE_FR": "hydrocivil.hydraulics.froude_fr(discharge, area, top_width, system='si')",
    "HYD_OC_FROUDE_V": "hydrocivil.hydraulics.froude_v(froude_number, hydraulic_depth, system='si')",
    "HYD_OC_JUMP_Y2": "hydrocivil.hydraulics.hydraulic_jump_y2(initial_depth, froude_1)",
    "HYD_OC_JUMP_Y1": "hydrocivil.hydraulics.hydraulic_jump_y1(sequent_depth, froude_2)",
    "HYD_OC_JUMP_FR1": "hydrocivil.hydraulics.hydraulic_jump_fr1(initial_depth, sequent_depth)",
    "HYD_OC_JUMP_DE": "hydrocivil.hydraulics.hydraulic_jump_de(initial_depth, sequent_depth)",

    # Pressurized Pipe Flow & Culverts
    "HYD_PF_DARCY_WEISBACH_001": "hydrocivil.hydraulics.darcy_weisbach(friction_factor, length, diameter, velocity, system='si')",
    "HYD_PF_REYNOLDS_001": "hydrocivil.hydraulics.reynolds_number(velocity, diameter, kinematic_viscosity)",
    "HYD_PF_LAMINAR_F_001": "hydrocivil.hydraulics.laminar_friction(reynolds)",
    "HYD_PF_COLEBROOK_001": "hydrocivil.hydraulics.colebrook_white(relative_roughness, reynolds)",
    "HYD_PF_SWAMEE_JAIN_001": "hydrocivil.hydraulics.swamee_jain(relative_roughness, reynolds)",
    "HYD_PF_HAALAND_001": "hydrocivil.hydraulics.haaland(relative_roughness, reynolds)",
    "HYD_PF_CHURCHILL_001": "hydrocivil.hydraulics.churchill(relative_roughness, reynolds)",
    "HYD_PF_WOOD_001": "hydrocivil.hydraulics.wood(relative_roughness, reynolds)",
    "HYD_PF_HAZEN_WILLIAMS_001": "hydrocivil.hydraulics.hazen_williams(length, discharge, c_coefficient, diameter, system='si')",
    "HYD_PF_HAZEN_WILLIAMS_VEL_001": "hydrocivil.hydraulics.hazen_williams_velocity(c_coefficient, hydraulic_radius, slope, system='si')",
    "HYD_PF_MINOR_LOSS_001": "hydrocivil.hydraulics.minor_loss(loss_coefficient, velocity, system='si')",
    "HYD_PF_WAVE_CELERITY_001": "hydrocivil.hydraulics.wave_celerity(bulk_modulus, density, elastic_modulus, diameter, wall_thickness)",
    "HYD_PF_JOUKOWSKY_001": "hydrocivil.hydraulics.joukowsky(celerity, delta_v, system='si')",
    "HYD_PF_CRIT_CLOSURE_001": "hydrocivil.hydraulics.critical_closure_time(length, celerity)",
    "HYD_PF_CULVERT_INLET_UNSUB_001": "hydrocivil.hydraulics.culvert_inlet_unsubmerged(discharge, diameter, area, critical_energy, slope, k_coeff=0.0098, m_exp=2.0)",
    "HYD_PF_CULVERT_INLET_SUB_001": "hydrocivil.hydraulics.culvert_inlet_submerged(discharge, diameter, area, slope, c_coeff=0.0398, y_const=0.67)",
    "HYD_PF_CULVERT_OUTLET_001": "hydrocivil.hydraulics.culvert_outlet_control_head(tailwater_term, total_losses, length, slope)",
    "HYD_PF_CULVERT_ENTRANCE_001": "hydrocivil.hydraulics.culvert_entrance_loss(entrance_coeff, velocity, system='si')",
    "HYD_PF_HARDY_CROSS_001": "hydrocivil.hydraulics.hardy_cross_correction(sum_head_loss, sum_derivative, n_exp=2.0)",
    "HYD_PF_EQUIV_LENGTH_001": "hydrocivil.hydraulics.equivalent_pipe_length(minor_loss_coeff, diameter, friction_factor)",
    "HYD_PF_SERIES_DIAMETER_001": "hydrocivil.hydraulics.equivalent_diameter_series(total_length, sum_ratio)",
    "HYD_PF_PARALLEL_FLOW_001": "hydrocivil.hydraulics.parallel_pipes_distribution(total_discharge, branch_conductance, sum_conductance)",
    "HYD_PF_WATER_POWER_001": "hydrocivil.hydraulics.water_horsepower(discharge, head, specific_weight=None, system='si')",
    "HYD_PF_BRAKE_POWER_001": "hydrocivil.hydraulics.pump_brake_power(water_power, efficiency)",

    # Pipe Flow Inversions
    "HYD_PF_DARCY_HF": "hydrocivil.hydraulics.darcy_weisbach_hf(friction_factor, length, diameter, velocity, system='si')",
    "HYD_PF_DARCY_F": "hydrocivil.hydraulics.darcy_weisbach_f(head_loss, length, diameter, velocity, system='si')",
    "HYD_PF_DARCY_V": "hydrocivil.hydraulics.darcy_weisbach_v(head_loss, length, diameter, friction_factor, system='si')",
    "HYD_PF_DARCY_D": "hydrocivil.hydraulics.darcy_weisbach_d(head_loss, length, friction_factor, velocity, system='si')",
    "HYD_PF_DARCY_Q": "hydrocivil.hydraulics.darcy_weisbach_q(head_loss, length, diameter, friction_factor, system='si')",
    "HYD_PF_REYNOLDS_RE": "hydrocivil.hydraulics.reynolds_re(velocity, diameter, kinematic_viscosity)",
    "HYD_PF_REYNOLDS_V": "hydrocivil.hydraulics.reynolds_v(reynolds, diameter, kinematic_viscosity)",
    "HYD_PF_HW_HF": "hydrocivil.hydraulics.hazen_williams_hf(length, discharge, c_coefficient, diameter, system='si')",
    "HYD_PF_HW_Q": "hydrocivil.hydraulics.hazen_williams_q(head_loss, length, c_coefficient, diameter, system='si')",
    "HYD_PF_HW_D": "hydrocivil.hydraulics.hazen_williams_d(head_loss, length, discharge, c_coefficient, system='si')",
    "HYD_PF_MINOR_HM": "hydrocivil.hydraulics.minor_loss_hm(loss_coefficient, velocity, system='si')",
    "HYD_PF_MINOR_KL": "hydrocivil.hydraulics.minor_loss_kl(head_loss, velocity, system='si')",
    "HYD_PF_POWER_PW": "hydrocivil.hydraulics.water_power_pw(discharge, head, specific_weight=None, system='si')",
    "HYD_PF_POWER_Q": "hydrocivil.hydraulics.water_power_q(power, head, specific_weight=None, system='si')",

    # Hydrology & Watershed Runoff
    "HYD_HY_IDF_SHERMAN_001": "hydrocivil.hydrology.idf_sherman(duration, a, b, c)",
    "HYD_HY_THIESSEN_001": "hydrocivil.hydrology.thiessen_areal(weights, precip)",
    "HYD_HY_HORTON_INF_001": "hydrocivil.hydrology.horton_rate(time, initial_capacity, steady_capacity, decay_constant)",
    "HYD_HY_HORTON_CUM_001": "hydrocivil.hydrology.horton_cumulative(time, initial_capacity, steady_capacity, decay_constant)",
    "HYD_HY_GREEN_AMPT_001": "hydrocivil.hydrology.green_ampt_rate(hydraulic_conductivity, suction_head, moisture_deficit, cumulative_depth)",
    "HYD_HY_SCS_CN_STORAGE_001": "hydrocivil.hydrology.scs_retention(curve_number, system='si')",
    "HYD_HY_SCS_CN_RUNOFF_001": "hydrocivil.hydrology.scs_runoff_depth(precip, retention, lambda_ratio=0.2)",
    "HYD_HY_RATIONAL_001": "hydrocivil.hydrology.rational_peak_flow(runoff_coefficient, intensity, area, system='si')",
    "HYD_HY_KIRPICH_001": "hydrocivil.hydrology.kirpich_tc(length, slope, system='si')",
    "HYD_HY_SNYDER_001": "hydrocivil.hydrology.snyder(basin_length, length_to_centroid, area, c_t=1.5, c_p=0.6, system='si')",
    "HYD_HY_SCS_DIM_UH_001": "hydrocivil.hydrology.scs_peak_flow(area, time_to_peak, system='si')",
    "HYD_HY_MUSKINGUM_001": "hydrocivil.hydrology.muskingum_coefficients(travel_time_k, weighting_factor_x, time_step_dt)",
    "HYD_HY_MUSKINGUM_ROUTING_001": "hydrocivil.hydrology.muskingum_route(inflow, travel_time_k, weighting_factor_x, time_step_dt, initial_outflow=None)",
    "HYD_HY_COMPOSITE_CN_001": "hydrocivil.hydrology.scs_composite_cn(subareas, curve_numbers)",
    "HYD_HY_SCS_AMC_I_001": "hydrocivil.hydrology.scs_cn_amc_i(curve_number_amc2)",
    "HYD_HY_SCS_AMC_III_001": "hydrocivil.hydrology.scs_cn_amc_iii(curve_number_amc2)",
    "HYD_HY_TR55_SHEET_FLOW_001": "hydrocivil.hydrology.tr55_sheet_flow_time(sheet_roughness, flow_length, two_year_24hr_precip, land_slope)",
    "HYD_HY_TR55_SHALLOW_VEL_001": "hydrocivil.hydrology.tr55_shallow_concentrated_velocity(land_slope, surface_coeff=16.1345)",
    "HYD_HY_GUMBEL_FLOOD_001": "hydrocivil.hydrology.gumbel_flood_frequency(sample_mean, sample_std, return_period)",
    "HYD_HY_NASH_CASCADE_001": "hydrocivil.hydrology.nash_cascade_iuh(time, number_reservoirs, storage_constant)",
    "HYD_HY_HARGREAVES_ET0_001": "hydrocivil.hydrology.hargreaves_samani_et0(extraterrestrial_radiation, mean_temp, max_temp, min_temp)",
    "HYD_HY_PENMAN_RAD_001": "hydrocivil.hydrology.net_radiation_equivalent_evap(net_radiation_mj, latent_heat_vaporization=2.45e6, water_density=1000.0)",
    "HYD_HY_TIME_AREA_RUNOFF_001": "hydrocivil.hydrology.time_area_runoff_step(effective_excess_precip, isochrone_subarea, unit_conversion=0.278)",

    # Hydrology Inversions
    "HYD_HY_RATIONAL_Q": "hydrocivil.hydrology.rational_q(runoff_coeff, intensity, area, system='si')",
    "HYD_HY_RATIONAL_C": "hydrocivil.hydrology.rational_c(discharge, intensity, area, system='si')",
    "HYD_HY_RATIONAL_A": "hydrocivil.hydrology.rational_a(discharge, runoff_coeff, intensity, system='si')",
    "HYD_HY_SCS_CN_S": "hydrocivil.hydrology.scs_cn_s(curve_number, system='si')",
    "HYD_HY_SCS_CN_CN": "hydrocivil.hydrology.scs_cn_cn(retention, system='si')",
    "HYD_HY_SCS_CN_Q": "hydrocivil.hydrology.scs_cn_q(precip, retention, lambda_ratio=0.2)",
    "HYD_HY_SCS_CN_P": "hydrocivil.hydrology.scs_cn_p(discharge, retention, lambda_ratio=0.2)",
    "HYD_HY_HORTON_FP": "hydrocivil.hydrology.horton_rate_fp(time, initial_capacity, steady_capacity, decay_constant)",
    "HYD_HY_HORTON_K": "hydrocivil.hydrology.horton_rate_k(time, current_rate, initial_capacity, steady_capacity)",

    # Structures, Spillways & Dissipators
    "HYD_ST_RECT_WEIR_001": "hydrocivil.structures.francis_weir(length, head, contractions=0.0, system='si')",
    "HYD_ST_VNOTCH_WEIR_001": "hydrocivil.structures.v_notch_weir(notch_angle_deg, head, discharge_coeff=0.585, system='si')",
    "HYD_ST_BROAD_WEIR_001": "hydrocivil.structures.broad_crested_weir(length, head, discharge_coeff=0.848, system='si')",
    "HYD_ST_PARSHALL_001": "hydrocivil.structures.parshall_flume(throat_width, head, coeff_c=2.32, exp_n=1.522)",
    "HYD_ST_ORIFICE_FREE_001": "hydrocivil.structures.orifice_free(area, head, discharge_coeff=0.62, system='si')",
    "HYD_ST_ORIFICE_SUB_001": "hydrocivil.structures.orifice_submerged(area, upstream_head, downstream_head, discharge_coeff=0.62, system='si')",
    "HYD_ST_SLUICE_FREE_001": "hydrocivil.structures.sluice_gate_free(gate_width, gate_opening, upstream_depth, discharge_coeff=0.6, system='si')",
    "HYD_ST_SLUICE_SUB_001": "hydrocivil.structures.sluice_gate_submerged(gate_width, gate_opening, upstream_depth, tailwater_depth, submerged_coeff=0.6, system='si')",
    "HYD_ST_OGEE_SPILLWAY_001": "hydrocivil.structures.ogee_spillway_discharge(discharge_coeff, effective_length, total_head)",
    "HYD_ST_OGEE_COEFF_001": "hydrocivil.structures.ogee_discharge_coefficient(design_coeff, actual_head, design_head)",
    "HYD_ST_EFF_CREST_LEN_001": "hydrocivil.structures.spillway_effective_length(clear_length, n_piers=0, k_pier=0.02, k_abutment=0.1, total_head=0.0)",
    "HYD_ST_CHUTE_VELOCITY_001": "hydrocivil.structures.chute_terminal_velocity(total_fall, head_loss=0.0, system='si')",
    "HYD_ST_STILLING_BASIN_001": "hydrocivil.structures.stilling_basin_length(sequent_depth, basin_coeff=4.3)",
    "HYD_ST_MORNING_GLORY_001": "hydrocivil.structures.morning_glory_weir_flow(crest_radius, head_on_crest, discharge_coeff=2.0)",
    "HYD_ST_SIPHON_SPILLWAY_001": "hydrocivil.structures.siphon_spillway_discharge(throat_area, operating_head, discharge_coeff=0.8, system='si')",
    "HYD_ST_DROP_STRUCT_001": "hydrocivil.structures.drop_structure_depth(drop_height, unit_discharge, system='si')",
    "HYD_ST_TAILWATER_001": "hydrocivil.structures.tailwater_depth(discharge, rating_a, rating_b, base_elevation=0.0)",

    # Structures Inversions
    "HYD_ST_VNOTCH_Q": "hydrocivil.structures.v_notch_weir_q(notch_angle_deg, head, discharge_coeff=0.585, system='si')",
    "HYD_ST_VNOTCH_H": "hydrocivil.structures.v_notch_weir_h(discharge, notch_angle_deg, discharge_coeff=0.585, system='si')",
    "HYD_ST_OGEE_Q": "hydrocivil.structures.ogee_spillway_q(discharge_coeff, effective_length, total_head)",
    "HYD_ST_OGEE_HE": "hydrocivil.structures.ogee_spillway_he(discharge, discharge_coeff, effective_length)",
    "HYD_ST_OGEE_LE": "hydrocivil.structures.ogee_spillway_le(discharge, discharge_coeff, total_head)",
    "HYD_ST_BASIN_LSB": "hydrocivil.structures.stilling_basin_lsb(sequent_depth, basin_coeff=4.3)",
    "HYD_ST_BASIN_Y2": "hydrocivil.structures.stilling_basin_y2(basin_length, basin_coeff=4.3)",

    # Groundwater & Aquifer Mechanics
    "HYD_GW_DARCY_1D_001": "hydrocivil.groundwater.darcy_flow_1d(hydraulic_conductivity, area, hydraulic_gradient)",
    "HYD_GW_DARCY_FLUX_001": "hydrocivil.groundwater.darcy_flux(hydraulic_conductivity, hydraulic_gradient)",
    "HYD_GW_THIEM_CONFINED_001": "hydrocivil.groundwater.thiem_confined(transmissivity, h1, h2, r1, r2)",
    "HYD_GW_THIEM_UNCONFINED_001": "hydrocivil.groundwater.thiem_unconfined(hydraulic_conductivity, h1, h2, r1, r2)",
    "HYD_GW_THEIS_001": "hydrocivil.groundwater.theis_drawdown(pumping_rate, transmissivity, storativity, radius, time)",
    "HYD_GW_COOPER_JACOB_001": "hydrocivil.groundwater.cooper_jacob_drawdown(pumping_rate, transmissivity, storativity, radius, time)",

    # Groundwater Inversions
    "HYD_GW_DARCY_Q": "hydrocivil.groundwater.darcy_flow_q(hydraulic_conductivity, area, hydraulic_gradient)",
    "HYD_GW_DARCY_K": "hydrocivil.groundwater.darcy_flow_k(discharge, area, hydraulic_gradient)",
    "HYD_GW_THIEM_Q": "hydrocivil.groundwater.thiem_confined_q(transmissivity, h1, h2, r1, r2)",
    "HYD_GW_THIEM_T": "hydrocivil.groundwater.thiem_confined_t(discharge, h1, h2, r1, r2)"
}

FUNCTION_DESCRIPTIONS = {
    # Open Channel Conveyance & Geometries
    "HYD_OC_MANNING_001": "Calculates volumetric discharge Q in open channels under steady uniform flow conditions based on cross-sectional area, hydraulic radius, bed slope, and boundary roughness.",
    "HYD_OC_MANNING_002": "Evaluates cross-sectional mean flow velocity V in open channels under steady uniform flow using Manning's roughness coefficient.",
    "HYD_OC_STRICKLER_001": "Computes mean flow velocity V using Strickler's roughness coefficient k_st = 1/n, commonly adopted in European river engineering and alpine torrent hydraulics.",
    "HYD_OC_CHEZY_001": "Calculates mean flow velocity V using the classical Chézy resistance formulation based on hydraulic radius and longitudinal bed slope.",
    "HYD_OC_KUTTER_001": "Derives the empirical Chézy resistance coefficient C using the Ganguillet-Kutter formulation as a function of roughness n, slope S_0, and hydraulic radius R_h.",
    "HYD_OC_BAZIN_001": "Computes the empirical Chézy resistance coefficient C using Bazin's formulation based on wall roughness parameter gamma and hydraulic radius R_h.",
    "HYD_OC_GEOM_RECT_001": "Computes all fundamental geometric properties of a rectangular cross-section: Area A, Wetted Perimeter P, Hydraulic Radius R_h, Top Width T, Hydraulic Depth D_h, and Centroid Depth y_bar.",
    "HYD_OC_GEOM_TRAP_001": "Evaluates the geometric properties of a symmetric trapezoidal channel with side slopes m:1 (horizontal:vertical), determining A, P, R_h, T, D_h, and centroid depth.",
    "HYD_OC_GEOM_TRI_001": "Calculates geometric properties for a symmetric triangular channel (V-shaped) with side slopes m:1.",
    "HYD_OC_GEOM_CIRC_001": "Evaluates partially full circular pipe and culvert flow geometry using the central angle subtended by the free water surface.",
    "HYD_OC_GEOM_PARA_001": "Computes geometric parameters of a parabolic channel cross-section based on water surface top width T and central depth y.",
    "HYD_OC_SPEC_ENERGY_001": "Computes specific energy E (energy head measured relative to channel bottom) as the sum of flow depth and velocity head.",
    "HYD_OC_FROUDE_001": "Calculates the dimensionless Froude number Fr representing the ratio of inertial forces to gravitational forces. Classifies flow as subcritical (Fr < 1), critical (Fr = 1), or supercritical (Fr > 1).",
    "HYD_OC_SPEC_FORCE_001": "Calculates specific force (momentum function) M composed of flow momentum flux and hydrostatic pressure force, conserved across rapidly varied transitions.",
    "HYD_OC_CRIT_DEPTH_RECT_001": "Computes the critical depth y_c in a rectangular channel corresponding to the minimum specific energy state for a given unit discharge q.",
    "HYD_OC_BELANGER_001": "Solves Bélanger's momentum conservation equation to find the subcritical sequent depth y_2 following a hydraulic jump in a rectangular horizontal channel.",
    "HYD_OC_JUMP_LOSS_001": "Determines the total energy head dissipation Delta_E across a classical hydraulic jump in a rectangular channel as a function of initial and sequent depths.",
    "HYD_OC_JUMP_LENGTH_001": "Estimates the longitudinal length L_j of a classical hydraulic jump based on USBR and Silvester empirical formulations.",
    "HYD_OC_GVF_DYNAMIC_001": "Evaluates the fundamental differential equation dy/dx of Gradually Varied Flow (GVF) relating water surface slope to bed slope, friction slope, and Froude number.",
    "HYD_OC_FRICTION_SLOPE_001": "Calculates the energy gradient (friction slope S_f) for non-uniform flow by inverting Manning's conveyance equation.",
    "HYD_OC_DIRECT_STEP_001": "Applies the Direct Step integration method to calculate reach distance Delta_x between two specified water depths in prismatic channels.",
    "HYD_OC_OPT_RECT_001": "Computes the dimensions and hydraulic parameters of the hydraulically most efficient rectangular open channel section minimizing wetted perimeter for a specified depth.",
    "HYD_OC_OPT_TRAP_001": "Evaluates the best hydraulic trapezoidal section (half of a regular hexagon) which delivers maximum discharge for a given cross-sectional excavation area.",
    "HYD_OC_OPT_TRI_001": "Calculates the most efficient triangular open channel section having a 90-degree central apex angle (side slope 1:1) and maximum hydraulic radius.",
    "HYD_OC_CRIT_VEL_001": "Computes critical flow velocity V_c at which the Froude number equals unity, representing the threshold between subcritical gravity streaming and supercritical shooting flow.",
    "HYD_OC_CRIT_SLOPE_001": "Calculates the critical bed slope S_c that sustains uniform flow at critical depth for a specified discharge and channel boundary roughness.",
    "HYD_OC_WAVE_CELERITY_001": "Evaluates shallow-water gravity wave celerity c relative to the flowing fluid in an open channel of hydraulic depth D_h.",
    "HYD_OC_JUMP_EFF_001": "Computes the hydraulic jump efficiency (ratio of post-jump to pre-jump specific energy E_2/E_1) as a direct function of initial inflow Froude number Fr_1.",
    "HYD_OC_JUMP_HEIGHT_001": "Calculates the physical vertical height h_j of a hydraulic jump roller from the supercritical initial depth y_1 to subcritical sequent depth y_2.",
    "HYD_OC_CRIT_DEPTH_TRI_001": "Computes the exact closed-form critical depth y_c for a triangular channel with side slopes m:1 under a specified total discharge Q.",
    "HYD_OC_COMP_N_HORTON_001": "Derives the equivalent composite Manning roughness coefficient across composite channel perimeters using the Horton-Einstein equal-velocity weighting hypothesis.",
    "HYD_OC_COMP_N_PAVLOVSKII_001": "Calculates composite Manning roughness using Pavlovskii's total resisting shear force formulation across heterogeneous channel boundary subsections.",
    "HYD_SED_SHEAR_STRESS_001": "Calculates mean boundary shear stress tau_0 exerted by flowing water on open channel beds and alluvial riverbanks according to Du Boys.",
    "HYD_SED_SHEAR_VEL_001": "Evaluates bed shear velocity u_* representing turbulent shear velocity scales and boundary layer velocity fluctuations.",
    "HYD_SED_SHIELDS_PARAM_001": "Computes the dimensionless Shields entrainment parameter theta_* representing the ratio of destabilizing hydrodynamic shear force to submerged particle weight.",
    "HYD_SED_CRIT_SHEAR_001": "Determines the critical threshold shear stress tau_c required to initiate sediment grain motion on alluvial riverbeds.",
    "HYD_SED_LANE_BALANCE_001": "Evaluates Lane's stable channel equilibrium balance index relating water discharge Q, channel slope S, and median grain size d_50.",
    "HYD_SED_MPM_BEDLOAD_001": "Calculates dimensionless bedload transport intensity q_b^* using the authoritative Meyer-Peter & Müller formulation for coarse sand and gravel beds.",
    "HYD_SED_RUBEY_SETTLING_001": "Evaluates Rubey's settling velocity w_s for silt, sand, and gravel particles spanning intermediate Reynolds numbers (0.1 < Re_p < 1000).",
    "HYD_SED_STOKES_SETTLING_001": "Calculates Stokes laminar terminal settling velocity w_s for spherical fine particles (clays and silts) under creeping flow conditions (Re_p < 0.1).",

    # Open Channel Inversions
    "HYD_OC_MANNING_Q": "Forward Manning discharge evaluation solving for volumetric flow rate Q from channel geometry, roughness, and slope.",
    "HYD_OC_MANNING_V": "Evaluates uniform open-channel mean velocity V from hydraulic radius, roughness, and energy slope.",
    "HYD_OC_MANNING_N": "Direct analytical inversion of Manning's formula isolating roughness coefficient n from known discharge, cross-sectional area, hydraulic radius, and bed slope.",
    "HYD_OC_MANNING_S0": "Direct analytical inversion isolating required longitudinal bed slope S_0 to convey design discharge Q under specified channel cross-section and roughness.",
    "HYD_OC_MANNING_A": "Solves for required cross-sectional flow area A under uniform Manning flow conditions.",
    "HYD_OC_MANNING_RH": "Analytically isolates required hydraulic radius R_h from known discharge Q, flow area A, roughness n, and longitudinal slope S_0.",
    "HYD_OC_STRICKLER_V": "Computes mean velocity V using Strickler roughness coefficient k_st.",
    "HYD_OC_STRICKLER_KST": "Inverts Strickler formula to back-calculate roughness parameter k_st from measured velocity, hydraulic radius, and energy slope.",
    "HYD_OC_STRICKLER_S0": "Solves for required bed slope S_0 sustaining velocity V under Strickler formulation.",
    "HYD_OC_CHEZY_V": "Calculates mean open-channel flow velocity V using Chézy resistance coefficient C.",
    "HYD_OC_CHEZY_C": "Inverts Chézy formula to back-calculate conveyance resistance coefficient C from observed velocity V, hydraulic radius R_h, and slope S_0.",
    "HYD_OC_CHEZY_S0": "Calculates required channel gradient S_0 under Chézy flow resistance.",
    "HYD_OC_SPEC_ENERGY_E": "Computes specific energy head E relative to channel bottom for given depth and flow conditions.",
    "HYD_OC_SPEC_ENERGY_V": "Solves for flow velocity V corresponding to a specified specific energy head E and flow depth y.",
    "HYD_OC_SPEC_ENERGY_Q": "Calculates total discharge Q for a given specific energy head E, flow depth y, and cross-sectional area A.",
    "HYD_OC_FROUDE_FR": "Evaluates dimensionless Froude number Fr characterizing inertial to gravitational force ratio.",
    "HYD_OC_FROUDE_V": "Computes flow velocity V required to achieve a specified target Froude number Fr at hydraulic depth D_h.",
    "HYD_OC_JUMP_Y2": "Computes subcritical sequent depth y_2 following a classical hydraulic jump given upstream depth y_1 and Froude number Fr_1.",
    "HYD_OC_JUMP_Y1": "Inverts Bélanger's momentum conservation equation to find initial supercritical inflow depth y_1 from downstream sequent depth y_2 and downstream Froude number Fr_2.",
    "HYD_OC_JUMP_FR1": "Calculates upstream supercritical inflow Froude number Fr_1 from the ratio of conjugate depths y_2 / y_1.",
    "HYD_OC_JUMP_DE": "Calculates energy head dissipation Delta_E across a classical hydraulic jump in a rectangular horizontal channel.",

    # Pressurized Pipe Flow & Culverts
    "HYD_PF_DARCY_WEISBACH_001": "Evaluates pipe friction head loss h_f using the fundamental Darcy-Weisbach equation applicable to all fluids across all flow regimes.",
    "HYD_PF_REYNOLDS_001": "Computes the dimensionless Reynolds number Re characterizing laminar vs. turbulent flow regimes in pressurized circular conduits.",
    "HYD_PF_LAMINAR_F_001": "Computes the exact theoretical Darcy friction factor f = 64/Re for laminar Hagen-Poiseuille pipe flow (Re < 2000).",
    "HYD_PF_COLEBROOK_001": "Solves the implicit Colebrook-White equation for turbulent transition and fully rough pipe flow using vectorized multi-core Newton-Raphson root finding.",
    "HYD_PF_SWAMEE_JAIN_001": "Explicit approximation of the Colebrook-White equation providing direct calculation of friction factor f with less than 1% deviation.",
    "HYD_PF_HAALAND_001": "Haaland's explicit approximation for the Darcy-Weisbach friction factor f, valid across the entire turbulent transition regime.",
    "HYD_PF_CHURCHILL_001": "Churchill's universal explicit equation continuously spanning laminar, critical transition, and fully turbulent flow regimes without discontinuities.",
    "HYD_PF_WOOD_001": "Wood's explicit formulation for pipe friction factor f in commercial turbulent water distribution pipes.",
    "HYD_PF_HAZEN_WILLIAMS_001": "Evaluates friction head loss h_f in pressurized water distribution pipes using the empirical Hazen-Williams formula with roughness C.",
    "HYD_PF_HAZEN_WILLIAMS_VEL_001": "Computes mean velocity V in pipes flowing full or open conduits using Hazen-Williams empirical coefficient C.",
    "HYD_PF_MINOR_LOSS_001": "Calculates local minor head loss h_m caused by valves, bends, expansions, contractions, and fittings via resistance coefficient K_L.",
    "HYD_PF_WAVE_CELERITY_001": "Determines acoustic pressure wave celerity a in elastic conduits considering liquid bulk modulus and conduit wall elasticity.",
    "HYD_PF_JOUKOWSKY_001": "Computes maximum water hammer transient pressure head rise Delta_H resulting from rapid valve closure according to Joukowsky's law.",
    "HYD_PF_CRIT_CLOSURE_001": "Calculates the critical valve closure time T_c representing the two-way wave travel time from valve to reservoir and back.",
    "HYD_PF_CULVERT_INLET_UNSUB_001": "Computes unsubmerged culvert inlet control headwater ratio HW_i/D according to FHWA HDS-5 empirical form 1 / 2 formulations.",
    "HYD_PF_CULVERT_INLET_SUB_001": "Evaluates submerged culvert inlet control headwater ratio HW_i/D under orifice-action submergence following FHWA HDS-5 standards.",
    "HYD_PF_CULVERT_OUTLET_001": "Determines the upstream headwater elevation HW_o under culvert outlet control full-barrel pressurized flow accounting for barrel friction and entrance losses.",
    "HYD_PF_CULVERT_ENTRANCE_001": "Calculates the localized head loss h_e at the culvert barrel entrance as a function of inlet geometry coefficient K_e (beveled, square-edge, or wingwall).",
    "HYD_PF_HARDY_CROSS_001": "Evaluates the flow loop correction delta_Q in closed-loop pipe distribution networks using Hardy Cross successive head-loss balance approximations.",
    "HYD_PF_EQUIV_LENGTH_001": "Converts localized minor head loss components (valves, elbows, meters) into an equivalent length L_e of straight pipe with identical diameter and friction factor.",
    "HYD_PF_SERIES_DIAMETER_001": "Calculates the uniform equivalent diameter D_e that replaces multiple pipes of varying diameters connected in series while preserving identical total head loss.",
    "HYD_PF_PARALLEL_FLOW_001": "Distributes total network inflow across parallel pipe branches in proportion to hydraulic conductance k_i under equal head loss constraints.",
    "HYD_PF_WATER_POWER_001": "Calculates theoretical water power (net hydraulic energy imparted to or extracted from flowing water) across pumps or turbines.",
    "HYD_PF_BRAKE_POWER_001": "Computes mechanical brake power P_b required to drive a pump given theoretical water power P_w and pump mechanical/hydraulic efficiency eta.",

    # Pipe Flow Inversions
    "HYD_PF_DARCY_HF": "Evaluates pipe friction head loss h_f from Darcy-Weisbach friction factor f, length L, diameter D, and velocity V.",
    "HYD_PF_DARCY_F": "Inverts Darcy-Weisbach equation to back-calculate friction factor f from measured head loss h_f, length L, diameter D, and velocity V.",
    "HYD_PF_DARCY_V": "Calculates permissible flow velocity V for a specified available friction head loss h_f, pipe length L, diameter D, and friction factor f.",
    "HYD_PF_DARCY_D": "Direct analytical inversion sizing internal pipe diameter D required to deliver velocity V within maximum allowable friction loss h_f.",
    "HYD_PF_DARCY_Q": "Evaluates pipe volumetric discharge Q under available friction head loss h_f in pressurized circular pipes.",
    "HYD_PF_REYNOLDS_RE": "Calculates Reynolds number Re from mean velocity V, diameter D, and fluid kinematic viscosity nu.",
    "HYD_PF_REYNOLDS_V": "Inverts Reynolds relationship to find flow velocity V corresponding to a target Reynolds number Re.",
    "HYD_PF_HW_HF": "Evaluates friction head loss h_f using Hazen-Williams formulation with exact D^4.87 exponent alignment.",
    "HYD_PF_HW_Q": "Inverts Hazen-Williams formula to solve for volumetric discharge Q under specified allowable head loss h_f.",
    "HYD_PF_HW_D": "Solves for required conduit diameter D under Hazen-Williams friction loss constraints.",
    "HYD_PF_MINOR_HM": "Calculates localized minor head loss h_m from loss coefficient K_L and flow velocity V.",
    "HYD_PF_MINOR_KL": "Back-calculates fitting loss coefficient K_L from measured head loss h_m and conduit velocity V.",
    "HYD_PF_POWER_PW": "Calculates theoretical hydraulic power P_w imparted to fluid by pump or extracted by turbine.",
    "HYD_PF_POWER_Q": "Inverts water power formula to calculate deliverable discharge Q for available hydraulic power P_w and total dynamic head H.",

    # Hydrology & Watershed Runoff
    "HYD_HY_IDF_SHERMAN_001": "Sherman intensity-duration-frequency (IDF) empirical relation estimating design storm rainfall intensity i as a function of storm duration t_d.",
    "HYD_HY_THIESSEN_001": "Calculates mean catchment areal precipitation using Thiessen polygon geometric weighting coefficients applied to rain gage networks.",
    "HYD_HY_HORTON_INF_001": "Evaluates Horton's infiltration capacity rate f_p(t) undergoing exponential decay from initial capacity f_0 to steady equilibrium rate f_c.",
    "HYD_HY_HORTON_CUM_001": "Integrates Horton's infiltration equation over time to determine cumulative infiltration depth F(t).",
    "HYD_HY_GREEN_AMPT_001": "Evaluates Green-Ampt physically-based infiltration rate based on wetting front matric suction head, moisture deficit, and saturated hydraulic conductivity.",
    "HYD_HY_SCS_CN_STORAGE_001": "Determines watershed potential maximum soil moisture retention S from the dimensionless NRCS Curve Number CN.",
    "HYD_HY_SCS_CN_RUNOFF_001": "Calculates total direct surface runoff depth Q from storm rainfall depth P using the standard NRCS Curve Number method with initial abstraction I_a.",
    "HYD_HY_RATIONAL_001": "Estimates peak catchment runoff rate Q for small urban and rural watersheds using the classical Rational Method based on runoff coefficient C and rainfall intensity I.",
    "HYD_HY_KIRPICH_001": "Computes time of concentration t_c (time required for runoff to travel from hydraulically most distant point to outlet) using Kirpich's formula.",
    "HYD_HY_SNYDER_001": "Derives synthetic unit hydrograph characteristics: basin lag time t_p and peak unit discharge Q_p based on basin geometry parameters L and L_c.",
    "HYD_HY_SCS_DIM_UH_001": "Calculates peak discharge q_p of the standard NRCS dimensionless unit hydrograph from watershed drainage area and time to peak.",
    "HYD_HY_MUSKINGUM_001": "Derives Muskingum linear flood routing coefficients C_0, C_1, C_2 based on reach travel time K, attenuation factor X, and routing interval dt.",
    "HYD_HY_MUSKINGUM_ROUTING_001": "Performs iterative step-by-step hydrologic channel routing of an inflow hydrograph series through a river reach using Muskingum's equation.",
    "HYD_HY_COMPOSITE_CN_001": "Calculates area-weighted composite NRCS Runoff Curve Number across heterogeneous land uses, soil complexes, and hydrologic conditions.",
    "HYD_HY_SCS_AMC_I_001": "Adjusts Curve Number from average antecedent moisture condition (AMC II) to dry condition (AMC I, 5-day prior rainfall < 13 mm).",
    "HYD_HY_SCS_AMC_III_001": "Adjusts Curve Number from average antecedent moisture condition (AMC II) to saturated wet condition (AMC III, 5-day prior rainfall > 28 mm).",
    "HYD_HY_TR55_SHEET_FLOW_001": "Computes sheet flow travel time T_t (hours) for overland flow lengths up to 300 ft using the USDA-NRCS TR-55 Manning kinematic equation.",
    "HYD_HY_TR55_SHALLOW_VEL_001": "Estimates average shallow concentrated flow velocity V across unpaved (k=16.13) or paved (k=20.33) rills and gullies according to TR-55.",
    "HYD_HY_GUMBEL_FLOOD_001": "Computes design flood peak quantile X_T for return period T years using Gumbel's Extreme Value Type 1 (EV-1) probability distribution.",
    "HYD_HY_NASH_CASCADE_001": "Generates Instantaneous Unit Hydrograph (IUH) ordinates u(t) modeling catchment routing through a cascade of n linear reservoirs each with storage delay K.",
    "HYD_HY_HARGREAVES_ET0_001": "Calculates reference crop evapotranspiration ET_0 (mm/day) using the temperature-based Hargreaves-Samani model suitable for data-sparse regions.",
    "HYD_HY_PENMAN_RAD_001": "Converts net solar and terrestrial radiation R_n (MJ/m^2/day) into equivalent depth of water evaporated (mm/day) using latent heat of vaporization.",
    "HYD_HY_TIME_AREA_RUNOFF_001": "Evaluates direct surface runoff discharge Q_j via time-area convolution between hyetograph excess rainfall intensities and watershed travel-time isochrones.",

    # Hydrology Inversions
    "HYD_HY_RATIONAL_Q": "Evaluates peak runoff rate Q from runoff coefficient C, rainfall intensity I, and catchment area A.",
    "HYD_HY_RATIONAL_C": "Inverts Rational formula to calculate effective watershed runoff coefficient C from observed peak flow rate Q.",
    "HYD_HY_RATIONAL_A": "Calculates required catchment drainage area A for a specified design discharge Q, intensity I, and runoff coefficient C.",
    "HYD_HY_SCS_CN_S": "Computes potential maximum soil moisture retention S from Curve Number CN.",
    "HYD_HY_SCS_CN_CN": "Inverts retention formula to back-calculate NRCS Curve Number CN from calibrated retention parameter S.",
    "HYD_HY_SCS_CN_Q": "Calculates direct runoff depth Q from storm rainfall depth P and retention parameter S.",
    "HYD_HY_SCS_CN_P": "Exact analytical quadratic inversion of the NRCS Curve Number equation solving for required rainfall depth P that produces runoff depth Q.",
    "HYD_HY_HORTON_FP": "Evaluates Horton's infiltration capacity rate f_p at time t.",
    "HYD_HY_HORTON_K": "Analytically isolates Horton's decay constant k from observed infiltration capacity f_p at time t.",

    # Structures, Spillways & Dissipators
    "HYD_ST_RECT_WEIR_001": "Computes discharge over a sharp-crested rectangular weir using Francis' formula with end contraction corrections for effective crest length.",
    "HYD_ST_VNOTCH_WEIR_001": "Determines discharge over a triangular V-notch sharp-crested weir as a function of notch opening angle theta and upstream head H.",
    "HYD_ST_BROAD_WEIR_001": "Calculates discharge across a broad-crested weir operating under critical flow condition over the horizontal weir crest.",
    "HYD_ST_PARSHALL_001": "Evaluates discharge through a standard Parshall flume operating under free-flow conditions as a power function of upstream head H_a.",
    "HYD_ST_ORIFICE_FREE_001": "Calculates free discharge Q through a sharp-edged circular or rectangular orifice into atmospheric pressure under total head H.",
    "HYD_ST_ORIFICE_SUB_001": "Evaluates discharge Q through a submerged orifice where the jet discharges below a downstream tailwater pool.",
    "HYD_ST_SLUICE_FREE_001": "Calculates free gravity discharge beneath a vertical sluice gate into atmosphere as a function of gate opening a and upstream depth y_1.",
    "HYD_ST_SLUICE_SUB_001": "Computes discharge beneath a submerged vertical sluice gate where tailwater depth produces downstream drowning.",
    "HYD_ST_OGEE_SPILLWAY_001": "Computes discharge Q over an ogee-crested overflow spillway based on USBR standard profile geometry, effective crest length L_e, and total design head H_e.",
    "HYD_ST_OGEE_COEFF_001": "Corrects the ogee spillway discharge coefficient C when operating at heads H_e differing from the design head H_o using the standard USBR power relation.",
    "HYD_ST_EFF_CREST_LEN_001": "Determines effective overflow spillway crest length L_e by applying pier and abutment end contraction coefficients to clear crest span L.",
    "HYD_ST_CHUTE_VELOCITY_001": "Calculates flow velocity V at the toe of a spillway chute from gross elevation drop Z_drop accounting for boundary friction and aeration head loss.",
    "HYD_ST_STILLING_BASIN_001": "Computes required length L_sb of a hydraulic jump stilling basin (USBR Type II, III, or IV) as a function of subcritical sequent depth y_2.",
    "HYD_ST_MORNING_GLORY_001": "Evaluates discharge Q over a circular shaft spillway (morning glory / bellmouth drop inlet) operating under free-surface weir control.",
    "HYD_ST_SIPHON_SPILLWAY_001": "Computes high-capacity discharge Q through a closed siphon spillway operating under full pipe vacuum priming across operating head difference H.",
    "HYD_ST_DROP_STRUCT_001": "Calculates supercritical flow depth y_1 at the toe of a vertical drop spillway based on Rand's empirical drop number formulation.",
    "HYD_ST_TAILWATER_001": "Evaluates river tailwater stage y_tw downstream of hydraulic structures using the standard power-law stage-discharge rating equation.",

    # Structures Inversions
    "HYD_ST_VNOTCH_Q": "Evaluates discharge Q through a sharp-crested triangular V-notch weir.",
    "HYD_ST_VNOTCH_H": "Inverts V-notch weir equation to solve for operating head H required to pass discharge Q.",
    "HYD_ST_OGEE_Q": "Evaluates discharge Q over an ogee overflow spillway crest.",
    "HYD_ST_OGEE_HE": "Inverts Ogee spillway equation to calculate head on crest H_e corresponding to discharge Q.",
    "HYD_ST_OGEE_LE": "Calculates required effective spillway crest length L_e to pass design flood discharge Q at total head H_e.",
    "HYD_ST_BASIN_LSB": "Computes stilling basin apron length L_sb from subcritical sequent depth y_2.",
    "HYD_ST_BASIN_Y2": "Inverts stilling basin design relation to determine allowable sequent depth y_2 for a fixed basin length L_sb.",

    # Groundwater & Aquifer Mechanics
    "HYD_GW_DARCY_1D_001": "Evaluates steady 1D groundwater flow discharge Q through porous media according to Darcy's linear law.",
    "HYD_GW_DARCY_FLUX_001": "Calculates Darcy flux (specific discharge) q = Q/A as the product of hydraulic conductivity K and hydraulic head gradient dh/dl.",
    "HYD_GW_THIEM_CONFINED_001": "Determines steady-state radial pumping discharge Q for a fully penetrating well in a confined aquifer using Thiem's equilibrium formula.",
    "HYD_GW_THIEM_UNCONFINED_001": "Calculates steady-state radial pumping discharge Q for a fully penetrating well in an unconfined aquifer incorporating Dupuit-Forchheimer parabolic head assumptions.",
    "HYD_GW_THEIS_001": "Computes transient drawdown s in a confined aquifer under unsteady non-equilibrium pumping using Theis' exponential integral well function W(u).",
    "HYD_GW_COOPER_JACOB_001": "Evaluates transient drawdown s using Cooper-Jacob logarithmic series truncation valid for small u (long pumping times or close observation radii).",

    # Groundwater Inversions
    "HYD_GW_DARCY_Q": "Evaluates steady Darcy seepage discharge Q through a saturated porous formation.",
    "HYD_GW_DARCY_K": "Inverts Darcy flow equation to calculate saturated hydraulic conductivity K from measured permeameter discharge Q and hydraulic gradient dh/dl.",
    "HYD_GW_THIEM_Q": "Evaluates radial pumping equilibrium discharge Q in a confined aquifer.",
    "HYD_GW_THIEM_T": "Inverts Thiem's equilibrium equation to determine confined aquifer transmissivity T from observation well drawdowns (h_2 - h_1)."
}


def generate_document():
    catalog_path = r"E:\python\Water_Resource_Library\hydrocivil\catalog\formula_catalog.json"
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    doc = Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Normal Style
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Calibri"
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(51, 51, 51)

    # -------------------------------------------------------------------------
    # COVER / HEADER TITLE
    # -------------------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(20)
    title_p.paragraph_format.space_after = Pt(6)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("PROJECT HYDROCIVIL")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(26)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(31, 78, 121)

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = sub_p.add_run("Master Engineering Formula Catalog & Computational Specification")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(15)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(89, 89, 89)

    # Meta banner
    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(24)
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = meta_p.add_run(
        f"Comprehensive Compendium of {len(catalog)} Mathematical Formulations Across 5 Engineering Pillars\n"
        "Engineered with Stacked Fractions, Explicit Inversions & High-Performance Rust Kernels"
    )
    run_meta.font.name = "Calibri"
    run_meta.font.size = Pt(10)
    run_meta.font.bold = True
    run_meta.font.color.rgb = RGBColor(46, 117, 182)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Group formulas by domain
    domain_order = [
        ("open_channel", "PILLAR 1: OPEN CHANNEL HYDRAULICS & SEDIMENT MECHANICS"),
        ("pipe_flow", "PILLAR 2: PRESSURIZED PIPE FLOW, NETWORKS & CULVERTS"),
        ("hydrology", "PILLAR 3: SURFACE WATER HYDROLOGY & WATERSHED MODELLING"),
        ("structures", "PILLAR 4: HYDRAULIC STRUCTURES, SPILLWAYS & DAMS"),
        ("groundwater", "PILLAR 5: SEEPAGE & SUBSURFACE GROUNDWATER HYDRAULICS")
    ]

    domains_map = {dom: [] for dom, _ in domain_order}
    for item in catalog:
        dom = item["domain"]
        if dom in domains_map:
            domains_map[dom].append(item)
        else:
            domains_map[dom] = [item]

    formula_counter = 1

    for dom_key, dom_title in domain_order:
        items = domains_map.get(dom_key, [])
        if not items:
            continue

        # Domain Heading 1
        h1 = doc.add_paragraph()
        h1.paragraph_format.space_before = Pt(26)
        h1.paragraph_format.space_after = Pt(8)
        h1.paragraph_format.keep_with_next = True
        run_h1 = h1.add_run(dom_title)
        run_h1.font.name = "Calibri"
        run_h1.font.size = Pt(16)
        run_h1.font.bold = True
        run_h1.font.color.rgb = RGBColor(31, 78, 121)

        # Thin rule under domain heading
        p_rule = doc.add_paragraph()
        p_rule.paragraph_format.space_after = Pt(14)
        r_rule = p_rule.add_run("—" * 60)
        r_rule.font.color.rgb = RGBColor(180, 198, 231)

        for item in items:
            fid = item["formula_id"]
            cname = item["canonical_name"]
            subdom = item["subdomain"]
            gov_eq = item["governing_equation"]
            lit_source = item["literature_source"]

            raw_latex = LATEX_MAP.get(fid, gov_eq)
            fn_sig = FUNCTION_SIGNATURES.get(fid, f"hydrocivil.{dom_key}.{cname}(...)")
            fn_desc = FUNCTION_DESCRIPTIONS.get(fid, f"Computes {cname.replace('_', ' ')} based on governing physical formulations.")

            # Heading for formula
            h2 = doc.add_paragraph()
            h2.paragraph_format.space_before = Pt(16)
            h2.paragraph_format.space_after = Pt(4)
            h2.paragraph_format.keep_with_next = True
            run_h2 = h2.add_run(f"{formula_counter}. {cname.replace('_', ' ').title()}  [{fid}]")
            run_h2.font.name = "Calibri"
            run_h2.font.size = Pt(12.5)
            run_h2.font.bold = True
            run_h2.font.color.rgb = RGBColor(46, 117, 182)

            formula_counter += 1

            # Subdomain & Scope
            p_sub = doc.add_paragraph()
            p_sub.paragraph_format.space_after = Pt(4)
            r_sub = p_sub.add_run(f"Domain: {dom_key.replace('_', ' ').title()} | Subdomain: {subdom.replace('_', ' ').title()} | Solver: {', '.join(item['solvers_supported']).title()}")
            r_sub.font.name = "Calibri"
            r_sub.font.size = Pt(9.5)
            r_sub.font.italic = True
            r_sub.font.color.rgb = RGBColor(120, 120, 120)

            # Function Call Box
            p_sig = doc.add_paragraph()
            p_sig.paragraph_format.space_after = Pt(6)
            r_sig_lbl = p_sig.add_run("HydroCivil Function: ")
            r_sig_lbl.font.bold = True
            r_sig_lbl.font.size = Pt(9.5)
            r_sig_val = p_sig.add_run(fn_sig)
            r_sig_val.font.name = "Consolas"
            r_sig_val.font.size = Pt(9.5)
            r_sig_val.font.color.rgb = RGBColor(160, 40, 40)

            # Function Description
            p_desc = doc.add_paragraph()
            p_desc.paragraph_format.space_after = Pt(8)
            r_desc = p_desc.add_run(fn_desc)
            r_desc.font.size = Pt(10)

            # Governing Equation Label
            p_eq_lbl = doc.add_paragraph()
            p_eq_lbl.paragraph_format.space_after = Pt(3)
            p_eq_lbl.paragraph_format.keep_with_next = True
            r_eq_lbl = p_eq_lbl.add_run("Governing Equation:")
            r_eq_lbl.font.bold = True
            r_eq_lbl.font.size = Pt(9.5)
            r_eq_lbl.font.color.rgb = RGBColor(31, 78, 121)

            # PROPER NATIVE WORD EQUATION BOX (WITH VERTICAL STACKED FRACTIONS)
            eq_list = raw_latex if isinstance(raw_latex, list) else [raw_latex]
            for eq_item in eq_list:
                p_math = doc.add_paragraph()
                p_math.paragraph_format.space_before = Pt(3)
                p_math.paragraph_format.space_after = Pt(6)
                p_math.alignment = WD_ALIGN_PARAGRAPH.CENTER
                try:
                    omml_element = latex_to_omml(eq_item)
                    p_math._p.append(omml_element)
                except Exception as e:
                    # Fallback to styled text if conversion fails
                    r_fallback = p_math.add_run(str(eq_item))
                    r_fallback.font.name = "Cambria Math"
                    r_fallback.font.size = Pt(11)
                    r_fallback.font.italic = True

            # Parameter Table
            param_headers = ["Parameter Name", "Symbol", "SI Units", "US Units", "Valid Bounds"]
            param_data = []
            for p in item["parameters"]:
                min_v = p.get("min")
                max_v = p.get("max")
                b_str = f"[{min_v if min_v is not None else '0.0'}, {max_v if max_v is not None else '∞'})"
                param_data.append([
                    p["name"].replace("_", " ").title(),
                    p["symbol"],
                    p["units_si"],
                    p["units_us"],
                    b_str
                ])

            table_p = doc.add_table(rows=1, cols=5)
            style_table(table_p, [2.2, 0.9, 1.1, 1.1, 1.2], param_headers, param_data)

            # Output Table if outputs exist
            if item.get("outputs"):
                out_headers = ["Output Quantity", "Symbol", "SI Units", "US Units"]
                out_data = []
                for o in item["outputs"]:
                    out_data.append([
                        o["name"].replace("_", " ").title(),
                        o["symbol"],
                        o["units_si"],
                        o["units_us"]
                    ])
                table_o = doc.add_table(rows=1, cols=4)
                style_table(table_o, [2.7, 1.1, 1.3, 1.4], out_headers, out_data)

            # Source Citation
            p_src = doc.add_paragraph()
            p_src.paragraph_format.space_before = Pt(4)
            p_src.paragraph_format.space_after = Pt(14)
            r_src_lbl = p_src.add_run("Literature Reference: ")
            r_src_lbl.font.bold = True
            r_src_lbl.font.size = Pt(9)
            r_src_lbl.font.color.rgb = RGBColor(89, 89, 89)
            r_src_val = p_src.add_run(lit_source)
            r_src_val.font.size = Pt(9)
            r_src_val.font.italic = True
            r_src_val.font.color.rgb = RGBColor(120, 120, 120)

    out_docx_path = r"E:\python\Water_Resource_Library\HydroCivil_Master_Formula_Catalog.docx"
    doc.save(out_docx_path)
    print(f"Successfully generated Master Formula Document: {out_docx_path}")
    print(f"Total equations processed into native Word formula boxes: {formula_counter - 1}")

if __name__ == "__main__":
    generate_document()
