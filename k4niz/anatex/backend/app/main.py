from fastapi import FastAPI
from .routers.organs import router as organs_router

app = FastAPI()
app.include_router(organs_router, prefix="/api")
