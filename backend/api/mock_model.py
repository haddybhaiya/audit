from fastapi import APIRouter

router = APIRouter(prefix="/mock", tags=["mock"])


@router.post("/")
def mock_predict(record: dict):

    gender = record.get("gender")

    if gender == "Male":
        score = 0.8
    else:
        score = 0.3

    return {"prediction": score}
# mock model for testing the probe endpoint without needing an actual model API. 
# This allows us to verify that the probe logic is working correctly and can detect bias in a controlled setting.