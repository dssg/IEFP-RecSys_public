import luigi

from iefp.processing.cleaning_task import CleanPedidos
from iefp.data.extract import ExtractInterventions


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield CleanPedidos()
        yield ExtractInterventions()
