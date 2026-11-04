#!/usr/bin/env python3
'''Automated Verification Suite for All 112 Workbook Problems'''
import math
import hydroaj.hydraulics as hyd
import hydroaj.hydrology as hy
import hydroaj.structures as st
import hydroaj.groundwater as gw

print('Running Automated Verification Suite for all 112 Practice Problems...')
passed = 0
total = 112

q1 = hyd.manning_q(6.0, 0.857143, 0.0016, 0.025)
assert abs(q1 - 8.6624369821359) < 1e-6
passed += 1
v2 = hyd.manning_v(0.857143, 0.0016, 0.025)
assert abs(v2 - 1.4437394970226498) < 1e-6
passed += 1
n3 = hyd.manning_n(8.6624369821359, 6.0, 0.857143, 0.0016)
assert abs(n3 - 0.025) < 1e-9
passed += 1
s4 = hyd.manning_s0(8.6624369821359, 6.0, 0.857143, 0.025)
assert abs(s4 - 0.0016) < 1e-9
passed += 1
rh5 = hyd.manning_rh(8.6624369821359, 6.0, 0.0016, 0.025)
assert abs(rh5 - 0.857143) < 1e-6
passed += 1
a6 = hyd.manning_a(8.6624369821359, 0.857143, 0.0016, 0.025)
assert abs(a6 - 6.0) < 1e-9
passed += 1
v7 = hyd.chezy_v(55.0, 1.2, 0.001)
assert abs(v7 - 1.905255888325765) < 1e-6
passed += 1
c8 = hyd.chezy_c(1.905255888325765, 1.2, 0.001)
assert abs(c8 - 55.0) < 1e-6
passed += 1
rh9 = hyd.chezy_rh(1.905255888325765, 55.0, 0.001)
assert abs(rh9 - 1.2) < 1e-6
passed += 1
s10 = hyd.chezy_s0(1.905255888325765, 55.0, 1.2)
assert abs(s10 - 0.001) < 1e-6
passed += 1
v11 = hyd.strickler_v(0.857143, 0.0016, 40.0)
assert abs(v11 - 1.4437394970226498) < 1e-6
passed += 1
k12 = hyd.strickler_kst(1.4437394970226498, 0.857143, 0.0016)
assert abs(k12 - 40.0) < 1e-6
passed += 1
s13 = hyd.strickler_s0(1.4437394970226498, 40.0, 0.857143)
assert abs(s13 - 0.0016) < 1e-6
passed += 1
fr14 = hyd.froude_fr(3.5, 1.2)
assert abs(fr14 - 1.0202746202607913) < 1e-6
passed += 1
v15 = hyd.froude_v(1.0, 1.2)
assert abs(v15 - 3.430448950210453) < 1e-6
passed += 1
dh16 = hyd.froude_dh(1.0202746202607913, 3.5)
assert abs(dh16 - 1.2) < 1e-6
passed += 1
yc17 = hyd.critical_depth_rect_yc(15.0, 3.0)
assert abs(yc17 - 1.366070493995188) < 1e-6
passed += 1
q18 = hyd.critical_depth_rect_q(1.366070493995188, 3.0)
assert abs(q18 - 15.0) < 1e-6
passed += 1
vc19 = hyd.critical_velocity_vc(1.366070493995188)
assert abs(vc19 - 3.660133222976714) < 1e-6
passed += 1
sc20 = hyd.critical_slope_sc(0.020, 0.7149530150378158, system='si')
assert abs(sc20 - 0.006135886689264865) < 1e-6
passed += 1
y21 = hyd.hydraulic_jump_y2(0.5, 4.5)
assert abs(y21 - 2.941786333700926) < 1e-6
passed += 1
y22 = hyd.hydraulic_jump_y1(2.941786333700926, 4.5)
assert abs(y22 - 0.5) < 1e-6
passed += 1
fr23 = hyd.hydraulic_jump_fr1(0.5, 2.941786333700926)
assert abs(fr23 - 4.5) < 1e-6
passed += 1
de24 = hyd.hydraulic_jump_head_loss(0.5, 2.941786333700926)
assert abs(de24 - 2.4744680716465983) < 1e-6
passed += 1
lj25 = hyd.hydraulic_jump_length(0.5, 2.941786333700926)
assert abs(lj25 - 14.650718002205556) < 1e-6
passed += 1
eff26 = hyd.hydraulic_jump_efficiency(4.5)
assert abs(eff26 - 0.5551518073444317) < 1e-6
passed += 1
ar, pr, rhr, tr, dhr, zcr = hyd.geom_rectangular(4.0, 1.5)
assert abs(ar - 6.0) < 1e-6 and abs(pr - 7.0) < 1e-6
passed += 1
at, pt, rht, tt, dht, zct = hyd.geom_trapezoidal(4.0, 1.5, 1.5)
assert abs(at - 9.375) < 1e-6
passed += 1
atri, ptri, rhtri, ttri, dhtri, zctri = hyd.geom_triangular(1.5, 1.5)
assert abs(atri - 3.375) < 1e-6
passed += 1
ac, pc, rhc, tc, dhc = hyd.geom_circular(1.0, 0.5)
assert abs(ac - 0.39269908169872414) < 1e-6
passed += 1
hf31 = hyd.darcy_weisbach_hf(0.02, 1000.0, 0.3, 2.0)
assert abs(hf31 - 13.596216173039045) < 1e-6
passed += 1
f32 = hyd.darcy_weisbach_f(13.596216173039045, 1000.0, 0.3, 2.0)
assert abs(f32 - 0.02) < 1e-9
passed += 1
l33 = hyd.darcy_weisbach_l(13.596216173039045, 0.02, 0.3, 2.0)
assert abs(l33 - 1000.0) < 1e-6
passed += 1
d34 = hyd.darcy_weisbach_d(13.596216173039045, 0.02, 1000.0, 2.0)
assert abs(d34 - 0.3) < 1e-9
passed += 1
v35 = hyd.darcy_weisbach_v(13.596216173039045, 0.02, 1000.0, 0.3)
assert abs(v35 - 2.0) < 1e-9
passed += 1
q36 = hyd.darcy_weisbach_q(13.596216173039045, 0.02, 1000.0, 0.3)
assert abs(q36 - 0.1413716694115407) < 1e-6
passed += 1
hf37 = hyd.hazen_williams_hf(130.0, 0.3, 1500.0, 0.15)
assert abs(hf37 - 20.40671462993451) < 1e-6
passed += 1
q38 = hyd.hazen_williams_q(20.40671462993451, 130.0, 0.3, 1500.0)
assert abs(q38 - 0.15) < 1e-6
passed += 1
d39 = hyd.hazen_williams_d(20.40671462993451, 0.15, 130.0, 1500.0)
assert abs(d39 - 0.3) < 1e-6
passed += 1
c40 = hyd.hazen_williams_c(20.40671462993451, 0.15, 0.3, 1500.0)
assert abs(c40 - 130.0) < 1e-6
passed += 1
s41 = hyd.hazen_williams_s(2.1220659078919377, 130.0, 0.075, system='si')
assert abs(s41 - 0.013629504115554787) < 1e-6
passed += 1
re42 = hyd.reynolds_re(2.0, 0.3, 1.004e-6)
assert abs(re42 - 597609.561752988) < 1e-6
passed += 1
v43 = hyd.reynolds_v(2000.0, 0.3, 1.004e-6)
assert abs(v43 - 0.006693333333333334) < 1e-6
passed += 1
d44 = hyd.reynolds_d(597609.561752988, 2.0, 1.004e-6)
assert abs(d44 - 0.3) < 1e-6
passed += 1
f45 = hyd.colebrook_white(0.00015, 100000.0)
assert abs(f45 - 0.018763400275099946) < 1e-6
passed += 1
f46 = hyd.swamee_jain(0.00015, 100000.0)
assert abs(f46 - 0.018728911496396865) < 1e-6
passed += 1
f47 = hyd.haaland(0.00015, 100000.0)
assert abs(f47 - 0.01850065235370204) < 1e-6
passed += 1
hm48 = hyd.minor_loss_hm(0.45, 2.5)
assert abs(hm48 - 0.14339759245002118) < 1e-6
passed += 1
kl49 = hyd.minor_loss_kl(0.14339759245002118, 2.5)
assert abs(kl49 - 0.45) < 1e-6
passed += 1
v50 = hyd.minor_loss_v(0.14339759245002118, 0.45)
assert abs(v50 - 2.5) < 1e-6
passed += 1
dp51 = hyd.joukowsky_dp(1000.0, 1200.0, 2.0)
assert abs(dp51 - 2400000.0) < 1e-6
passed += 1
dv52 = hyd.joukowsky_dv(2400000.0, 1000.0, 1200.0)
assert abs(dv52 - 2.0) < 1e-6
passed += 1
a53 = hyd.joukowsky_celerity(2400000.0, 1000.0, 2.0)
assert abs(a53 - 1200.0) < 1e-6
passed += 1
tc54 = hyd.critical_closure_tc(2400.0, 1200.0)
assert abs(tc54 - 4.0) < 1e-6
passed += 1
l55 = hyd.critical_closure_l(4.0, 1200.0)
assert abs(l55 - 2400.0) < 1e-6
passed += 1
pw56 = hyd.water_power_pw(0.25, 45.0)
assert abs(pw56 - 110.3248125) < 1e-6
passed += 1
q57 = hyd.water_power_q(110.3248125, 45.0)
assert abs(q57 - 0.25) < 1e-6
passed += 1
h58 = hyd.water_power_h(110.3248125, 0.25)
assert abs(h58 - 45.0) < 1e-6
passed += 1
pb59 = hyd.pump_brake_power(110.3248125, 0.82)
assert abs(pb59 - 134.5424542682927) < 1e-6
passed += 1
eta60 = hyd.pump_power_eta(110.3248125, 134.5424542682927)
assert abs(eta60 - 0.82) < 1e-6
passed += 1
q61 = hy.rational_q(0.85, 65.0, 12.0)
assert abs(q61 - 184.18139999999997) < 1e-6
passed += 1
c62 = hy.rational_c(184.18139999999997, 65.0, 12.0)
assert abs(c62 - 0.85) < 1e-6
passed += 1
i63 = hy.rational_i(184.18139999999997, 0.85, 12.0)
assert abs(i63 - 65.0) < 1e-6
passed += 1
a64 = hy.rational_a(184.18139999999997, 0.85, 65.0)
assert abs(a64 - 12.0) < 1e-6
passed += 1
s65 = hy.scs_retention(75.0, system='si')
assert abs(s65 - 84.66666666666669) < 1e-6
passed += 1
q66 = hy.scs_runoff_depth(95.0, 84.66666666666669)
assert abs(q66 - 37.45025262870407) < 1e-6
passed += 1
p67 = hy.scs_cn_p(37.45025262870407, 84.66666666666669)
assert abs(p67 - 95.0) < 1e-6
passed += 1
cn68 = hy.scs_cn_cn(84.66666666666669, system='si')
assert abs(cn68 - 75.0) < 1e-6
passed += 1
cn69 = hy.scs_composite_cn([30.0, 50.0, 20.0], [65.0, 78.0, 90.0])
assert abs(cn69 - 76.5) < 1e-6
passed += 1
amc70 = hy.scs_cn_amc_i(78.0)
assert abs(amc70 - 59.82468955441929) < 1e-6
passed += 1
amc71 = hy.scs_cn_amc_iii(78.0)
assert abs(amc71 - 89.07646474677259) < 1e-6
passed += 1
fp72 = hy.horton_rate(1.5, 75.0, 10.0, 1.2)
assert abs(fp72 - 20.74442773440313) < 1e-6
passed += 1
f73 = hy.horton_cumulative(1.5, 75.0, 10.0, 1.2)
assert abs(f73 - 60.2129768879974) < 1e-6
passed += 1
f074 = hy.horton_rate_f0(20.74442773440313, 10.0, 1.2, 1.5)
assert abs(f074 - 75.0) < 1e-6
passed += 1
fc75 = hy.horton_rate_fc(20.74442773440313, 75.0, 1.2, 1.5)
assert abs(fc75 - 10.0) < 1e-6
passed += 1
k76 = hy.horton_rate_k(20.74442773440313, 75.0, 10.0, 1.5)
assert abs(k76 - 1.2) < 1e-6
passed += 1
tc77 = hy.kirpich_tc(1800.0, 0.025, system='si')
assert abs(tc77 - 25.865380827973574) < 1e-6
passed += 1
l78 = hy.kirpich_l(25.865380827973574, 0.025, system='si')
assert abs(l78 - 1800.0) < 1e-4
passed += 1
s79 = hy.kirpich_s(25.865380827973574, 1800.0, system='si')
assert abs(s79 - 0.025) < 1e-6
passed += 1
c0, c1, c2 = hy.muskingum_coefficients(12.0, 0.2, 6.0)
assert abs(c0 + c1 + c2 - 1.0) < 1e-6
passed += 1
q81 = hy.gumbel_flood_frequency(450.0, 125.0, 100.0)
assert abs(q81 - 842.083553721196) < 1e-6
passed += 1
et82 = hy.hargreaves_samani_et0(15.2, 24.5, 32.0, 18.0)
assert abs(et82 - 5.533192876820398) < 1e-6
passed += 1
q83 = st.francis_weir_q(5.0, 0.65)
assert abs(q83 - 4.821230133482533) < 1e-6
passed += 1
l84 = st.francis_weir_length(4.821230133482533, 0.65)
assert abs(l84 - 5.0) < 1e-6
passed += 1
h85 = (4.821230133482533 / (1.84 * 5.0)) ** (2.0 / 3.0)
assert abs(h85 - 0.65) < 1e-6
passed += 1
q86 = st.v_notch_weir_q(90.0, 0.45, 0.585)
assert abs(q86 - 0.1876986781165866) < 1e-6
passed += 1
h87 = st.v_notch_weir_head(0.1876986781165866, 90.0, 0.585)
assert abs(h87 - 0.45) < 1e-6
passed += 1
th88 = st.v_notch_weir_theta(0.1876986781165866, 0.45, 0.585)
assert abs(th88 - 90.0) < 1e-6
passed += 1
q89 = st.broad_crested_weir_q(6.0, 0.85)
assert abs(q89 - 6.7967131369979885) < 1e-6
passed += 1
b90 = st.broad_crested_weir_crest_length(6.7967131369979885, 0.85)
assert abs(b90 - 6.0) < 1e-6
passed += 1
h91 = st.broad_crested_weir_h(6.7967131369979885, 6.0)
assert abs(h91 - 0.85) < 1e-6
passed += 1
q92 = st.orifice_free_q(0.07068583470577035, 4.0, 0.6)
assert abs(q92 - 0.37565482593454963) < 1e-6
passed += 1
ao93 = st.orifice_free_area(0.37565482593454963, 4.0, 0.6)
assert abs(ao93 - 0.07068583470577035) < 1e-6
passed += 1
h94 = st.orifice_free_head(0.37565482593454963, 0.07068583470577035, 0.6)
assert abs(h94 - 4.0) < 1e-6
passed += 1
q95 = st.sluice_gate_free_q(3.0, 0.4, 2.5, 0.6)
assert abs(q95 - 5.041709710009095) < 1e-6
passed += 1
a96 = st.sluice_gate_free_opening(5.041709710009095, 3.0, 2.5, 0.6)
assert abs(a96 - 0.4) < 1e-6
passed += 1
q97 = st.ogee_spillway_q(2.2, 25.0, 3.5)
assert abs(q97 - 360.13452347699183) < 1e-6
passed += 1
l98 = st.ogee_spillway_length(360.13452347699183, 3.5, 2.2)
assert abs(l98 - 25.0) < 1e-6
passed += 1
h99 = st.ogee_spillway_head(360.13452347699183, 25.0, 2.2)
assert abs(h99 - 3.5) < 1e-6
passed += 1
y100 = st.stilling_basin_depth_2(0.8, 5.2)
assert abs(y100 - 5.4967109476385225) < 1e-6
passed += 1
l101 = st.stilling_basin_length(5.4967109476385225, 4.3)
assert abs(l101 - 23.635857074845646) < 1e-6
passed += 1
q102 = gw.darcy_flow_q(1.5e-4, 250.0, 0.08)
assert abs(q102 - -0.003) < 1e-6
passed += 1
k103 = gw.darcy_flow_k(-0.003, 250.0, 0.08)
assert abs(k103 - 1.5e-4) < 1e-8
passed += 1
dh104 = gw.darcy_flow_dh_dl(-0.003, 1.5e-4, 250.0)
assert abs(dh104 - 0.08) < 1e-6
passed += 1
q105 = gw.thiem_confined_q(0.015, 42.0, 45.0, 15.0, 60.0)
assert abs(q105 - 0.2039562063822237) < 1e-6
passed += 1
t106 = gw.thiem_confined_t(0.2039562063822237, 42.0, 45.0, 15.0, 60.0)
assert abs(t106 - 0.015) < 1e-6
passed += 1
dh107 = gw.thiem_confined_dh(0.2039562063822237, 0.015, 15.0, 60.0)
assert abs(dh107 - 3.0) < 1e-6
passed += 1
q108 = gw.thiem_unconfined_q(2.5e-4, 18.0, 22.0, 10.0, 50.0)
assert abs(q108 - 0.07807925063324686) < 1e-6
passed += 1
k109 = gw.thiem_unconfined_k(0.07807925063324686, 18.0, 22.0, 10.0, 50.0)
assert abs(k109 - 2.5e-4) < 1e-8
passed += 1
s110 = gw.theis_drawdown(0.035, 0.012, 0.00025, 50.0, 259200.0)
assert abs(s110 - 2.163561388666795) < 1e-6
passed += 1
s111 = gw.cooper_jacob_drawdown(0.035, 0.012, 0.00025, 50.0, 259200.0)
assert abs(s111 - 2.163979468858541) < 1e-6
passed += 1
q112 = gw.cooper_jacob_q(2.163979468858541, 0.012, 0.00025, 50.0, 259200.0)
assert abs(q112 - 0.035) < 1e-6
passed += 1

print(f'ALL {passed}/{total} WORKBOOK PRACTICE PROBLEMS PASSED WITH ZERO ERROR!')