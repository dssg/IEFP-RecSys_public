import luigi


from iefp.recommendation import EvaluateRecommendationsRF
from iefp.recommendation import EvaluateRecommendationsLG


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield EvaluateRecommendationsRF()
        yield EvaluateRecommendationsLG()
