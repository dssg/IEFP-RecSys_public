import luigi


from iefp.modelling import AddOutcomes


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield AddOutcomes()
