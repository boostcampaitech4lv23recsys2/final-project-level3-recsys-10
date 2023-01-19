import pandas as pd 
import folium
import streamlit as st
from streamlit_folium import st_folium
from streamlit_custom_toggle import st_custom_toggle
import streamlit.components.v1 as components
import random
from folium.map import Marker
from folium import plugins
import yaml
import streamlit_authenticator as stauth    #암호 인증
from config.config import BACKEND_ADDRESS, DOMAIN_INFO, GU_INFO

def my_map(session:dict,items:list):
    # center on Liberty Bell, add marker
    m = folium.Map(location=session.center, zoom_start=15)
    # markers = plugins.MarkerCluster(transformed_coord_list )
    # markers.add_to(m) 
    with st.spinner() : 
        for item in items[:40]:
            x,y = item["lng"],item["lat"]
            # print(item["lng"],item["lat"])
            # x,y = item["location"].split(',')
            popup = folium.Popup(f"{item['information']['local1']} {item['information']['local2']}", min_width=200, max_width=200)
            folium.Marker(
                [x,y],icon=folium.Icon(icon = 'home', color = 'red')
            ).add_to(m)

        # for item in items[40:60]:
        #     x,y = item["lng"],item["lat"]
        #     # print(item["lng"],item["lat"])
        #     x,y = item["location"].split(',')
        #     popup = folium.Popup(f"{item['local1']} {item['local2']}", min_width=200, max_width=200)
        #     folium.Marker(
        #         [x,y], popup=popup, tooltip=f"{item['title']}",icon=folium.Icon(icon = 'home', color = 'lightgray')
        #     ).add_to(m)

        # for item in items[60:]:
        #     x,y = item["lng"],item["lat"]
        #     # x,y = item["location"].split(',')
        #     popup = folium.Popup(f"{item['description'][:100]}", min_width=200, max_width=200)
        #     folium.Marker(
        #         [x,y], popup=popup, tooltip=f"{item['title']}",icon=folium.Icon(icon = 'home', color = 'lightblue')
        #     ).add_to(m)

    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=1250,height=1250)
    return st_data


def header(session:dict, selected_gu:str=""):

    selected_idx = ( GU_INFO.index(selected_gu) if "" != selected_gu else 0)

    option = st.selectbox(
        label = "구",
        options = GU_INFO,
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        index = selected_idx
    )

    return option


def logout(session:dict):
    with open('./config/user_sample.yaml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    authenticator.logout('Logout', 'main')

# id : house_id_위도_경도 ( 현재는 이름만 경도 위도 순으로 되어 있음 )
def get_list_component( item:dict, clickevent=None):
        
    item["information"]["price_deposit"] = "문의" if item["information"]["price_deposit"] == None else item["information"]["price_deposit"] 
    item["information"]["price_sales"]   = "문의" if item["information"]["price_sales"] == None else item["information"]["price_sales"] 
    cur_item_info = item["information"]
    
    return f'<div><a href="#" id="{item["house_id"]}_{item["lng"]}_{item["lat"]}">\
        <div style="display:inline-block;vertical-align:top;">\
            <img alt="" draggable="false" src="https://ic.zigbang.com/ic/items/34463020/1.jpg?w=400&amp;h=300&amp;q=70&amp;a=1" class="css-9pa8cd"  align="top">\
        </div>\
            <div style="display:inline-block;">\
                <a href="#" id="zzim_{item["zzim"]}_{item["house_id"]}">\
                    <i id="heart_{item["zzim"]}" class="fa fa-heart"></i>\
                </a>\
                <div style="display:inline-block; font-size:50px;"> {item["ranking"]} </div>\
                <div> { cur_item_info["price_deposit"] } / { cur_item_info["price_sales"] } item[title] 자리입니다." </div>\
            </div>\
            <div> "item[summary] 자리입니다." </div>\
        </a></div>\
        <hr/>'


def get_detail_component( item:dict,clickevent=None ):
    
    item["information"]["price_deposit"] = "문의" if item["information"]["price_deposit"] == None else item["information"]["price_deposit"] 
    item["information"]["price_sales"]   = "문의" if item["information"]["price_sales"] == None else item["information"]["price_sales"] 
    cur_item_info = item["information"]

    return f'<div>\
        <div style="display:inline-block;vertical-align:top;">\
            <img alt="" draggable="false" src="https://ic.zigbang.com/ic/items/34463030/1.jpg?w=400&amp;h=300&amp;q=70&amp;a=1" class="css-9pa8cd"  align="top">\
        </div>\
        <div >\
            <div style="display:inline-block;">\
                <a href="#" id="zzim_{item["zzim"]}_{item["house_id"]}">\
                    <i id="heart_{item["zzim"]}" class="fa fa-heart"></i>\
                </a>\
            </div>\
            <div style="display:inline-block;"> {item["ranking"]} </div>\
        </div>\
        <div> "item[title] 자리입니다." </div>\
        <div> { cur_item_info["price_deposit"] } / { cur_item_info["price_sales"] } item[title] 자리입니다." </div>\
        <div> "item[description] 자리입니다."</div>\
        <hr/>'