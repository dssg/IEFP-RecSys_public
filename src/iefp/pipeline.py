import luigi

from iefp.intermediate.transform import TransformToJourneys
from iefp.processing import CleanInterventions


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield CleanInterventions()
        yield TransformToJourneys()
