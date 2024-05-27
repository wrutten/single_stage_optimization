#!/usr/bin/env python3
r"""
Script to analyse scan results from iteration .csv files.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.colors as cm

from src.my_utils import get_convergence_data


parent_path = str(Path(__file__).parent.resolve())
scan_name = 'results/BenchmarkScan_1/'
os.chdir(parent_path)
rootdir  = os.path.join(parent_path, scan_name)

# Get convergence data per design point
ts_data, ss_data = get_convergence_data(rootdir)


ss_X = []
ss_f_QS = []
ss_f_QF = []
ts_X = []
ts_f_QS = []
ts_f_QF = []

# Process data
two_stage_quasisymmetry = 0.0018388705086775513 # manually extracted the values for BenchmarkScan_1 from their respective output.txt. This is independent from n_coils for the two stage approach.
for dp in ts_data:
    ts_X.append(dp['ncoils'])
    ts_f_QS.append(two_stage_quasisymmetry)    
    ts_f_QF.append(float(dp['Jf']))
    if dp['ncoils'] == 3:
        benchmark_ts_QS = two_stage_quasisymmetry
        benchmark_ts_QF = float(dp['Jf'])

for dp in ss_data:
    ss_X.append(dp['ncoils'])
    ss_f_QS.append(float(dp['Jquasisymmetry']))
    ss_f_QF.append(float(dp['Jf']))
    if dp['ncoils'] == 3:
        benchmark_ss_QS = float(dp['Jquasisymmetry'])
        benchmark_ss_QF = float(dp['Jf'])
        print(True)


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