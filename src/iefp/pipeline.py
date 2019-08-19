import luigi


from iefp.recommendation import EvaluateRecommendationsRF
from iefp.recommendation import EvaluateRecommendationsLG
from iefp.recommendation import EvaluateRecommendationsGB


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield EvaluateRecommendationsRF()
        yield EvaluateRecommendationsLG()
        yield EvaluateRecommendationsGB()
