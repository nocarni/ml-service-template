import pytest

from example.domain.model import ResumeKeywords, User
from example.domain.ml import RealModel

@pytest.fixture
def resume_keywords():
    return ResumeKeywords(keyword="Rails Engineer")

@pytest.fixture
def user():
    return User(user_id="123", name="Jane Doe")

@pytest.fixture
def model():
    return RealModel()
