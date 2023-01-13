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

import requests
COORD_MULT = 1000000000

# if session 없으면 로그인 화면 보여준다. 

# if clicked marker 있으면 right 에 상세 정보 화면 보여준다. 

# if 찜 목록 활성화 되면 '다 지우고' 찜 목록만 보여준다. 
# 지도도 같이 보여주는게 좋을 것 같다. 
# left 는 그대로 두고, marker 뿌리고 오른쪽은 찜 목록으로 대체 

# 초기 설정
if 'is_login' not in st.session_state:
    st.session_state['is_login'] = False

if 'ex_loaction' not in st.session_state:
    st.session_state['ex_loaction'] = None

if 'rand_list' not in st.session_state:
    st.session_state['rand_list'] = None

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "collapsed"
    st.session_state.disabled = False

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

if 'show_detail' not in st.session_state:
    st.session_state.show_detail = False

if 'show_heart' not in st.session_state:
    st.session_state.show_heart = False

if 'show_item_list' not in st.session_state:
    st.session_state.show_item_list = None
    

#count = 0 => 로그인
#      = 1 => 회원가입
#      = 2 => 둘러보기(인프라 선택)
#      = 3 => 지도

if 'page_counter' not in st.session_state:
    st.session_state['page_counter'] = 0


st.set_page_config(layout="wide")

# params  = {'userid': 3, 'location': '수영구'}
# url = 'http://27.96.130.120:30002/'
#     # json.dumps(user)
# x = requests.get(url,params=params)
# print(x)
# 로그인
if ( 0 == st.session_state['page_counter']):
    # st.session_state['page_counter']  값이 1 ( 회원가입 ) 또는 2 ( 인프라 ) 로 변경됨 
    show_login(st.session_state)

# 회원가입
elif ( 1 == st.session_state['page_counter']):
    # st.session_state['page_counter']  값이 2 ( 인프라 ) 로 변경됨 
    show_signup(st.session_state)

# 인프라
elif( 2 == st.session_state['page_counter'] ):
    show_infra(st.session_state)

# 지도
elif( 3 == st.session_state['page_counter'] ):
    example_item_list = get_example_data()

    if(  False == st.session_state['show_heart']):
        # TODO Data loader 선택한 지역구의 매물 정보 가져오기 
        header(st.session_state)
    show_main(st.session_state,example_item_list)
    pass 