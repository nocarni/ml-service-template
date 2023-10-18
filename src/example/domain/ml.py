import abc

from pandas import DataFrame

from example.domain.model import JobPosting

class AbstractModel(abc.ABC):
    @abc.abstractmethod
    def predict(df: DataFrame) -> JobPosting:
        raise NotImplementedError

class RealModel(AbstractModel):
    def __init__(self):
        self.model = None  # load the actual model from filesystem or remote storage

    def predict(self, df: DataFrame) -> JobPosting:
        # self.model.predict(df)
        return JobPosting(
            company="Google",
            title="SWE 2",
            link="google.com"
        )