import pandas as pd 

import streamlit as st

# from screen.header import header
# from screen.map import my_map
from screen.components import logout,get_list_component, get_detail_component, my_map, header

from config.config import BACKEND_ADDRESS, DOMAIN_INFO
from st_click_detector import click_detector
import copy

print(BACKEND_ADDRESS)
print(DOMAIN_INFO)
COORD_MULT = 1000000000

def show_main(session:dict,item_list:list):
    # print("check" , os.spath.isfile("/opt/ml/3rdproject/final_team_repo/webserver/frontend/config/user_sample.yaml") )
    # item_list = item_list[5:6] if( True == session.show_detail) else item_list
    # show_item_list 는 item_list 로 초기화된다. 
    if( None == session["show_item_list"]):
        session["show_item_list"] = copy.deepcopy(item_list)

    if 'center' not in session:
        session.center = [37.4920372,127.0567124] 

    choice = st.selectbox(
    '유저',
    ('전체보기','관심 목록', '인프라 변경'),
    label_visibility=session.visibility)
    
    # TODO: logout 버튼 클릭 후 새로 고침해야하는 문제 있음 
    logout(session)

    if( '관심 목록'== choice ):
        # TODO FT301
        # TODO 찜 목록 요청 
        # params = {
        #     user_id : st.session_state['cur_user_info']['user_id'],

        # }
        # url = ''.join([BACKEND_ADDRESS, DOMAIN_INFO['zzim'], DOMAIN_INFO['items']])
        # res = requests.get(url,params=params )
        # pass
        session['show_heart'] = True
        
    elif('인프라 변경'== choice):
        session['page_counter'] = 2
        st.experimental_rerun()
        pass
    
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

                # TODO FT401
                # TODO Marker 내 매물 클릭 
                # params = {
                #     user_id : st.session_state['cur_user_info']['user_id'],

                # }
                # url = ''.join([BACKEND_ADDRESS, DOMAIN_INFO['map'], DOMAIN_INFO['click']])
                # res = requests.get(url,params=params )
                # pass
        
        with right:
            # detail 한 정보를 보여주는 상태일 때 
            if (session["show_detail"] == True) :
                # 돌아가기 버튼을 클릭하면 show_item_list 를 item_list 로 다시 교체
                if ( st.button('상세 목록 돌아가기')):
                    session["show_detail"] = False
                    session["show_item_list"] = item_list

            str = '\
            <link href="https://hangeul.pstatic.net/hangeul_static/css/nanum-square-neo.css" rel="stylesheet" " crossorigin="anonymous">\
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">\
            <link rel="stylesheet" href="css_basic.css">\
                <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>\
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>\
                <div style="overflow-y: scroll; height:1500px;">'
            # 실행 순서상 아래 str 만드는 for 문 바로 위에 있어야 함 
            make_html = get_detail_component if( True == session.show_detail) else get_list_component

            for item in session["show_item_list"]: 
                str+= make_html(item)
            str+= "</div>"
            clicked = click_detector(str)

            if( "" != clicked and "love"!=clicked[:4]):
                # TODO FT402
                # TODO List 내 매물클릭 
                # params = {
                #     user_id : st.session_state['cur_user_info']['user_id'],

                # }
                # url = ''.join([BACKEND_ADDRESS, DOMAIN_INFO['map'], DOMAIN_INFO['click']])
                # res = requests.get(url,params=params )
                # pass
                
                session["show_detail"] = True
                session["show_item_list"] = list(filter(lambda item: item['location'] == clicked, item_list))
                session["center"] = clicked.split(',')

            # st.markdown(f"**{clicked} clicked**" if clicked != "" else "**No click**")

            # # bootstrap 4 collapse example
            # components.html(
            #     str,
            #     height=1300,
            #     scrolling=True,
            # )
