import luigi

from iefp.data.extract import ExtractInterventions, ExtractPedidos


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield ExtractInterventions()
        yield ExtractPedidos()
