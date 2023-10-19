from pandas import DataFrame
from pandas.testing import assert_frame_equal

def test_user_to_dataframe(resume_keywords, user):
    expected = DataFrame([{
        "keywords": resume_keywords.keyword
    }])
    user.add_features({"resume_keywords": resume_keywords})
    
    result = user.to_dataframe()
    assert_frame_equal(result, expected)