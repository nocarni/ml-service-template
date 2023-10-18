from fastapi import FastAPI, HTTPException

from example.service_layer import services, unit_of_work
from example.domain.model import User, JobPosting

app = FastAPI()


@app.post("/user/")
async def predict_job_postings(user: User):
    try:
        job_postings = services.predict_job_postings(
            user,
            unit_of_work.MachineLearningUnitOfWork(),
            unit_of_work.FeatureStoreUnitOfWork()
        )
    except services.UserNotFound as e:
        return HTTPException(status_code=400, detail="error")
    return job_postings