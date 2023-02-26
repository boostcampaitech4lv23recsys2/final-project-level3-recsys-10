# main.py

import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.test import router as test_router
from routers.map import router as map_router
from routers.users import router as user_router
from routers.zzim import router as zzim_router
from routers.recommend import router as recommend_router

origins = ["http://27.96.130.120:30009","34.64.72.237:3306","http://34.125.1.1:80","http://hobbang.shop:80","http://hobbang.shop","https://double-operator-375604.du.r.appspot.com","double-operator-375604.du.r.appspot.com"]

app = FastAPI() # FastAPI 모듈
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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