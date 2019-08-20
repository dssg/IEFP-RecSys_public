import click

from random import random

from iefp.data import postgres
from iefp.data import s3
from iefp.recommendation import get_top_recommendations


@click.command(help="IEFP Intervention Recommender.")
@click.option("-r", "--recommendations", default=10, help="Number of recommendations")
@click.option(
    "-s",
    "--set-size",
    default=3,
    help="Maximum number of interventions in a recommended set",
)
def cli(recommendations, set_size):
    model_path, _, test_path = postgres.get_best_model_paths()
    df_test = s3.read_parquet(test_path)
    model = s3.read_pickle(model_path)

    # Input: Random observation
    observation = df_test.iloc[int(100 * random())]
    observation = observation.drop(["ttj_sub_12", "ttj"])
    df_recs = get_top_recommendations(
        model, observation, set_size=set_size, n=recommendations
    )
    click.echo(df_recs)
