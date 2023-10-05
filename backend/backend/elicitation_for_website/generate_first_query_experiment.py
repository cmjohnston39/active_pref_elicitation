import itertools

# n = 5
list_of_things = [[-1, -1, 1], [0, 0], [0, 1, -1], [-1, 0, 1]] #9+ 27 + 9 +9 = 54

nums = [-1, 0, 1]
list_total = []
for i in list_of_things:
    list_all_resp = list(list(entry) for entry in itertools.product(nums, repeat=5-len(i)))
    for j in list_all_resp:
        print(i+j)
        list_total.append(i +j)
# print(len(list_total))
# sys.exit()
for ix, resp in enumerate(list_total):
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

    with open("./house_query3/housing_pref" + str(ix) +".sh", "w") as text_file:
        text_file.write(file)
