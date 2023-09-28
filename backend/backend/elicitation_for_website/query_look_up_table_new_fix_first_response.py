import pickle
import argparse
import os

from get_next_query import find_optimal_query_mip, find_optimal_query
from preference_classes import Query
from data_functions import get_data_items, get_data_items_LAHSA
from utils import get_gamma ,get_logger, generate_filepath, U0_positive_normed
from static_elicitation import feasibility_subproblem


def create_query_lookup_table(args):
    """
    create lookup table (dictionary) to calculate offline the next query to ask

    """

    file_str = args.input_csv[1:-30] + "_K" + str(args.max_K) + "_s" + str(args.sigma) + "_" + str(
        args.problem_type) + "_start" + str(args.first_response)

    print(file_str)

    output_file = generate_filepath('./', "preference_experiment", "csv")

    output_file = os.path.join('query_responses/' + file_str, output_file)

    os.makedirs('/'.join(output_file.split('/')[:-1]), exist_ok=True)

    log_file = generate_filepath('./', "preference_experiment_LOGS", "txt")

    log_file = os.path.join('query_responses/' + file_str, log_file)

    logger = get_logger(logfile=log_file)

    agents=[1]

    items = get_data_items_LAHSA(
        args.input_csv, standardize_features=True
        )
    for i in items:
        print("items are", i.features)

    print("total number of items", len(items))

    valid_responses=[-1,0, 1]

    first_response = args.first_response

    print("first resposne is", first_response)
    print("args first resposne is", args.first_response)
    if type(first_response[0]) == list:
        first_response = first_response[0]
        args.first_response=args.first_response[0]

    print("first resposne now is", first_response)
    print("args first resposne now is", args.first_response)


    lookup= {}
    # start = True
    query_list = []
    count = 0

    #TODO: rewrite using response list in find_optimal_query

    while len(query_list) !=0 or count == 0:

        print("processing num:", count, "\n")
        logger.info("response number: {}".format(count))

        if count == 0:
            answered_queries = []

        else:
            answered_queries = query_list[0]
            print("aq", [(q.item_A.id, q.item_B.id,q.response ) for q in answered_queries])

        gamma = get_gamma(len(answered_queries) + 1, args.sigma, args.confidence_level)

        print("gamma is", gamma)

        item_a_opt, item_b_opt, _, objval_opt = find_optimal_query_mip(answered_queries, items, gamma=gamma,
                           problem_type=args.problem_type, u0_type="box", eps=0.0, time_limit=args.time_limit)


        # item_a_exhaust, item_b_exhaust, _, objval_exhaust = find_optimal_query(answered_queries, items, gamma=gamma)
        #
        # #assert using exhaustive check
        # print("A:", item_a_opt.id, item_a_exhaust.id)
        # print("B:", item_b_opt.id, item_b_exhaust.id)
        # print("obj val", objval_exhaust, objval_opt)
        # assert((item_a_opt.id == item_a_exhaust.id and item_b_opt.id == item_b_exhaust.id)
        #        or (abs(objval_exhaust - objval_opt) <= 1e-3))

        print(tuple([(q.item_A.id, q.item_B.id, q.response) for q in answered_queries]), ":", (item_a_opt.id,item_b_opt.id))

        lookup[tuple([(q.item_A.id, q.item_B.id, q.response) for q in answered_queries])] = (item_a_opt.id,item_b_opt.id)

        if len(answered_queries) != args.max_K - 1:
            small= 1000

            print("len",len(args.first_response))
            print(args.first_response)

            if args.first_response == None or (count > len(args.first_response) -1):
                for s in valid_responses:
                    # print("s is", s)
                    answered_queries.append(Query(item_a_opt, item_b_opt, response=s))
                    # print("answere queries", [(q.item_A.id, q.item_B.id,q.response) for q in answered_queries])
                    query_list.append(answered_queries)
                    answered_queries=answered_queries[:-1] #remove just added new query


            else:
                answered_queries.append(Query(item_a_opt, item_b_opt, response=first_response[0]))
                # print("answere queries", [(q.item_A.id, q.item_B.id,q.response) for q in answered_queries])
                query_list.append(answered_queries)
                answered_queries = answered_queries[:-1]  # remove just added new query
                print("first response before", first_response)
                first_response=first_response[1:] #get rid of first response we've already processed
                print("first response after", first_response)


        # for q in query_list:
        #     print("q", q[0].item_A.id, q[0].item_B.id,q[0].response)

        if count !=0:
            query_list = query_list[1:] #remove processed query

        count +=1

        if count % 1000 == 0:
            output_file = os.path.join('query_responses/' + file_str + str(count) )
            os.makedirs('/'.join(output_file.split('/')[:-1]), exist_ok=True)

            log_file = generate_filepath('./', str(count) + "query_dictionary", "p")
            output_file = os.path.join('query_responses/' + file_str, log_file)
            pickle.dump(lookup, open(output_file, "wb"))

            log_file = generate_filepath('./', str(count) +  "query_list_unsettled", "p")
            output_file = os.path.join('query_responses/' + file_str, log_file)

            unset_pickle = []
            for qi in query_list:
                q_list = []
                for q in qi:
                    q_list.append((q.item_A.id, q.item_B.id, q.response))
                unset_pickle.append(q_list)
            print("unsettled",unset_pickle)
            pickle.dump(unset_pickle, open(output_file, "wb"))


    print("lookup is", lookup)
    for key, val in lookup.items():
        print("prev answered:", key, "next query:", val)
    # print(len(lookup)) # 3^(K) + 1

    output_file = os.path.join('query_responses/'+ file_str)
    #
    os.makedirs('/'.join(output_file.split('/')[:-1]), exist_ok=True)
    log_file = generate_filepath('./', "preference_experiment_LOGS", "p")
    output_file = os.path.join('query_responses/' + file_str, log_file)

    pickle.dump(lookup, open(output_file, "wb"))

