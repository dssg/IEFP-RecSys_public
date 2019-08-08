import luigi


from iefp.modelling import EvaluateRandomForest


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield EvaluateRandomForest()
