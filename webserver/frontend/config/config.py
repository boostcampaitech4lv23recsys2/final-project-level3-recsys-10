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
        "users":"/users",
        "join":"/join", # FT101, FT102
        "infra":"/infra", # FT103
        "login":"/login", # FT104
        "name":"/name", # FT106
        "map":"/map", 
        "items":"/items", # FT201,
        "zoom":"/zoom", # FT202
        "zzim":"/zzim",
        "register":"/register", # FT302
        "unregister":"/unregister", # FT303
        "click":"/click", # FT401, FT402
    },
    "location":{
        "si":[],
        "gun":[],
        "gu":['강남구','강동구','강서구','강북구','관악구','광진구','구로구','금천구','노원구',
            '동대문구','도봉구','동작구','마포구','서대문구','성동구','성북구','서초구','송파구',
            '영등포구','용산구','양천구','은평구','종로구','중구','중랑구']
    },

    # 230117 backend {'subway':'01','cs':'02','mart':'03','park':'04','cafe':'05','phar':'06','theater':'07'}    
    "infra":{
        '지하철':{
            "en":"subway",
            "ko":"지하철",
            "code":"01",
            "img" : ""
        },
        '편의점':{
            "en":"convenience store",
            "ko":"편의점",
            "code":"02",
            "img" : ""
        },
        '대형마트':{
            "en":"mart",
            "ko":"대형마트",
            "code":"03",
            "img" : ""
        },
        '공원':{
            "en":"park",
            "ko":"공원",
            "code":"04",
            "img" : ""
        },
        '카페':{
            "en":"cafe",
            "ko":"카페",
            "code":"05",
            "img" : ""
        },
        '약국':{
            "en":"pharmacy",
            "ko":"약국",
            "code":"06",
            "img" : ""
        },
        '영화관':{
            "en":"theater",
            "ko":"영화관",
            "code":"07",
            "img" : ""
        },
    }
}

BACKEND_ADDRESS = f'{setting["backend"]["protocol"]}{setting["backend"]["address"]}:{setting["backend"]["port"]}'
DOMAIN_INFO = setting["domain"] 
GU_INFO = setting["location"]["gu"] 