import pytest

from example.service_layer import services, unit_of_work
from example.adapters import repo

class FakeFeatureStoreRepository(repo.AbstractFeatureStoreRepository):
    def __init__(self, resume_keywords):
        self.resume_keywords = resume_keywords

    def get_resume_keywords(self, user=None):
        return self.resume_keywords


class FakeFeatureStoreUnitOfWork(unit_of_work.AbstractFeatureStoreUnitOfWork):
    def __init__(self, resume_keywords):
        self.repo = FakeFeatureStoreRepository(resume_keywords)




class FakeMachineLearningRepository(repo.AbstractMachineLearningRepository):
    def __init__(self, model):
        self.model = model

    def get_model(self):
        return self.model


class FakeMachineLearningUnitOfWork(unit_of_work.AbstractMachineLearningUnitOfWork):
    def __init__(self, model):
        self.repo = FakeMachineLearningRepository(model)



def test_happy_path_predict_job_postings(model, resume_keywords, user):
    ml_uow = FakeMachineLearningUnitOfWork(model) 
    fs_uow = FakeFeatureStoreUnitOfWork(resume_keywords)

    result = services.predict_job_postings(
        user,
        ml_uow,
        fs_uow
    )
    expected = {"company":"Google","title":"SWE 2","link":"google.com"}
    assert dict(result) == expected



class FakeFeatureStoreErrorRepository(repo.AbstractFeatureStoreRepository):
    def __init__(self):
        pass

    def get_resume_keywords(self):
        raise ValueError("raise error to test try-catch")


class FakeFeatureStoreErrorUnitOfWork(unit_of_work.AbstractFeatureStoreUnitOfWork):
    def __init__(self):
        pass

def test_error_path_predict_job_postings(model, user):
    ml_uow = FakeMachineLearningUnitOfWork(model) 
    fs_uow = FakeFeatureStoreErrorUnitOfWork()

    with pytest.raises(services.UserNotFound):
        result = services.predict_job_postings(
            user,
            ml_uow,
            fs_uow
        )