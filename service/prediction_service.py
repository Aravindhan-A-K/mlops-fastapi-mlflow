import pandas as pd
from fastapi import Request
from fastapi import BackgroundTasks
from api.schemas import RequestModel
from core.logger import logger
import time


def predict_service(request:Request, data:RequestModel, background_task:BackgroundTasks, model):
    start_time = time.time()
    try:
        input_dict = data.model_dump()
        input_df = pd.DataFrame([input_dict])
        input_df = input_df.reindex(columns=model.feature_names_in_)

        prediction = model.predict(input_df)
        prediction = {'salePrice': float(prediction[0])}
        return prediction
    finally:
        latency = time.time() - start_time
        logger.info("Prediction successful" if prediction else "Prediction failed", 
                    extra={
                    'correlation_id': getattr(request.state, "correlation_id" , None),
                    'model_latency': latency,
                    'prediction_value': prediction})
