import luigi

from iefp.intermediate.add_outcomes import AddBinOutcome
from iefp.processing import CleanInterventions


class RunFull(luigi.WrapperTask):
    def requires(self):
        yield CleanInterventions()
        yield AddBinOutcome()
