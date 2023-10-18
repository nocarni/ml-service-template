import abc
from typing import Tuple

import pandas as pd

from example.domain.model import User, ResumeKeywords
from example.domain.ml import RealModel, AbstractModel


class AbstractMachineLearningRepository(abc.ABC):
    @abc.abstractmethod
    def get_model(self):
        raise NotImplementedError


class MachineLearningRepository(AbstractMachineLearningRepository):
    def __init__(self):
        pass
    def get_model(self) -> AbstractModel:
        return RealModel()


class AbstractFeatureStoreRepository(abc.ABC):
    @abc.abstractmethod
    def get_resume_keywords(self, *args):
        raise NotImplementedError


class FeatureStoreRepository(AbstractFeatureStoreRepository):
    def __init__(self):
        pass

    def get_resume_keywords(self, user: User) -> ResumeKeywords:
        # Query datastore
        # parse results
        # return results in domain object
        raise ValueError("on purpose")
        # return ResumeKeywords(keyword="Software Engineer")
