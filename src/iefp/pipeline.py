import luigi


from iefp.recommendation import EvaluateRecommendations


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield EvaluateRecommendations()
