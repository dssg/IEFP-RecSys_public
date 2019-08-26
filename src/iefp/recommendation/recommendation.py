import itertools
import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator


def get_top_recommendations(
    model: BaseEstimator, journey: pd.Series, set_size: int, n: int
):
    """
    Calculates top n recommendations for a given journey series

    :param model: Sci-kit learn model
    :param journey: Journey series including interventions
    :param set_size: Size of intervention sets
    :param n: Number of recommendations to return
    """
    # Generate intervention combinations
    interventions = [i for i in journey.index if "i_" in i[:2]]
    df_intervention_combinations = generate_combinations(
        k=set_size, n=len(interventions)
    )
    df_intervention_combinations.columns = interventions

    # Generate dataframe with fixed features and intervention combinations
    df_journey = pd.DataFrame(journey).T.drop(interventions, axis=1)
    df_journey_combinations = df_journey.append(
        [df_journey] * (df_intervention_combinations.shape[0] - 1), ignore_index=True
    )
    df_journey_combinations = df_journey_combinations.merge(
        df_intervention_combinations, right_index=True, left_index=True
    )

    y_proba = model.predict_proba(df_journey_combinations)
    df_recommendations = calculate_top_interventions(
        df_journey_combinations, y_proba, n
    )

    df_recommendations.columns = [
        "intervention_" + str(i + 1) for i in range(set_size)
    ] + ["predicted_probability"]
    df_recommendations.index = df_recommendations.index + 1

    return df_recommendations


def generate_combinations(k: int, n: int):
    """
    Generates binary dataframe of k out of n combinations

    :param k:
    :param n:
    """
    result = list()
    for i in range(1, k + 1):
        for bits in itertools.combinations(range(n), i):
            s = [0] * n
            for bit in bits:
                s[bit] = 1
            result.append(s)

    return pd.DataFrame(result)


def calculate_top_interventions(X: pd.DataFrame, y_proba: np.array, n: int):
    """
    Calculates top interventions based on predicted probabilities

    :param X: Input matrix used for prediction
    :param y_proba: Result probability vector
    :param n: Top n results
    """
    top_n_rec = (
        pd.DataFrame(y_proba, columns=["false", "true"])
        .sort_values("true", ascending=False)
        .head(n)
    )

    intervention_cols = [col for col in X.columns if "i_" in col[:2]]
    df_result = X.loc[top_n_rec.index, intervention_cols]

    rec_interv = list()
    for i in range(len(df_result)):
        row = df_result.iloc[i]
        interventions = row[row == 1]
        interventions = (
            interventions.index.str.replace("i_", "").str.replace("_", " ").tolist()
        )
        rec_interv.append(interventions + [top_n_rec.iloc[i]["true"]])

    df_rec_interv = pd.DataFrame(rec_interv)
    return df_rec_interv
