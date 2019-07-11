import luigi

from iefp.data.extract import ExtractPedidos


class RunFull(luigi.WrapperTask):
    def requires(self):
        return ExtractPedidos()
