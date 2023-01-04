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
from screen.components import get_list_component, get_detail_component, my_map, header

import copy

COORD_MULT = 1000000000

def show_main(session:dict,item_list:list):
    # print("check" , os.spath.isfile("/opt/ml/3rdproject/final_team_repo/webserver/frontend/config/user_sample.yaml") )
       # item_list = item_list[5:6] if( True == st.session_state.show_detail) else item_list
    if( None == st.session_state["show_item_list"]):
        st.session_state["show_item_list"] = copy.deepcopy(item_list)

    if(  False == st.session_state['show_heart']):
        # TODO Data loader 선택한 지역구의 매물 정보 가져오기 
        header(st.session_state)
    else : 
        # TODO Data loader 선택한 지역구의 매물 정보 가져오기 
        pass 

        st.session_state['show_detail'] = True if ( True == st.session_state['show_heart'] ) else False 
        
    st.button("내 정보")
    left, right  = st.columns([5,3])
    
    make_html = get_detail_component if( True == st.session_state.show_detail) else get_list_component

    with st.spinner():

        with left : 
            map_data = my_map(st.session_state,item_list)

            if( ( st.session_state['ex_loaction'] != map_data["last_object_clicked"] ) and 
                ( None != map_data["last_object_clicked"] ) ):
                st.session_state['show_detail'] = True
                st.session_state['ex_loaction'] = map_data["last_object_clicked"]
                compare_location = f"{map_data['last_object_clicked']['lat']},{map_data['last_object_clicked']['lng']}"
                st.session_state["show_item_list"] = list(filter(lambda item: item['location'] == compare_location, item_list))
                print(st.session_state["show_item_list"])
        
        with right:
            # Toggle sidebar state between 'expanded' and 'collapsed'.
            if (st.session_state["show_detail"] == True) :
                if ( st.button('Click to toggle sidebar state')):
                    st.session_state["show_detail"] = False
                    st.session_state["show_item_list"] = item_list

            str = '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">\
                <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>\
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>'

            for item in st.session_state["show_item_list"]: 
                str+= make_html(item)

            # bootstrap 4 collapse example
            components.html(
                str,
                height=1300,
                scrolling=True,
            )
