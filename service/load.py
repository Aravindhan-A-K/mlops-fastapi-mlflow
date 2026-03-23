import mlflow
import os


model = None

def set_model():
    mlflow.set_tracking_uri(os.getenv("MODEL_TRACKING_URI"))
    environment = os.getenv("Environment", "Production")
    global model 
    model = mlflow.pyfunc.load_model(f"models:/Bike_sharing_model/{environment}")

def get_model():
    return model