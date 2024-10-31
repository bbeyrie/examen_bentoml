import bentoml
from bentoml.io import JSON
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta
import numpy as np

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "SECRET_KEYYY"
JWT_ALGORITHM = "HS256"

# User credentials for authentication
USERS = {
    "admin": "admin",
    "bento": "bento"
}

# Define the model input schema (example using Pydantic)
class AdmissionRequest(BaseModel):
    GRE_Score: float
    TOEFL_Score: float
    University_Rating: int
    SOP: float
    LOR: float
    CGPA: float
    Research: int

# Middleware for JWT Authentication
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Secure only the predict endpoint
        if request.url.path == "/predict":
            token = request.headers.get("Authorization")
            if not token:
                return JSONResponse(status_code=401, content={"detail": "Missing authentication token"})
            
            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail": "Token has expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})
            
            request.state.user = payload.get("sub")

        response = await call_next(request)
        return response

# Function to create a JWT token
def create_jwt_token(user_id: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

# Load the saved model
model_runner = bentoml.sklearn.get("admissions_model").to_runner()

# Define the BentoML service
svc = bentoml.Service("admissions_prediction_service", runners=[model_runner])

# Add the JWTAuthMiddleware to the service
svc.add_asgi_middleware(JWTAuthMiddleware)

# Login endpoint to get JWT token
@svc.api(input=JSON(), output=JSON(), route='/login')
def login(credentials: dict) -> dict:
    username = credentials.get("username")
    password = credentials.get("password")

    if username in USERS and USERS[username] == password:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

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