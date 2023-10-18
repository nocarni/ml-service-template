from example.service_layer import unit_of_work
from example.domain.model import User, ResumeKeywords, JobPosting

class UserNotFound(Exception):
    pass


def predict_job_postings(
    user: User,
    ml_uow: unit_of_work.AbstractMachineLearningUnitOfWork,
    fs_uow: unit_of_work.AbstractFeatureStoreUnitOfWork,
):

    with fs_uow:
        try:
            features: ResumeKeywords = fs_uow.repo.get_resume_keywords(user=user)
        except Exception as e:
            raise UserNotFound(f"Features for user `{user.name}` could not be found.")

    user.add_features({
        "resume_keywords": features
    })
    with ml_uow:
        model = ml_uow.repo.get_model()
        posts: JobPosting = model.predict(
            user.to_dataframe()
        )

    return posts

