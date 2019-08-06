import luigi


from iefp.modelling import SplitTrainTest


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield SplitTrainTest()
