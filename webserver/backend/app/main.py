# main.py

import os
from typing import Optional
from fastapi import FastAPI
from routers.test import router as test_router
from routers.map import router as map_router
from routers.users import router as user_router
from routers.zzim import router as zzim_router
from routers.recommend import router as recommend_router

app = FastAPI() # FastAPI 모듈
app.include_router(test_router) # 다른 route파일들을 불러와 포함시킴
app.include_router(map_router)
app.include_router(user_router)
app.include_router(zzim_router)
app.include_router(recommend_router)

@app.get("/") # Route Path
def index():
    return {
        "Python": "Framework",
    }