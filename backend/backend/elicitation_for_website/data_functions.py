# placeholder functions for interacting with a database

import numpy as np
import pandas as pd

from preference_classes import Item, Query, User

def get_test_items():
    """
    create a list of item objects
    """
    rs = np.random.RandomState(0)

    feature_names = ['f1', 'f2', 'f3', 'f4', 'f5']
    num_features = 2
    num_items = 4
    random_features = lambda: rs.rand(num_features) * 10 - 5

    feat_list = [[1,0],[-1,0],[0,1],[-1,1]]

    items = []
    for i in range(num_items):
        # features = random_features()
        features = feat_list[i]
        print("featurse:", features)
        items.append(Item(features, i, feature_names=feature_names))

    return items, num_features


def get_test_users(items):
    """
    create a dict of user obejcts. key = username, value = User object

    input:
    - items: (list(Item)). a list of preference_classes.Item objects
    """

    np.random.seed(0)

    num_features = len(items[0].features)

    a = User('a')
    a.answered_queries = [
            Query(items[0], items[1], response=1),
        ]

    d = User('d')
    d.answered_queries = []

    # e = User('e')
    # e.answered_queries = [
    #     Query(items[4], items[6], response=1),
    #     Query(items[4], items[6], response=-1),
    #     Query(items[2], items[4], response=0),
    #     Query(items[1], items[3], response=0),
    # ]

    new_user = User('new_user')
    new_user.u_true = np.random.rand(num_features)

    user_dict = {'a': a,
                 'd': d,
                 # 'e': e,
                 'new_user': new_user,
                 }

    return user_dict


def get_data_items(data_file):
    df = pd.read_csv(data_file)

    feature_names = list(df.columns[0:])

    items = []
    for i, row in df.iterrows():
        features = np.array(row)[0:]
        items.append(Item(features, i, feature_names=feature_names))

    return items

def get_data_items_LAHSA(filename, max_items=99999, standardize_features=False, normalize_features=False, drop_cols=[]):

    df = pd.read_csv(filename)

    # df["IsInterpretable_int"] = df["IsInterpretable"].apply(lambda x: 1 if x else 0)

    # drop unused cols
    # drop_cols = drop_cols + ["id", "PolicyType", "Policy", "IsInterpretable"]
    # print(df.head())
    if "UsesProtectedFeatures" in df.columns.to_list():
        drop_cols = ["Id", "PolicyName", "Policy", "NumFeatures", "UsesProtectedFeatures"]
    else:
        drop_cols = ["Approach", "TrainingFile", "NumDatapoints", "TreeDepth", "BranchingLimit", "TimeLimit", "ProbTypePred", "SolverStatus", "ObjVal", "MIPGap", "SolvingTime", "NumBranchingNodes"]
    df.drop(columns=drop_cols, inplace=True)

    # df["NumBranchingFeatures"] = -df["NumBranchingFeatures"]
    # df["NumProtectedBranchingFeatures"] = -df["NumProtectedBranchingFeatures"]

    items = []
    for i, row in df.iterrows():
        items.append(Item(row.values, i))

    if len(items) > max_items:
        items = items[:max_items]

    if standardize_features:
        for i_feat in range(len(items[0].features)):
            feature_list = [i.features[i_feat] for i in items]
            mean_feat = np.mean(feature_list)
            stddev_feat = np.std(feature_list)

            if stddev_feat > 0:
                for item in items:
                    item.features[i_feat] = (
                        item.features[i_feat] - mean_feat
                    ) / stddev_feat
            else:
                for item in items:
                    item.features[i_feat] = 0.0

    if normalize_features:
        for i_feat in range(len(items[0].features)):
        # for i_feat in range(2):
            feature_list = [i.features[i_feat] for i in items]
            max_feat = np.max(feature_list)
            min_feat = np.min(feature_list)

            for item in items:
                item.features[i_feat] = (item.features[i_feat] - min_feat) / (max_feat - min_feat)

    return items