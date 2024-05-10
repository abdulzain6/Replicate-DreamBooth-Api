import requests
from typing import Dict, Any, Optional
from pydantic import BaseModel

class RunInput(BaseModel):
    prompt: str
    
class TrainIO(BaseModel):
    instance_prompt: str
    class_prompt: str
    instance_data: str
    max_train_steps: int
    model: str
    trainer_version: Optional[str]
    webhook_completed: Optional[str]

    def model_dump(self) -> Dict[str, Any]:
        return {
            "input": {
                "instance_prompt": self.instance_prompt,
                "class_prompt": self.class_prompt,
                "instance_data": self.instance_data,
                "max_train_steps": self.max_train_steps
            },
            "model": self.model,
            "trainer_version": self.trainer_version,
            "webhook_completed": self.webhook_completed
        }

class DreamBoothAPI:
    def __init__(self, api_token: str):
        self.api_token = api_token

    def upload_zip_file(self, zip_file_path: str) -> str:
        headers = {'Authorization': f'Token {self.api_token}'}
        response = requests.post(
            'https://dreambooth-api-experimental.replicate.com/v1/upload/data.zip',
            headers=headers
        ).json()
        try:
            upload_url = response['upload_url']
        except Exception as e:
            raise ValueError(f"Error {e}, {response}") from e

        with open(zip_file_path, 'rb') as f:
            requests.put(upload_url, headers={'Content-Type': 'application/zip'}, data=f)

        return response['serving_url']

    def train_model(self, train_config: TrainIO) -> Dict[str, Any]:
        headers = {'Authorization': f'Token {self.api_token}'}
        return requests.post(
            'https://dreambooth-api-experimental.replicate.com/v1/trainings',
            headers=headers,
            json=train_config.model_dump(),
        ).json()

    def run_model(self, input: RunInput, version: str) -> Dict[str, Any]:
        headers = {'Authorization': f'Token {self.api_token}'}
        return requests.post(
            'https://api.replicate.com/v1/predictions',
            headers=headers,
            json={"input" : input.model_dump(), "version" : version},
        ).json()

    def get_prediction(self, url: str):
        headers = {'Authorization': f'Token {self.api_token}'}
        return requests.get(url, headers=headers).json()

    def get_training_status(self, training_id: str) -> Dict[str, Any]:
        headers = {'Authorization': f'Token {self.api_token}'}
        url = f'https://dreambooth-api-experimental.replicate.com/v1/trainings/{training_id}'
        response = requests.get(url, headers=headers, timeout=10)
        return response.json()
        
