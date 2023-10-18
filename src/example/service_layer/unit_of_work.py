import abc
import os

from example.adapters import repo

class AbstractMachineLearningUnitOfWork(abc.ABC):
    def __init__(self):
        self.repo: repo.AbstractMachineLearningRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class MachineLearningUnitOfWork(AbstractMachineLearningUnitOfWork):
    def __init__(self):
        self.repo = repo.MachineLearningRepository()

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)


class AbstractFeatureStoreUnitOfWork(abc.ABC):
    def __init__(self) -> None:
        self.repo: repo.AbstractFeatureStoreRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class FeatureStoreUnitOfWork(AbstractFeatureStoreUnitOfWork):

    def __init__(self):
        self.repo = repo.FeatureStoreRepository()

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
