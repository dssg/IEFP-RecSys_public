import click

from iefp.data import postgres
from iefp.data import s3
from iefp.recommendation import get_top_recommendations


@click.command(help="IEFP Intervention Recommender.")
@click.option("-i", "--journey-id", type=int, help="Journey User ID of the Job Seeker")
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

    observation = df_test.loc[journey_id, :].copy()
    observation = observation.drop(["ttj_sub_12", "ttj"])
    interv_cols = [col for col in observation.index if "i_" in col[:2]]
    dem_cols = [col for col in observation.index if "d_" in col[:2]]

    click.echo("Journey {} --- Demographics".format(journey_id))
    click.echo("---------------")
    output = observation[dem_cols]
    click.echo(output[output == 1])
    # NOTE: Un-normalize age here.
    # Get maximum age from journey data instead
    click.echo("Age: {}".format(round(output["d_age"] * 78)))
    click.echo("---------------")
    click.echo("Use Model: {}".format(model.__class__.__name__))
    click.echo("---------------")
    observation[interv_cols] = 0
    base_probability = model.predict_proba(observation.to_numpy().reshape(1, -1))
    click.echo("Base employment probability {:.4f}".format(base_probability[0][1]))
    click.echo("---------------")
    click.echo("Intervention Recommendations".format(journey_id))
    click.echo("---------------")
    df_recs = get_top_recommendations(
        model, observation, set_size=set_size, n=recommendations
    )
    click.echo(df_recs)
