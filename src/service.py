import bentoml
from bentoml.io import JSON
from pydantic import BaseModel

# Define the model input schema (example using Pydantic)
class AdmissionRequest(BaseModel):
    GRE_Score: float
    TOEFL_Score: float
    University_Rating: int
    SOP: float
    LOR: float
    CGPA: float
    Research: int

# Load the saved model
model_runner = bentoml.sklearn.get("admissions_model").to_runner()

# Define the BentoML service
svc = bentoml.Service("admissions_prediction_service", runners=[model_runner])

# Define the prediction endpoint (synchronous)
@svc.api(input=JSON(pydantic_model=AdmissionRequest),
         output=JSON(),
         route='/predict')
async def predict(admission_data: AdmissionRequest):
    input_data = [[
        admission_data.GRE_Score,
        admission_data.TOEFL_Score,
        admission_data.University_Rating,
        admission_data.SOP,
        admission_data.LOR,
        admission_data.CGPA,
        admission_data.Research
    ]]

    prediction = await model_runner.predict.async_run(input_data)
    return {"Chance of Admit": float(prediction[0])}