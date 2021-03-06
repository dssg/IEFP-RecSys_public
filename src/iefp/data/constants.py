class Category:
    UNEMPLOYED_FIRST_JOB = 1
    UNEMPLOYED_NEW_JOB = 2
    EMPLOYED = 3
    EMPLOYED_PART_TIME = 4


class Interventions:
    TRAINING = 777
    TRAINING_SUB_CATEGORIES = [777785, 777802, 777803, 777805, 777801]
    GENERIC_TRAINING_SUB_CATEGORY = 777777
    EFA_INTERVENTIONS_LIST = [742, 767, 768, 769, 770, 771, 772, 779, 784, 785]
    EFA_GENERIC_INTERVENTION = 1000


class Movement:
    REGISTRATION = 11
    JOB_PLACEMENT_IEFP = 21
    CANCELLATION = 31
    INTERVENTION_OUTCOME = 35
    CATEGORY_CHANGE = 43


class RegistrationReason:
    NOT_PAID = 17


class Status:
    ACTIVE = "ACT"


class Database:
    EVALUATION_TABLE = "modelling.evaluations"
    INTERVENTIONS_EXTRACTION_SIZE = 10000000
    INTERVENTIONS_TABLE = "intervencoes"
    PEDIDOS_EXTRACTION_SIZE = 15000000
    PEDIDOS_TABLE = "pedidos"
    RECOMMENDATION_ERRORS_TABLE = "modelling.recommendation_errors"


class S3:
    EXTRACT = "extract/"
    CLEAN = "clean/"
    TRANSFORM = "transform/"
    MODELLING = "modelling/"
    MODELS = "models/"
