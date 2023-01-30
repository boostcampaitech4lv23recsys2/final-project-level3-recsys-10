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
        "gu":{
            "name_list": ['원하는 구를 선택하세요.','강남구','강동구','강서구','강북구','관악구','광진구','구로구','금천구','노원구',
            '동대문구','도봉구','동작구','마포구','서대문구','성동구','성북구','서초구','송파구',
            '영등포구','용산구','양천구','은평구','종로구','중구','중랑구'],
            "center_code": { 
                "종로구":{"code:":11110,"lng":126.9773213,"lat":37.59491732}
                ,"중구":{"code:":11140,"lng":126.9959681,"lat":37.56014356}
                ,"용산구":{"code:":11170,"lng":126.979907 ,"lat":37.53138497}
                ,"성동구":{"code:":11200,"lng":127.0410585,"lat":37.55102969}
                ,"광진구":{"code:":11215,"lng":127.0857435,"lat":37.54670608}
                ,"동대문구":{"code:":11230,"lng":127.0548481,"lat":37.58195655}
                ,"중랑구":{"code:":11260,"lng":127.0928803,"lat":37.59780259}
                ,"성북구":{"code:":11290,"lng":127.0175795,"lat":37.6057019 }
                ,"강북구":{"code:":11305,"lng":127.011189 ,"lat":37.64347391}
                ,"도봉구":{"code:":11320,"lng":127.0323688,"lat":37.66910208}
                ,"노원구":{"code:":11350,"lng":127.0750347,"lat":37.65251105}
                ,"은평구":{"code:":11380,"lng":126.9270229,"lat":37.61921128}
                ,"서대문구":{"code:":11410,"lng":126.9390631,"lat":37.57778531}
                ,"마포구":{"code:":11440,"lng":126.90827  ,"lat":37.55931349}
                ,"양천구":{"code:":11470,"lng":126.8554777,"lat":37.52478941}
                ,"강서구":{"code:":11500,"lng":126.822807 ,"lat":37.56123543}
                ,"구로구":{"code:":11530,"lng":126.8563006,"lat":37.49440543}
                ,"금천구":{"code:":11545,"lng":126.9008202,"lat":37.46056756}
                ,"영등포구":{"code:":11560,"lng":126.9101695,"lat":37.52230829}
                ,"동작구":{"code:":11590,"lng":126.9516415,"lat":37.49887688}
                ,"관악구":{"code:":11620,"lng":126.9453372,"lat":37.46737569}
                ,"서초구":{"code:":11650,"lng":127.0312203,"lat":37.47329547}
                ,"강남구":{"code:":11680,"lng":127.0629852,"lat":37.49664389}
                ,"송파구":{"code:":11710,"lng":127.115295 ,"lat":37.50561924}
                ,"강동구":{"code:":11740,"lng":127.1470118,"lat":37.55045024}
            }
        }
    },

    # 230117 backend {'subway':'01','cs':'02','mart':'03','park':'04','cafe':'05','phar':'06','theater':'07'}    
    "infra":{
        '01':{
            "en":"subway",
            "ko":"지하철",
            "code":"01",
            "img":"",
            "icon":"subway",
            "emoji":"&#128650;",
        },
        '02':{
            "en":"convenience store",
            "ko":"편의점",
            "code":"02",
            "img":"",
            "icon":"shopping-basket",
            "emoji":"&#127857;",
        },
        '03':{
            "en":"mart",
            "ko":"대형마트",
            "code":"03",
            "img" : "",
            "icon":"shopping-cart",
            "emoji":"&#128717;",
        },
        '04':{
            "en":"park",
            "ko":"공원",
            "code":"04",
            "img" : "",
            "icon":"futbol-o",
            "emoji":"&#128054;",
        },
        '05':{
            "en":"cafe",
            "ko":"카페",
            "code":"05",
            "img" : "",
            "icon":"coffee",
            "emoji":"&#127849;",
        },
        '06':{
            "en":"pharmacy",
            "ko":"약국",
            "code":"06",
            "img" : "",
            "icon":"ambulance",
            "emoji":"&#128138;",
        },
        '07':{
            "en":"theater",
            "ko":"영화관",
            "code":"07",
            "img" : "",
            "icon":"film",
            "emoji":"&#127916;",
        },
    },
    "2infra":
        [ {
            "en":"subway",
            "ko":"지하철",
            "code":"01",
            "img":"",
            "icon":"subway",
        },
        {
            "en":"convenience store",
            "ko":"편의점",
            "code":"02",
            "img":"",
            "icon":"shopping-basket",
        },
        {
            "en":"mart",
            "ko":"대형마트",
            "code":"03",
            "img" : "",
            "icon":"shopping-cart",
        },
        {
            "en":"park",
            "ko":"공원",
            "code":"04",
            "img" : "",
            "icon":"futbol-o",
        },
        {
            "en":"cafe",
            "ko":"카페",
            "code":"05",
            "img" : "",
            "icon":"coffee",
        },
        {
            "en":"pharmacy",
            "ko":"약국",
            "code":"06",
            "img" : "",
            "icon":"ambulance",
        },
        {
            "en":"theater",
            "ko":"영화관",
            "code":"07",
            "img" : "",
            "icon":"film",
        }
    ],
    "state_key":[
        ("is_login", False),
        ("ex_loaction", None),
        ("rand_list",None),
        ("visibility",'collapsed'),
        ('disabled',False),
        ('sidebar_state','collapsed'), 
        ('show_detail',False),
        ('show_heart', False),
        ('show_item_list',None),
        ('page_counter',0),
        ('cur_user_info',{
            "user_id":None, 
            "user_gu":"",
        }),
        ('ex_user_info',{
            "user_id":None, 
            "user_gu":"",
        }),
        ('center',{ 'coord' : [37.4920372,127.0567124] , 'level':15}),
        ('item_list',[]),
        ('page_counter',0),
        ('map_bounds',{}),
        ]
}

BACKEND_ADDRESS = f'{setting["backend"]["protocol"]}{setting["backend"]["address"]}:{setting["backend"]["port"]}'
DOMAIN_INFO = setting["domain"] 
GU_INFO = setting["location"]["gu"]["name_list"]
GU_INFO_CENTER = setting["location"]["gu"]["center_code"]
# INFRA_INFO = [*setting["infra"].values()]
INFRA_INFO = [*setting["infra"].values()]
INFRA_INFO_DICT= setting["infra"]
STATE_KEYS_VALS = setting["state_key"]