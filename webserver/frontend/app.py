import pandas as pd 

import streamlit as st
import folium

from streamlit_folium import st_folium
from folium import plugins

from folium.map import Marker
from jinja2 import Template

import streamlit.components.v1 as components
import copy

# from utils import project_array
# from components import get_list_component, get_detail_component
# from screen.header import header
# # from screen.map import my_map
# from screen.login import show_login
# from screen.signup import show_signup
# from screen.infra import show_infra
from screen.components import header
from screen.initial_page import show_login, show_signup,show_infra
from screen.main_page import show_main
from utils import get_example_data
from config.config import BACKEND_ADDRESS, DOMAIN_INFO, GU_INFO_CENTER,STATE_KEYS_VALS

from  SessionState import get
import requests
import json

# COORD_MULT = 1000000000 미사용 : lng, lat 실수값 그대로 사용

# if session 없으면 로그인 화면 보여준다. 

# if clicked marker 있으면 right 에 상세 정보 화면 보여준다. 

# if 찜 목록 활성화 되면 '다 지우고' 찜 목록만 보여준다. 
# 지도도 같이 보여주는게 좋을 것 같다. 
# left 는 그대로 두고, marker 뿌리고 오른쪽은 찜 목록으로 대체 


def set_state_key(STATE_KEYS_VALS,session_state):
    for k, v in STATE_KEYS_VALS:
        if k not in session_state:
            session_state[k] = v


# 초기 설정
# if 'is_login' not in session_state:
#     session_state['is_login'] = False

# if 'ex_loaction' not in session_state:
#     session_state['ex_loaction'] = None

# if 'rand_list' not in session_state:
#     session_state['rand_list'] = None

# Store the initial value of widgets in session state
# if "visibility" not in session_state:
#     session_state.visibility = "collapsed"
#     session_state.disabled = False

# if 'sidebar_state' not in session_state:
#     session_state.sidebar_state = 'collapsed'

# if 'show_detail' not in session_state:
#     session_state.show_detail = False

# if 'show_heart' not in session_state:
#     session_state.show_heart = False

# if 'show_item_list' not in session_state:
#     session_state.show_item_list = None
    

#count = 0 => 로그인
#      = 1 => 회원가입
#      = 2 => 둘러보기(인프라 선택)
#      = 3 => 지도

# if 'page_counter' not in session_state:
#     session_state.page_counter = 0

session_state = get(
        is_login=False,
        ex_loaction=None,
        rand_list=None,
        visibility='collapsed',
        disabled=False,
        sidebar_state='collapsed', 
        show_detail=False,
        show_heart=False,
        show_item_list=None,
        page_counter=0,
        cur_user_info={
            "user_id":None, 
            "user_gu":"",
        },
        ex_user_info={
            "user_id":None, 
            "user_gu":"",
        },
        center={ 'coord' : [37.4920372,127.0567124] , 'level':15},
        item_list=[],
        map_bounds={})

st.set_page_config( initial_sidebar_state = "expanded",
                    page_icon="./image/hobbang_favicon_outline.png",
                    layout="wide", 
                    page_title="당신이 선호하는 방, 호빵")

# params  = {'userid': 3, 'location': '수영구'}
# url = 'http://27.96.130.120:30002/'
#     # json.dumps(user)
# x = requests.get(url,params=params)
# print(x)
# 로그인

# set_state_key(STATE_KEYS_VALS,session_state)

if ( 0 == session_state.page_counter):
    # session_state.page_counter  값이 1 ( 회원가입 ) 또는 2 ( 인프라 ) 로 변경됨 
    # for key in session_state.keys():
    #     del session_state[key]
    # set_state_key(STATE_KEYS_VALS)
    show_login(session_state)

# 회원가입
elif ( 1 == session_state.page_counter):
    # session_state.page_counter  값이 2 ( 인프라 ) 로 변경됨 
    show_signup(session_state)

# 인프라
elif( 2 == session_state.page_counter ):
    show_infra(session_state)

# 지도
elif( 3 == session_state.page_counter ):
    # example_item_list = get_example_data()

    if(  False == session_state.show_heart):
        selected_gu = header(session_state, session_state.cur_user_info['user_gu'])
        cache_gu = session_state.cur_user_info['user_gu']
        session_state.cur_user_info['user_gu'] = selected_gu

        # Rerendering issue 방지 
        # TODO 매물이 하나도 없는 경우 오류
        if( ( ( "" != selected_gu ) and (selected_gu != cache_gu) ) or 
            ( 0 == len(session_state.item_list) ) ):
            # ( session_state['ex_user_info']['selected_gu']
            # != session_state.cur_user_info['selected_gu'])):
            # Done FT201
            # Done Data loader 선택한 지역구의 매물 정보 가져오기 
            user_info = {
                "user_id" : session_state.cur_user_info['user_id'],
                "user_gu" : session_state.cur_user_info['user_gu'],
                "house_ranking":{}
            }
            session_state.center['coord'] = [GU_INFO_CENTER[selected_gu]["lat"],GU_INFO_CENTER[selected_gu]["lng"]]
            url = ''.join([BACKEND_ADDRESS, DOMAIN_INFO['map'], DOMAIN_INFO['items']])
            res = requests.post(url,data=json.dumps(user_info) )
            session_state.item_list= [*res.json()['houses'].values()]
            session_state.show_item_list= session_state.item_list

    show_main(session_state, session_state.show_item_list)