def main():
    def list_of_ints(arg):
        return list(map(int, arg.split(',')))

    parser = argparse.ArgumentParser(
        description="static experiment comparing optimal heuristic to random "
    )

    parser.add_argument(
        "--max-K", type=int, help="total number of queries to ask", default=5
    )

    parser.add_argument(
        "--first-response", type=list_of_ints, nargs="+",help="elements of {-1,1,0} separated by commas, e.g. 1,-1,0"
                                                    " which will be first response(s) in list (to parallelize)", default=None
    )

    parser.add_argument(
        "--sigma",
        type=float,
        default=0.0,
        help="st. dev. for distirbution of xi inconsistency values. If sigma=0, use no inconsistencies",
    )
    parser.add_argument(
        "--time-limit",
        type=float,
        default=1800000.0,
        help="time limit for solver",
    )

    parser.add_argument(
        "--confidence-level",
        type=float,
        default=1.0,
        help="level of confidence for which the sum of agent consistencies will be less than"
             "the calculated \Gamma value",
    )

    parser.add_argument("--output-dir", type=str, help="output directory",
                        default="C:\\Users\\cjjoh\\Downloads\\ActiveRobustPreferenceElicitation-master")

    parser.add_argument(
        "--u0-type",
        type=str,
        default="box",
        help="type of initial uncertainty set to use {'box' | 'positive_normed'}",
    )

    parser.add_argument(
        "--problem-type",
        type=str,
        default="maximin",
        help="type of problem to solve {'maximin' | 'mmr'}",
    )

    parser.add_argument(
        "--same-query-num",
        action="store_true",
        default=False,
        help="if set, each agent is asked the same number of queries per round",
    )

    parser.add_argument(
        "--fair-type",
        type=str,
        default="sum",
        help="fairness aggregation type is either min or sum",
    )

    parser.add_argument("--input-csv", type=str, help="csv of item data to read", default="./covid_data_normalized")

    parser.add_argument(
        "--partworth",
        action="store_true",
        default=False,
        help="use partworth utilities (sum to 1 per agent)",
    )

    parser.add_argument(
        "--DEBUG",
        action="store_true",
        help="if set, use a fixed arg string. otherwise, parse args.",
        default=False,
    )

    args = parser.parse_args()

    print("args are", args)

    if args.DEBUG:
        # fixed set of parameters, for debugging:
        arg_str = "--max-K 1"
        arg_str += " --u0-type box"
        arg_str += " --problem-type mmr"
        arg_str += " --sigma 0.025"
        arg_str += " --confidence-level 0.9"
        arg_str += " --output-dir ./hi"
        arg_str += " --input-csv ../data/LAHSA/AdultHMIS_20210922_preprocessed_final_Robust_edit.csv"
        arg_str += " --fair-type sum"
        # arg_str += " --partworth"
        arg_str += " --first-response=1,-1"
        arg_str += " --time-limit 3600"
        # arg_str += " --same-query-num"

        args_fixed = parser.parse_args(arg_str.split())
        create_query_lookup_table(args_fixed)
    else:
        args = parser.parse_args()
        create_query_lookup_table(args)


if __name__ == "__main__":
    main()