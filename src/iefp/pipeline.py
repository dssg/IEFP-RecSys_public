import luigi


from iefp.intermediate.modelling_layer import TransformModelling


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield TransformModelling()
