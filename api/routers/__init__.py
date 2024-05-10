from fastapi.responses import JSONResponse
from fastapi import Depends, File, HTTPException, UploadFile, Form, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Union
import tempfile
from ..globals import WEBHOOK_URL, api, logger, API_KEY
from ..dreambooth import RunInput, TrainIO
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import status


router = APIRouter()
security = HTTPBearer()


class TrainRequest(BaseModel):
    instance_prompt: str
    class_prompt: str
    max_train_steps: int
    model: str
    trainer_version: Optional[str]


class WebhookInput(BaseModel):
    id: str
    input: dict = Field(..., alias="input")
    model: str
    status: str
    trainer_version: str
    webhook_completed: str
    version: str


def verify_apikey(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/train_model/")
def train_model_endpoint(
    instance_prompt: str = Form(...),
    class_prompt: str = Form(...),
    max_train_steps: int = Form(...),
    model: str = Form(...),
    trainer_version: str = Form(...),
    file: UploadFile = File(...),
    verify=Depends(verify_apikey),
) -> JSONResponse:
    try:
        logger.log("info", "Train model request recieved.")
        temp_zip_path = tempfile.mktemp(suffix=".zip")

        with open(temp_zip_path, "wb") as f:
            f.write(file.file.read())

        serving_url = api.upload_zip_file(temp_zip_path)
        train_config_data = {
            "instance_prompt": instance_prompt,
            "class_prompt": class_prompt,
            "max_train_steps": max_train_steps,
            "model": model,
            "trainer_version": trainer_version,
            "webhook_completed": WEBHOOK_URL,
            "instance_data": serving_url,
        }

        train_config = TrainIO(**train_config_data)
        response = api.train_model(train_config)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.log("error", f"THere was an error in training model {e}")
        raise HTTPException(500) from e


@router.post("/run_model/")
def run_model_endpoint(
    run_config: RunInput, version: str, verify=Depends(verify_apikey)
) -> JSONResponse:
    try:
        logger.log("info", "run model request recieved.")
        response: Union[dict, str] = api.run_model(run_config, version)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.log("error", f"THere was an error in running model {e}")
        raise HTTPException(status_code=500) from e


@router.get("/get_prediction/")
def get_prediction(url: str, verify=Depends(verify_apikey)) -> JSONResponse:
    try:
        logger.log("info", "Get prediction request recieved.")
        response: Union[dict, str] = api.get_prediction(url)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.log("error", f"THere was an error in getting prediction {e}")
        raise HTTPException(status_code=500) from e


@router.get("/get_training_status/{training_id}/")
def get_training_status_endpoint(
    training_id: str, verify=Depends(verify_apikey)
) -> JSONResponse:
    try:
        logger.log("info", "Get training status request recieved.")
        response: Union[dict, str] = api.get_training_status(training_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        logger.log("error", f"Get training status error {e}")
        raise HTTPException(status_code=500) from e


@router.post("/webhook/")
def webhook_endpoint(payload: WebhookInput) -> None:
    try:
        logger.log(f"Got payload in webhook, {payload}")
    except Exception as e:
        raise HTTPException(status_code=500) from e
