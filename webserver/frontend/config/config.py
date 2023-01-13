import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

setting = {
    "frontend":{
        "protocol": os.getenv('PROTOCOL'),
        "address":"0.0.0.0",
        "port":"30001"
    },
    "backend":{
        "protocol":os.getenv('PROTOCOL'),
        "address": os.getenv('BACKEND_IP'),
        "port": os.getenv('BACKEND_PORT')
    },
    "domain":{
        "login":"/login"
    },
    "location":{
        "si":[],
        "gun":[],
        "gu":['강남구','강동구','강서구','강북구','관악구','광진구','구로구','금천구','노원구',
            '동대문구','도봉구','동작구','마포구','서대문구','성동구','성북구','서초구','송파구',
            '영등포구','용산구','양천구','은평구','종로구','중구','중랑구']
    }
}

BACKEND_ADDRESS = f'{setting["backend"]["protocol"]}{setting["backend"]["address"]}:{setting["backend"]["port"]}'
DOMAIN_INFO = setting["domain"] 
GU_INFO = setting["location"]["gu"]