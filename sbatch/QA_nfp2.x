#!/bin/bash

#SBATCH -N 4
#SBATCH -n 25
#SBATCH -A FUA36_OHARS
#SBATCH -p skl_fua_prod
#SBATCH --mem=160000 
#SBATCH --time 24:00:00
#SBATCH --job-name=QAnfp2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=rogerio.jorge@tecnico.ulisboa.pt
cd /marconi_scratch/userexternal/rjorge00/single_stage_optimization

mkdir -p outputs

nfp=2
for ncoils in {2,3,4}; do \
    for len in {4.0,4.5,5.0,5.5}; do \
        mpirun -np 25 ./main.py QA --MAXITER_stage_1 20 --MAXITER_stage_2 500 --MAXITER_single_stage 500 max_modes 2 --ncoils $ncoils --lengthbound $len --vmec_input_start input.nfp${nfp}_QA_optimized > outputs/QA_nfp${nfp}_length${len}_${ncoils}coils.txt &
    done
    wait
done
wait

