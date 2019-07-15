import luigi

from iefp.intermediate.transform import TransformToJourneys
from iefp.data.extract import ExtractInterventions


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield ExtractInterventions()
        yield TransformToJourneys()
