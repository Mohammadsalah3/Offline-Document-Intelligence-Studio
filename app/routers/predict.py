#from _future_ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.prediction_service import predict_iris


router = APIRouter()


class PredictRequest(BaseModel):
    features: list[float] = Field(..., example=[5.1, 3.5, 1.4, 0.2])


@router.post("/")
def predict(request: PredictRequest):
    print("[predict] request received, features:", request.features)
    try:
        result = predict_iris(request.features)
        print("[predict] result:", result)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")