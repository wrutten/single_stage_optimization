#!/usr/bin/env python3
r"""
Script to analyse scan results from iteration .csv files.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.colors as cm
import numpy as np
from src.my_utils import get_convergence_data


parent_path = str(Path(__file__).parent.resolve())
scan_name = 'results/QH_BenchmarkScan_2/'
os.chdir(parent_path)
rootdir  = os.path.join(parent_path, scan_name)

# Get convergence data per design point
ts_data, ss_data = get_convergence_data(rootdir)


ss_X = []
ss_f_QS = []
ss_f_QF = []
ss_CC = []
ss_f_A = []
ss_msc = []
ss_curv = []
ss_J = []
ts_X = []
ts_f_QS = []
ts_f_QF = []
ts_CC = []
ts_f_A = []
ts_msc = []
ts_curv = []
ts_J = []
# index,Nfeval,J,Jf,J_length,J_CC,J_CURVATURE,J_LENGTH_PENALTY,J_MSC,J_ALS,Lengths,curvatures,msc,B.n,C-C-Sep

# Process data
two_stage_quasisymmetry = 0.0018388705086775513 # manually extracted the values for BenchmarkScan_1 (same for BenchmarkScan_2) from their respective output.txt. This is independent from n_coils for the two stage approach.
two_stage_aspect_ratio = 7.000556095458935 # manually extracted the values for BenchmarkScan_1 (same for BenchmarkScan_2) from their respective output.txt. This is independent from n_coils for the two stage approach.
for dp in ts_data:
    ts_X.append(dp['ncoils'])
    ts_f_QS.append(two_stage_quasisymmetry)  
    ts_f_A.append(two_stage_aspect_ratio)  
    ts_f_QF.append(float(dp['Jf']))
    ts_CC.append(float(dp['C-C-Sep']))
    ts_msc.append(float(dp['msc'])/dp['ncoils']) # convert to average msc by dividing over ncoils
    ts_curv.append(float(dp['curvatures'])/dp['ncoils']) # convert to average by dividing over ncoils
    ts_J.append(float(dp['J'])) # to plot any objective

    if dp['ncoils'] == 3:
        benchmark_ts_QS = two_stage_quasisymmetry
        benchmark_ts_QF = float(dp['Jf'])

for dp in ss_data:
    ss_X.append(dp['ncoils'])
    ss_f_QS.append(float(dp['Jquasisymmetry']))
    ss_f_A.append(np.sqrt(float(dp['Jaspect']))+7) # reconstruct aspect ratio, assuming it is always pushed above the target.
    ss_f_QF.append(float(dp['Jf']))
    ss_CC.append(float(dp['C-C-Sep']))
    ss_msc.append(float(dp['msc'])/dp['ncoils']) # convert to average msc by dividing over ncoils
    ss_curv.append(float(dp['curvatures'])/dp['ncoils']) # convert to average by dividing over ncoils
    ss_J.append(float(dp['J'])) # to plot any objective

    if dp['ncoils'] == 3:
        benchmark_ss_QS = float(dp['Jquasisymmetry'])
        benchmark_ss_QF = float(dp['Jf'])


# Plot QS and QF over scan range
fig1, ax1 = plt.subplots()
ax1.scatter(ss_X,ss_f_QS, marker='x', color='0')
ax1.scatter(ss_X,ss_f_QF, marker='o', color='0')
ax1.scatter(ts_X,ts_f_QS, marker='x', color='tab:red')
ax1.scatter(ts_X,ts_f_QF, marker='o', color='tab:red')

ax1.legend(['Single stage QS', 'Single stage QF', 'Two stage QS', 'Two stage QF', 'Jorge Single stage QS'], loc='center left', bbox_to_anchor=(1, 0.5))


ax1.set_yscale('log')
ax1.set_xlabel('# coils')
ax1.set_ylabel('value')
fig1.tight_layout()

fig_name = 'scan_QS-QF.png'
fig_path = rootdir + fig_name
fig1.savefig(fig_path)
# fig1.show()

## benchmark plot
fig2, ax2 = plt.subplots()

jorge_ts_QS = 2.0e-3
jorge_ts_QF = 3.1e-5
jorge_ss_QS = 1.3e-2
jorge_ss_QF = 8.3e-6
ax2.scatter(3,jorge_ss_QS, marker='x', color='0.8')
ax2.scatter(3,jorge_ss_QF, marker='o', color='0.8')
ax2.scatter(3,jorge_ts_QS, marker='x', color='tab:orange')
ax2.scatter(3,jorge_ts_QF, marker='o', color='tab:orange')
ax2.scatter(3,benchmark_ss_QS, marker='x', color='0')
ax2.scatter(3,benchmark_ss_QF, marker='o', color='0')
ax2.scatter(3,benchmark_ts_QS, marker='x', color='tab:red')
ax2.scatter(3,benchmark_ts_QF, marker='o', color='tab:red')

ax2.legend(['Single stage QS', 'Single stage QF', 'Two stage QS', 'Two stage QF', 'Jorge Single stage QS', 'Jorge Single stage QF', 'Jorge Two stage QS', 'Jorge Two stage QF'], loc='center left', bbox_to_anchor=(1, 0.5))


ax2.set_yscale('log')
ax2.set_xlabel('# coils')
ax2.set_ylabel('value')
fig2.tight_layout()

fig_name = 'benchmark_plot.png'
fig_path = rootdir + fig_name
fig2.savefig(fig_path)

## Plot C-C distance
fig3, ax3 = plt.subplots()
ax3.scatter(ss_X,ss_CC, marker='x', color='0')
ax3.scatter(ts_X,ts_CC, marker='x', color='tab:red')

ax3.legend(['Single stage', 'Two stage'], loc='center left', bbox_to_anchor=(1, 0.5))
ax3.axhline(y=0.08, color='k', linestyle='--')

# ax3.set_yscale('log')
ax3.set_xlabel('# coils')
ax3.set_ylabel('CC-sep [m?]')
fig3.tight_layout()

fig_name = 'scan_CC-sep.png'
fig_path = rootdir + fig_name
fig3.savefig(fig_path)
# fig1.show()

## Plot Aspect ratio
fig4, ax4 = plt.subplots()
ax4.scatter(ss_X,ss_f_A, marker='x', color='0')
ax4.scatter(ts_X,ts_f_A, marker='x', color='tab:red')

ax4.legend(['Single stage', 'Two stage'], loc='center left', bbox_to_anchor=(1, 0.5))
ax4.axhline(y=7, color='k', linestyle='--')

# ax4.set_yscale('log')
ax4.set_xlabel('# coils')
ax4.set_ylabel('Aspect ratio')
fig4.tight_layout()

fig_name = 'scan_aspect_ratio.png'
fig_path = rootdir + fig_name
fig4.savefig(fig_path)
# fig1.show()

## Plot msc
fig5, ax5 = plt.subplots()
ax5.scatter(ss_X,ss_msc, marker='x', color='0')
ax5.scatter(ts_X,ts_msc, marker='x', color='tab:red')

ax5.legend(['Single stage', 'Two stage'], loc='center left', bbox_to_anchor=(1, 0.5))
ax5.axhline(y=10, color='k', linestyle='--')

# ax5.set_yscale('log')
ax5.set_xlabel('# coils')
ax5.set_ylabel('Mean square curvature')
fig5.tight_layout()

fig_name = 'scan_msc.png'
fig_path = rootdir + fig_name
fig5.savefig(fig_path)
# fig1.show()

## Plot curvatures
fig5, ax5 = plt.subplots()
ax5.scatter(ss_X,ss_curv, marker='x', color='0')
ax5.scatter(ts_X,ts_curv, marker='x', color='tab:red')

ax5.legend(['Single stage', 'Two stage'], loc='center left', bbox_to_anchor=(1, 0.5))
ax5.axhline(y=10, color='k', linestyle='--')

# ax5.set_yscale('log')
ax5.set_xlabel('# coils')
ax5.set_ylabel('Max curvature')
fig5.tight_layout()

fig_name = 'scan_curvatures.png'
fig_path = rootdir + fig_name
fig5.savefig(fig_path)
# fig1.show()

## Plot curvatures
fig5, ax5 = plt.subplots()
ax5.scatter(ss_X,ss_J, marker='x', color='0')
ax5.scatter(ts_X,ts_J, marker='x', color='tab:red')

ax5.legend(['Single stage', 'Two stage'], loc='center left', bbox_to_anchor=(1, 0.5))

ax5.set_yscale('log')
ax5.set_xlabel('# coils')
ax5.set_ylabel('J')
fig5.tight_layout()

fig_name = 'scan_J.png'
fig_path = rootdir + fig_name
fig5.savefig(fig_path)
# fig1.show()

print('Finished plotting')