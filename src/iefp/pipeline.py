import luigi

from iefp.modelling.add_mappings import AddModelMappings


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield AddModelMappings()
