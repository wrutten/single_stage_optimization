
An attempt was made to run QFM analysis with varying parameters for the new benchmark run with coilweight 7e3.
Unfortunately, only the first few runs were able to get VMEC to converge. QFM surface was not necessarily converged for these runs, making results questionable.

echo "----------------- Starting run 0 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 0" --mpol 3 --ntor 3
echo "----------------- Starting run 1 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 1" --mpol 4 --ntor 4
echo "----------------- Starting run 2 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 2" --mpol 5 --ntor 5
echo "----------------- Starting run 3 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 3" --mpol 6 --ntor 6
echo "----------------- Starting run 4 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 4" --mpol 7 --ntor 7
echo "----------------- Starting run 5 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 5" --mpol 9 --ntor 9
echo "----------------- Starting run 6 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 6" --mpol 11 --ntor 11
echo "----------------- Starting run 7 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 7" --mpol 12 --ntor 12
echo "----------------- Starting run 8 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 8" --mpol 13 --ntor 13
echo "----------------- Starting run 9 --------------------"
python plot.py --results_folder "QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3 copy 9" --mpol 15 --ntor 15

mpol=5,ntor=5 provided best results, and was investigated further. Also by changing the QFM surface max iterations, such that it actually converged.
A good run was found in results/QH_BenchmarkQFMScan/QH_Stage123_Lengthbound3.5_ncoils3_nfp4_w7e3_nm5, but results were not reproducable. So strong limitations apply.
The troubles with reproducability also put questionmarks on the results shown in Jorge et al.