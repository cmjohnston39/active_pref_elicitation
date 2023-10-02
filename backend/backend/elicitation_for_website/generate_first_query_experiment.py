import itertools

n = 5
nums = [-1, 0, 1]
list_all_resp = list(list(entry) for entry in itertools.product(nums, repeat=5))
print(len(list_all_resp))
for ix, resp in enumerate(list_all_resp):
    print(resp)
    file = """#!/bin/bash
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=6
#SBATCH --mem-per-cpu=4GB
#SBATCH --time=48:00:00
#SBATCH --array=0
#SBATCH --account=vayanou_581
    
    
module load gcc/8.3.0
module load python
module load gurobi
    
sigma="0.05"
sigma=($sigma) 
    
python3 query_look_up_table_new_fix_first_response.py --first-response=""" + str(resp)[1:-1].replace(" ","") +""" --max-K 10 --time-limit 3600 --sigma ${sigma[$SLURM_ARRAY_TASK_ID]}  --confidence-level 0.9 --fair-type "sum" --problem-type "mmr" --u0-type positive_box --input-csv ../data/LAHSA/AdultHMIS_20210922_preprocessed_final_Robust_edit.csv --output-dir ./hi"""
    print(file)

    with open("./house_query/housing_pref" + str(ix) +".sh", "w") as text_file:
        text_file.write(file)
