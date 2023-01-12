# main.py

import os
from typing import Optional
from fastapi import FastAPI
from routes.test import router as test_router

app = FastAPI() # FastAPI 모듈
app.include_router(test_router) # 다른 route파일들을 불러와 포함시킴

@app.get("/") # Route Path
def index():
    return {
        "Python": "Framework",
    }