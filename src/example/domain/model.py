from typing import List, Optional, Dict
from pandas import DataFrame
from pydantic import BaseModel

class JobPosting(BaseModel):
    company: str
    title: str
    link: str


class FeatureSet(BaseModel):
    ...

class ResumeKeywords(FeatureSet):
    keyword: str

class User(BaseModel):
    user_id: str
    name: str
    features: Optional[Dict[str, FeatureSet]] = None

    def add_features(self, features: Dict[str,FeatureSet]):
        self.features = features

    def to_dataframe(self):
        row = [{
            "keywords": self.features['resume_keywords'].keyword
        }]
        return DataFrame(row)