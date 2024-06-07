#!/usr/bin/env python3
r"""
Data processing utils
"""

import os
import csv
import re

def extract_ncoils_from_path(path):
    # Define the regular expression pattern to match ncoils value
    pattern = r'ncoils(\d+)'
    
    # Use re.search to find the pattern in the path
    match = re.search(pattern, path)
    
    if match:
        # Extract and return the ncoils value as an integer
        return int(match.group(1))
    else:
        # Return None if the pattern doesn't match
        return None

def extract_last_row_as_dict(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        last_row = None
        for row in reader:
            last_row = row
        return last_row

def get_convergence_data(rootdir):
    """
    Read all .csv files in the root directory and subfolders. Extract the design point from the last row of the csv. Put into an (unordered) array containing all design points, separated by both optimisation approaches..
    """

    ts_data = []
    ss_data = []

    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith("output_stage2_max_mode_3.csv"):
                csv_file_path = os.path.join(subdir, file)
                ts_design_point = extract_last_row_as_dict(csv_file_path)
                ncoils = extract_ncoils_from_path(subdir)                
                ts_design_point.update({
                    "ncoils":ncoils, 
                    "rundir":subdir,
                    "opt_type":'two_stage',
                    })
                ts_data.append(ts_design_point)

            elif file.endswith("output_max_mode_3.csv"):
                csv_file_path = os.path.join(subdir, file)
                ss_design_point = extract_last_row_as_dict(csv_file_path)
                ncoils = extract_ncoils_from_path(subdir)

                ss_design_point.update({
                    "ncoils":ncoils, 
                    "rundir":subdir,
                    "opt_type":'single_stage',
                    })
                ss_data.append(ss_design_point)

    return ts_data, ss_data

# overlapping functionality with extract_ncoils_from_path... this is taken from plot.py
def find_ncoils(string):
    parts = string.split("_")
    for part in parts:
        if part[:6] == "ncoils":
            return int(part[6:])

def read_QFM_output_files(parent_dir):
    output_dict = {}
    # ss_QFM_QS = []
    # ts_QFM_QS = []
    # Loop through all subdirectories of the parent directory
    for subdir in os.listdir(parent_dir):
        subdir_path = os.path.join(parent_dir, subdir)
        if os.path.isdir(subdir_path):
            ss_file_path = os.path.join(subdir_path, 'output', 'output_QFM_qs.txt')
            ts_file_path = os.path.join(subdir_path, 'output', 'output_QFM_qs_stage12.txt')

            # Find QFM QS from single stage output file
            if os.path.isfile(ss_file_path):
                with open(ss_file_path, 'r') as file:
                    content = file.read()
                    ss_QFM_QS = float(content.split(':')[1].strip())

            # Find QFM QS from two stage output file
            if os.path.isfile(ts_file_path):
                with open(ts_file_path, 'r') as file:
                    content = file.read()
                    ts_QFM_QS = float(content.split(':')[1].strip())

            ncoils = find_ncoils(subdir_path)

            output_dict[subdir] = [ncoils, ss_QFM_QS, ts_QFM_QS]

    return output_dict


