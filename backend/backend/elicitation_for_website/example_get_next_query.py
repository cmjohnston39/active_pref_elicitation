# demonstrate the behavior of get_next_query()

from get_next_query import get_next_query, robust_recommend_subproblem
from data_functions  import get_test_items, get_test_users, get_data_items, get_data_items_LAHSA
from preference_classes import Query
from utils import get_gamma


def main():

    # create example items (these would be read from the database)
    # items, num_features = get_test_items()
    # items = get_data_items(
    #     "../data/COVID/UK_6781beds-25policies_normalized_0_1.csv"
    # )
    # for i in items:
    #     print(i.features)

    items = get_data_items_LAHSA(
        "../data/LAHSA/AdultHMIS_20210922_preprocessed_final_Robust_edit.csv", standardize_features=True
    )
    for i in items:
        print("items ix", i.id, i.features)

    # get the user objects (these would be read from the database, as needed -- not all at once)
    user_dict = get_test_users(items)

    # print(items)

    # simulate get_next_query
    # for username, user in user_dict.items():
    #     print('simulating get_next_query for user {}...'.format(username))
    #
    #     current_gamma = get_gamma(
    #         len(user.answered_queries) + 1, sigma=0.1, confidence_level=0.9
    #     )
    #
    #     _ = get_next_query(items, user.answered_queries, gamma=current_gamma, verbose=True)
    #     print("\n")

    # simulate elicitation
    username = 'new_user'
    user = user_dict[username]
    print('simulating get_next_query for user {}, with no answered queries'.format(username))

    for x in range(7):
        current_gamma = get_gamma(
            len(user.answered_queries) + 1, sigma=0.3, confidence_level=0.9
        ) #sigma=0.2 works

        a_id, b_id, _, objval, _, _ = get_next_query(items, user.answered_queries, gamma=current_gamma, verbose=True)
        # user.answer_query(Query(items[a_id], items[b_id]))

        # if len(user.answered_queries) == 0:
        # if len(user.answered_queries) == 5:
        #     user.answer_query(Query(items[0], items[44]))
        # elif len(user.answered_queries) == 6:
        #     user.answer_query(Query(items[0], items[25]))
        # if len(user.answered_queries) == 3:
        #     user.answer_query(Query(items[1], items[27]))
        # elif len(user.answered_queries) == 4:
        #     user.answer_query(Query(items[0], items[19]))
        # elif  len(user.answered_queries) == 5:
        #     user.answer_query(Query(items[0], items[1]))
        # elif  len(user.answered_queries) == 6:
        #     user.answer_query(Query(items[2], items[25]))
        # elif  len(user.answered_queries) == 7:
        #     user.answer_query(Query(items[1], items[2]))
        # else:
        user.answer_query(Query(items[a_id], items[b_id]))
        #
        # else:
        #     user.answer_query(Query(items[0], items[2]))

        # resp = [-1,-1, -1, 0, -1, -1,0]
        resp = [1,1,0,-1,-1,0,-1]
        # resp = [1, 1]
        for ix in range( len(user.answered_queries)):
        #     if ix != 4:
            user.answered_queries[ix].response = resp[ix]

        # print("answered q", q.answered_queries)

        print([(i.item_A.id, i.item_B.id, i.response) for i in user.answered_queries])

        items_rec = items.copy()
        # del items_rec[2]
        # print('item rec', items_rec)
        # print(items)

        print('query {}: ({}, {}). answer: {}. objval: {}'.format(i, a_id, b_id, user.answered_queries[-1].response, objval))
        recommended_item, objval, u_vec = robust_recommend_subproblem(
            user.answered_queries,
            items,
            problem_type="maximin",
            verbose=False,
            gamma=current_gamma,
        )
        print("rec item:", recommended_item.id, "objal:", objval, "U vec", u_vec, "\n")

        # print("true u", user.u_true)


    # now simulate with data from the CSV
    # print('--- Now using data from CSV ---')
    # data_file = '/Users/duncan/research/ActivePreferenceLearning/PrefElicitationModule_github/module/data/PolicyQuestion-2019-12-19.csv'
    # data_items = get_data_items(data_file)
    # data_user_dict = get_test_users(data_items)
    #
    # username = 'new_user'
    # user = data_user_dict[username]
    # print('simulating get_next_query for user {}, with no answered queries'.format(username))
    # for i in range(5):
    #     a_id, b_id, _, objval = get_next_query(data_user_dict[username], data_items, verbose=True)
    #     user.answer_query(Query(data_items[a_id], data_items[b_id]))
    #     print('query {}: ({}, {}). answer: {}. objval: {}'.format(i, a_id, b_id, user.answered_queries[-1].response, objval))



    # ------------------------------------------------------------------------------------------------------------------
    # --- Expected output ---
    # ------------------------------------------------------------------------------------------------------------------
    # simulating get_next_query for user a...
    # Academic license - for non-commercial use only
    # next query for user a: item_A=18, item_B=19
    # simulating get_next_query for user d...
    # next query for user d: item_A=0, item_B=2
    # simulating get_next_query for user e...
    # next query for user e: item_A=18, item_B=19
    # simulating get_next_query for user new_user...
    # next query for user new_user: item_A=0, item_B=18
    # simulating get_next_query for user new_user, with no answered queries
    # next query for user new_user: item_A=1, item_B=9
    # query 0: (1, 9). answer: 1. objval: None
    # next query for user new_user: item_A=18, item_B=19
    # query 1: (18, 19). answer: 1. objval: -1.1260250287891678
    # next query for user new_user: item_A=17, item_B=19
    # query 2: (17, 19). answer: -1. objval: -0.8254620694257426
    # next query for user new_user: item_A=17, item_B=18
    # query 3: (17, 18). answer: -1. objval: -0.05639266801591408
    # next query for user new_user: item_A=16, item_B=19
    # query 4: (16, 19). answer: -1. objval: -0.056392668015913694
    # --- Now using data from CSV ---
    # simulating get_next_query for user new_user, with no answered queries
    # next query for user new_user: item_A=0, item_B=6
    # query 0: (0, 6). answer: -1. objval: None
    # next query for user new_user: item_A=12, item_B=13
    # query 1: (12, 13). answer: -1. objval: -1.0027576907541431
    # next query for user new_user: item_A=11, item_B=13
    # query 2: (11, 13). answer: -1. objval: -0.9599118514113755
    # next query for user new_user: item_A=11, item_B=12
    # query 3: (11, 12). answer: -1. objval: -0.9599118514113755
    # next query for user new_user: item_A=10, item_B=13
    # query 4: (10, 13). answer: -1. objval: -0.9599118514113755


if __name__ == "__main__":
    main()