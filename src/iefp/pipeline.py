import luigi

from iefp.intermediate.transform_interventions import TransformInterventions


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield TransformInterventions()
