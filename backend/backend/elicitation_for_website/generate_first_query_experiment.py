import itertools

n = 5
nums = [-1, 0, 1]
list_all_resp = list(list(entry) for entry in itertools.product(nums, repeat=5))
print(len(list_all_resp))
for ix, resp in enumerate(list_all_resp):
    print(resp)
    file = """#!/bin/bash \n
    # SBATCH --ntasks=1 \n
    # SBATCH --cpus-per-task=6\n
    # SBATCH --mem-per-cpu=16GB\n
    # SBATCH --time=48:00:00\n
    # SBATCH --array=0-2\n
    # SBATCH --account=vayanou_581\n
    
    
    module load gcc/8.3.0 \n
    module load python \n
    module load gurobi\n
    
    sigma="0.025 0.05 0.1" \n
    
    sigma=($sigma) \n
    
    python3 query_look_up_table_new_fix_first_response.py --first-response=""" + str(resp)[1:-1].replace(" ","") +""" --max-K 10 --time-limit 3600 --sigma ${sigma[$SLURM_ARRAY_TASK_ID]}  --confidence-level 0.9 --fair-type "sum" --problem-type "mmr" --u0-type box --input-csv ../data/LAHSA/AdultHMIS_20210922_preprocessed_final_Robust_edit.csv --output-dir ./hi"""
    print(file)

    with open("./house_query/housing_pref" + str(ix) +".sh", "w") as text_file:
        text_file.write(file)
