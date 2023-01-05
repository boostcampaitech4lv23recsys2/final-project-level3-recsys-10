import pandas as pd 

import streamlit as st
import folium

from streamlit_folium import st_folium
from folium import plugins

from utils import project_array

from folium.map import Marker
from jinja2 import Template

# from screen.header import header
# from screen.map import my_map
import streamlit.components.v1 as components
from screen.components import logout,get_list_component, get_detail_component, my_map, header

import copy

COORD_MULT = 1000000000

def show_main(session:dict,item_list:list):
    # print("check" , os.spath.isfile("/opt/ml/3rdproject/final_team_repo/webserver/frontend/config/user_sample.yaml") )
       # item_list = item_list[5:6] if( True == session.show_detail) else item_list
    # show_item_list 는 item_list 로 초기화된다. 
    if( None == session["show_item_list"]):
        session["show_item_list"] = copy.deepcopy(item_list)

    if(  False == session['show_heart']):
        # TODO Data loader 선택한 지역구의 매물 정보 가져오기 
        header(session)
    else : 
        # TODO Data loader 선택한 지역구의 매물 정보 가져오기 
        pass 


    choice = st.selectbox(
    '유저',
    ('전체보기','관심 목록'),
    label_visibility=session.visibility)
    
    # TODO: logout 버튼 클릭 후 새로 고침해야하는 문제 있음 
    logout(session)

    if( '관심 목록'== choice ):
        # TODO : 찜 목록 요청 
        session['show_heart'] = True
    elif('로그 아웃'== choice):
        # TODO : 서버에 요청  
        pass
    else : 
        session['show_heart'] = False
    
    # 관심 목록은 detail 한 것을 보여준다. 
    session['show_detail'] = True if ( True == session['show_heart'] ) else session['show_detail']  

    left, right  = st.columns([5,3])
    

    with st.spinner():

        with left : 
            map_data = my_map(session,item_list)
            
            # 클릭된 좌표가 이전 것과 같지 않고, 클릭된 것이 있을 때 
            # detail 한 정보를 보여준다. 
            if( ( session['ex_loaction'] != map_data["last_object_clicked"] ) and 
                ( None != map_data["last_object_clicked"] ) ):
                session['show_detail'] = True
                session['ex_loaction'] = map_data["last_object_clicked"]
                compare_location = f"{map_data['last_object_clicked']['lat']},{map_data['last_object_clicked']['lng']}"
                session["show_item_list"] = list(filter(lambda item: item['location'] == compare_location, item_list))
                print(session["show_item_list"])
        
        with right:
            # detail 한 정보를 보여주는 상태일 때 
            print("ho" , session["show_detail"] )
            if (session["show_detail"] == True) :
                # 돌아가기 버튼을 클릭하면 show_item_list 를 item_list 로 다시 교체
                if ( st.button('상세 목록 돌아가기')):
                    session["show_detail"] = False
                    session["show_item_list"] = item_list

            str = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">\
                <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>\
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>'

            # 실행 순서상 아래 str 만드는 for 문 바로 위에 있어야 함 
            make_html = get_detail_component if( True == session.show_detail) else get_list_component

            for item in session["show_item_list"]: 
                str+= make_html(item)

            # bootstrap 4 collapse example
            components.html(
                str,
                height=1300,
                scrolling=True,
            )
