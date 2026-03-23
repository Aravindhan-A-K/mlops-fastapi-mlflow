from fastapi import FastAPI
from service.load import set_model
from core.middlerware import Middleware
from api.routes import router
from core.exception_handler import register_exception

app = FastAPI(title="MlOps app")

@app.on_event('startup')
async def start():
    set_model()

app.add_middleware(Middleware)

app.include_router(router=router)

register_exception(app=app)

