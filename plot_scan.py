#!/usr/bin/env python3
r"""
Script to analyse scan results from iteration .csv files.
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
from src.my_utils import get_convergence_data, read_QFM_output_files

parent_path = str(Path(__file__).parent.resolve())
scan_name = 'results/QH_QFM_test2/'
os.chdir(parent_path)
rootdir  = os.path.join(parent_path, scan_name)

figsize_sidebyside = (10, 4.5)
# Make sure that the grid is not plotted over the data.
plt.rc('axes', axisbelow=True)

# Get convergence data per design point
ts_data, ss_data = get_convergence_data(rootdir)

# Objective to plot
objectives_legend = ['J_total', 'J_Quadratic_Flux', 'J_Length', 'J_C-C', 'J_Curvature', 'J_Length_penalty', 'J_MSC', 'J_ALS', 'J_Quasisymmetry', 'J_Aspect'] # Jiota excluded because not in objective!
ss_objectives = ['J', 'Jf', 'J_length', 'J_CC', 'J_CURVATURE', 'J_LENGTH_PENALTY', 'J_MSC', 'J_ALS', 'Jquasisymmetry', 'Jaspect'] # Jiota excluded because not in objective!
ts_objectives = ['J', 'Jf', 'J_length', 'J_CC', 'J_CURVATURE', 'J_LENGTH_PENALTY', 'J_MSC', 'J_ALS']

ss_X = []
ss_f_QS = []
ss_f_QF = []
ss_CC = []
ss_f_A = []
ss_msc = []
ss_curv = []
ss_J_list = [[] for _ in range(len(ss_objectives))] 
ts_X = []
ts_f_QS = []
ts_f_QF = []
ts_CC = []
ts_f_A = []
ts_msc = []
ts_curv = []
ts_J_list = [[] for _ in range(len(ss_objectives))] 

two_stage_quasisymmetry = 0.0018388705086775513 # manually extracted the values for BenchmarkScan_1 (same for BenchmarkScan_2 and 3) from their respective output.txt. This is independent from n_coils for the two stage approach.
two_stage_Jiota = -1.1398587496646777
two_stage_aspect_ratio = 7.000556095458935 # manually extracted the values for BenchmarkScan_1 (same for BenchmarkScan_2 and 3) from their respective output.txt. This is independent from n_coils for the two stage approach.
two_stage_J_aspect_ratio = 0.0235816763385 # computed by sqrt(aspectratio-7)

# Unpack runtime data
for dp in ts_data:
    ts_X.append(dp['ncoils'])
    ts_f_QS.append(two_stage_quasisymmetry)  
    ts_f_A.append(two_stage_aspect_ratio)  
    ts_f_QF.append(float(dp['Jf']))
    ts_CC.append(float(dp['C-C-Sep']))
    ts_msc.append(float(dp['msc'])/dp['ncoils']) # convert to average msc by dividing over ncoils
    ts_curv.append(float(dp['curvatures'])/dp['ncoils']) # convert to average by dividing over ncoils

    for i in range(len(ts_objectives)):
        ts_J_list[i].append(float(dp[ts_objectives[i]])) # to plot any objective
        # Manually add plasma surface properties
    ts_J_list[len(ss_objectives)-2].append(two_stage_quasisymmetry)
    # ts_J_list[len(ss_objectives)-2].append(two_stage_Jiota)
    ts_J_list[len(ss_objectives)-1].append(two_stage_J_aspect_ratio)

    if dp['ncoils'] == 3:
        benchmark_ts_QS = two_stage_quasisymmetry
        benchmark_ts_QF = float(dp['Jf'])

for dp in ss_data:
    ss_X.append(dp['ncoils'])
    ss_f_QS.append(float(dp['Jquasisymmetry']))
    ss_f_A.append(float(dp['Jaspect'])) # reconstruct aspect ratio, assuming it is always pushed above the target.
    ss_f_QF.append(float(dp['Jf']))
    ss_CC.append(float(dp['C-C-Sep']))
    ss_msc.append(float(dp['msc'])/dp['ncoils']) # convert to average msc by dividing over ncoils
    ss_curv.append(float(dp['curvatures'])/dp['ncoils']) # convert to average by dividing over ncoils

    J_list = [[] for _ in range(len(ss_objectives))]
    for i in range(len(ss_objectives)):
        ss_J_list[i].append(float(dp[ss_objectives[i]])) # to plot any objective

    if dp['ncoils'] == 3:
        benchmark_ss_QS = float(dp['Jquasisymmetry'])
        benchmark_ss_QF = float(dp['Jf'])


## Plot QS and QF over scan range
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize_sidebyside, tight_layout=True, sharey=True)

ax1.set_title('Single stage')
ax1.set_yscale('log')
ax1.set_xlabel('# coils')
ax1.set_ylabel('Objective')
ax1.grid(color='0.1', linestyle='-.', linewidth=.5)
ax1.tick_params(which='both', direction="in")

ax2.set_title('Two stage')
ax2.set_yscale('log')
ax2.set_xlabel('# coils')
# ax2.set_ylabel('Objective') # captured by shared axis
ax2.grid(color='0.3', linestyle='-.', linewidth=.5)
ax2.tick_params(which='both', direction="in")

# Scatter the data
ax1.scatter(ss_X,ss_f_QS, marker='x', color='k')
ax1.scatter(ss_X,ss_f_QF, marker='+', color='k')
ax2.scatter(ts_X,ts_f_QS, marker='x', color='k')
ax2.scatter(ts_X,ts_f_QF, marker='+', color='k')

# Put legend to right side of righternmost plot
ax2.legend(['J_Quasisymmetry', 'J_Quadratic_Flux'], loc='center left', bbox_to_anchor=(1, 0.5))

fig_name = 'scan_QS-QF.png'
fig_path = rootdir + fig_name
fig.savefig(fig_path)

# ## benchmark plot
# fig2, ax2 = plt.subplots()

# jorge_ts_QS = 2.0e-3
# jorge_ts_QF = 3.1e-5
# jorge_ss_QS = 1.3e-2
# jorge_ss_QF = 8.3e-6
# ax2.scatter(3,jorge_ss_QS, marker='x', color='0.8')
# ax2.scatter(3,jorge_ss_QF, marker='o', color='0.8')
# ax2.scatter(3,jorge_ts_QS, marker='x', color='tab:orange')
# ax2.scatter(3,jorge_ts_QF, marker='o', color='tab:orange')
# ax2.scatter(3,benchmark_ss_QS, marker='x', color='0')
# ax2.scatter(3,benchmark_ss_QF, marker='o', color='0')
# ax2.scatter(3,benchmark_ts_QS, marker='x', color='tab:red')
# ax2.scatter(3,benchmark_ts_QF, marker='o', color='tab:red')

# ax2.legend(['Single stage QS', 'Single stage QF', 'Two stage QS', 'Two stage QF', 'Jorge Single stage QS', 'Jorge Single stage QF', 'Jorge Two stage QS', 'Jorge Two stage QF'], loc='center left', bbox_to_anchor=(1, 0.5))


# ax2.set_yscale('log')
# ax2.set_xlabel('# coils')
# ax2.set_ylabel('Objective')
# fig2.tight_layout()

# fig_name = 'benchmark_plot.png'
# fig_path = rootdir + fig_name
# fig2.savefig(fig_path)

# ## Objectives plotting
# for i in range(len(ss_objectives)):
#     figi, axi = plt.subplots(tight_layout=True)
#     axi.scatter(ss_X,ss_J_list[i], marker='x', color='0')
#     axi.scatter(ts_X,ts_J_list[i], marker='x', color='tab:red')
#     axi.legend(['Single stage', 'Two stage'], loc='center left', bbox_to_anchor=(1, 0.5))

#     axi.set_yscale('log')
#     axi.set_xlabel('# coils')
#     axi.set_ylabel(objectives_legend[i])
#     axi.grid(color='0.3', linestyle='-.', linewidth=.5)
#     axi.tick_params(which='both', direction="in")

#     fig_name = 'Scan_' + objectives_legend[i]  +'.png'
#     fig_path = rootdir + fig_name
#     figi.savefig(fig_path)

# ## Objectives plotting
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize_sidebyside, tight_layout=True, sharey=True)

# # Exclude total J to make marker color black. (should be done with a proper colormap)
# ax1.scatter(ss_X,ss_J_list[0], marker='x', color='k')
# ax2.scatter(ts_X,ts_J_list[0], marker='x', color='k')
# for i in range(len(ss_objectives)-1): #Make length one shorter to exclude scatter of total J 
#     ax1.scatter(ss_X,ss_J_list[i+1])
#     ax2.scatter(ts_X,ts_J_list[i+1])
# # Scatter J marker again to put it on top. Workaround to easily make sure legend is still right.
# ax1.scatter(ss_X,ss_J_list[0], marker='x', color='k')
# ax2.scatter(ts_X,ts_J_list[0], marker='x', color='k')

# ax1.set_title('Single stage')
# ax1.set_yscale('log')
# ax1.set_xlabel('# coils')
# ax1.set_ylabel('Objective')
# ax1.grid(color='0.1', linestyle='-.', linewidth=.5)
# ax1.tick_params(which='both', direction="in")

# # ax1.legend(ss_objectives, loc='center left', bbox_to_anchor=(1, 0.5)) # Can be excluded, as colormap is the same for both subplots

# ax2.set_title('Two stage')
# ax2.set_yscale('log')
# ax2.set_xlabel('# coils')
# # ax2.set_ylabel('Objective') # captured by shared axis
# ax2.grid(color='0.3', linestyle='-.', linewidth=.5)
# ax2.tick_params(which='both', direction="in")

# ax2.legend(objectives_legend, loc='center left', bbox_to_anchor=(1, 0.5))

# fig_name = 'Scan_objectives.png'
# fig_path = rootdir + fig_name
# fig.savefig(fig_path)

# # ## Plot proof that coils are in eachothers way
# fig, (ax1,ax2) = plt.subplots(1, 2, figsize=figsize_sidebyside, tight_layout=True)

# # Plot correct constraint value
# if scan_name == 'results/QH_BenchmarkScan_3/':
#     Coil_constraint_value = 0.15
# elif scan_name == 'results/QH_BenchmarkScan_2/':
#     Coil_constraint_value = 0.08
# else:
#     Coil_constraint_value = 0.08
#     print('Coil_constraint_value = 0.08, is used may not be correct.')

# # Actual coil-coil distances
# ax1.scatter(ss_X,ss_CC, marker='x', color='0')
# ax1.scatter(ts_X,ts_CC, marker='x', color='tab:red')
# ax1.axhline(y=Coil_constraint_value, color='k', linestyle='--')
# ax1.set_xlabel('# coils')
# ax1.set_ylabel('d_min [m]')
# ax1.set_title('Minimum coil-coil distance')

# # Actual msc
# ax2.scatter(ss_X,ss_msc, marker='x', color='0')
# ax2.scatter(ts_X,ts_msc, marker='x', color='tab:red')
# ax2.axhline(y=10, color='k', linestyle='--')
# ax2.legend(['Single stage', 'Two stage', 'Constraint value'], loc='center left', bbox_to_anchor=(1, 0.5))
# ax2.set_xlabel('# coils')
# ax2.set_ylabel('unit?')
# ax2.set_title('Maximum coil mean square curvature')


# fig_name = 'scan_coil_problems.png'
# fig_path = rootdir + fig_name
# fig.savefig(fig_path)
# # fig1.show()

## QFM plot
# Extract QFM data
QFM_dict = read_QFM_output_files(rootdir)

fig, ax = plt.subplots(tight_layout=True)

for key in QFM_dict:
    ncoils, ss_QFM_QS, ts_QFM_QS = QFM_dict[key]
    ax.scatter(ncoils,ss_QFM_QS, marker='x', color='0')
    ax.scatter(ncoils,ts_QFM_QS, marker='x', color='tab:red')
ax.legend(['Single stage', 'Two stage'], loc='center left', bbox_to_anchor=(1, 0.5))
ax.set_xlabel('# coils')
ax.set_ylabel('QFM quasisymmetry')
ax.set_yscale('log')

# ax.set_title('Maximum coil mean square curvature')

fig_name = 'scan_QFM.png'
fig_path = rootdir + fig_name
fig.savefig(fig_path)

print('Finished plotting')