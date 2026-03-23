from fastapi import APIRouter, BackgroundTasks, Depends, Request
from api.schemas import RequestModel, ResponseModel
from service.prediction_service import predict_service
from service.load import get_model

router = APIRouter()

@router.get('/')
async def health_check():
    return {"Status": 'Ok'}

@router.post('/predict', response_model=ResponseModel)
async def predict(request: Request, data: RequestModel, background_tasks: BackgroundTasks, model=Depends(get_model())):
    return predict_service(request, data, background_tasks, model)