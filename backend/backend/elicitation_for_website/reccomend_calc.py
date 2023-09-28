import pickle
import argparse
import os

from get_next_query import find_optimal_query_mip, find_optimal_query
from preference_classes import Query
from data_functions import get_data_items, get_data_items_LAHSA
from utils import get_gamma ,get_logger, generate_filepath, U0_positive_normed
from static_elicitation import feasibility_subproblem
from get_next_query import robust_recommend_subproblem
from preference_classes import Item, Query


items = get_data_items_LAHSA(
    "../data/LAHSA/AdultHMIS_20210922_preprocessed_final_Robust_edit.csv", standardize_features=True
    )
for i in items:
    print("items are", i.features)

print("total number of items", len(items))

valid_responses=[-1,0, 1]

with open("AdultHMIS_20210922_prep_K10_s0.65_maximin.p", 'rb') as f:
    query_list = pickle.load(f)

rec_dict = {}

for sequence in query_list:
    # print(sequence)
    if len(sequence) == 9:

        for resp in {1,0,-1}:
            q_list = []
            for q in sequence:
                q_list.append(Query(items[q[0]], items[q[1]],response=q[2]))
            q_list.append(Query(items[query_list[sequence][0]], items[query_list[sequence][1]], response=resp))
            # print(sequence, query_list[sequence])
            # print([(i.item_A.id, i.item_B.id, i.response) for i in q_list])

            rec_item, _, _ = robust_recommend_subproblem(
                q_list, items, problem_type="maximin", verbose=False, gamma=0.65
            )
            # print("rec item id",rec_item.id)

            if rec_item is None:
                print([(i.item_A.id, i.item_B.id, i.response) for i in q_list])
                print("none type" )
                print('now', [(i.item_A.id, i.item_B.id, i.response) for i in q_list[:-1]])
                rec_item, _, _ = robust_recommend_subproblem(
                    q_list[:-1], items, problem_type="maximin", verbose=False, gamma=0.65
                )
                # print(rec_item.id)
                continue

            if rec_item.id not in rec_dict:
                rec_dict[rec_item.id] = 1

            else:
                rec_dict[rec_item.id] += 1
            print(rec_dict)
        # sys.exit()