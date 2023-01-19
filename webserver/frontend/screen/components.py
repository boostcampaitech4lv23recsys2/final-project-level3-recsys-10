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
from config.config import BACKEND_ADDRESS, DOMAIN_INFO, GU_INFO,INFRA_INFO_DICT


def make_marker(items:list, start_idx:int, end_idx:int, m, marker_color:str="red", do:bool=False):
    
    for item in items[start_idx:end_idx] :
        related_item_dict = item['related_infra']
        x,y = item["lat"],item["lng"]

        popup_str = ""
        for k in related_item_dict.keys():
            popup_str += f'가장 가까운 {INFRA_INFO_DICT[k]["ko"]} : {round(related_item_dict[k]["distance"] * 1000)}m <br>'

        popup = folium.Popup(popup_str, min_width=200, max_width=200)

        folium.Marker(
                [x,y],popup=popup,icon=folium.Icon(icon = 'home', color = marker_color)
        ).add_to(m)

        if( True == do):
            for k in related_item_dict.keys():
                folium.Marker(
                    [related_item_dict[k]["lat"],related_item_dict[k]["lng"]],icon=folium.Icon(icon = f'{INFRA_INFO_DICT[k]["icon"]}', color = 'orange',prefix='fa')
                ).add_to(m)


def my_map(session:dict,items:list):
    # center on Liberty Bell, add marker
    m = folium.Map(location=session.center["coord"], zoom_start=session.center["level"]
    ,tiles = "https://map.pstatic.net/nrb/styles/basic/1673590395/{z}/{x}/{y}.png?mt=bg.ol.sw", attr = "Naver")
    # markers = plugins.MarkerCluster(transformed_coord_list )
    # markers.add_to(m) 
    with st.spinner() : 
        do = ( len(items) < 3 )  
        make_marker(items,0,20,m,'red',do)
        make_marker(items,20,80,m,'lightblue',do)
        make_marker(items,80,100,m,'lightgray',do)

        # for item in items[:40]:
        #     x,y = item["lat"],item["lng"]
        #     # print(item["lng"],item["lat"])
        #     # x,y = item["location"].split(',')
        #     popup = folium.Popup(f"{item['information']['local1']} {item['information']['local2']}", min_width=200, max_width=200)
        #     folium.Marker(
        #         [x,y],icon=folium.Icon(icon = 'home', color = 'red')
        #     ).add_to(m)

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
    
    return f'<div><a href="#" id="{item["house_id"]}_{item["lat"]}_{item["lng"]}">\
        <div style="display:inline-block;vertical-align:top;">\
            <img alt="" draggable="false" src="{cur_item_info["image_thumbnail"]}?w=400&amp;h=300&amp;q=70&amp;a=1" class="css-9pa8cd"  align="top">\
        </div>\
            <div style="display:inline-block;">\
                <a href="#" id="zzim_{item["zzim"]}_{item["house_id"]}">\
                    <i id="heart_{item["zzim"]}" class="fa fa-heart"></i>\
                </a>\
                <div style="display:inline-block; font-size:50px;"> {item["ranking"]} </div>\
                <div style="font-weight:bold;"> { cur_item_info["price_deposit"] } / { cur_item_info["price_sales"] }　{cur_item_info["address"]} </div>\
                <br>\
            </div >\
            <div> {cur_item_info["title"]} </div>\
        </a></div>\
        <hr/>'


def get_detail_component( item:dict,clickevent=None ):

    item["information"]["price_deposit"] = "문의" if item["information"]["price_deposit"] == None else item["information"]["price_deposit"] 
    item["information"]["price_sales"]   = "문의" if item["information"]["price_sales"] == None else item["information"]["price_sales"] 
    cur_item_info = item["information"]

    return f'<div>\
        <div style="display:inline-block;vertical-align:top;">\
            <img alt="" draggable="false" src="{cur_item_info["image_thumbnail"]}?w=400&amp;h=300&amp;q=70&amp;a=1" class="css-9pa8cd"  align="top">\
        </div>\
        <div >\
            <div style="display:inline-block;">\
                <a href="#" id="zzim_{item["zzim"]}_{item["house_id"]}">\
                    <i id="heart_{item["zzim"]}" class="fa fa-heart"></i>\
                </a>\
            </div>\
            <div style="display:inline-block; font-size:50px;"> {item["ranking"]} </div>\
        </div>\
        <br>\
        <div style="font-weight:bold;"> { cur_item_info["price_deposit"] } / { cur_item_info["price_sales"] }　{cur_item_info["address"]} </div>\
        <br>\
        <div> {cur_item_info["description"]}</div>\
        <hr/>'