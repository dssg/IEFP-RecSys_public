import click

from iefp.data import postgres
from iefp.data import s3
from iefp.recommendation import get_top_recommendations


@click.command(help="IEFP Intervention Recommender.")
@click.option(
    "-i", "--journey-id", default=6136, help="Journey User ID of the Job Seeker"
)
@click.option("-r", "--recommendations", default=10, help="Number of recommendations")
@click.option(
    "-s",
    "--set-size",
    default=3,
    help="Maximum number of interventions in a recommended set",
)
def cli(recommendations, set_size, journey_id):
    model_path, _, test_path = postgres.get_best_model_paths()
    df_test = s3.read_parquet(test_path)
    model = s3.read_pickle(model_path)

    if not journey_id:
        click.echo(
            "No Journey id specified. Try for example {}".format(
                df_test.sample(5).index.tolist()
            )
        )
        return
    elif journey_id not in df_test.index.tolist():
        click.echo(
            "Journey ID {} not found. Try for example {}".format(
                journey_id, df_test.sample(5).index.tolist()
            )
        )
        return

    observation = df_test.loc[journey_id, :]
    dem_cols = [col for col in observation.index if "d_" in col[:2]]
    output = observation[dem_cols]
    click.echo("Journey {} --- Demographics".format(journey_id))
    click.echo("---------------")
    click.echo("Age: {}".format(round(output["d_age"] * 85)))
    click.echo(output[output == 1])
    click.echo("---------------")
    click.echo("Intervention Recommendations".format(journey_id))
    click.echo("---------------")
    observation = observation.drop(["ttj_sub_12", "ttj"])
    df_recs = get_top_recommendations(
        model, observation, set_size=set_size, n=recommendations
    )
    click.echo(df_recs)
