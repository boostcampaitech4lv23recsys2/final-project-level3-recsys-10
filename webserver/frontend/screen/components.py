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


def make_marker(items:list, start_idx:int, end_idx:int, m, marker_color:str="red", do:bool=False,icon:str="home"):
    
    for item in items[start_idx:end_idx] :
        related_item_dict = item['related_infra']
        x,y = item["lat"],item["lng"]

        # popup_str = "<p>우리 집 주변에는</p>"
        popup_str = ""
        for k in related_item_dict.keys():
            popup_str += f' <p> {INFRA_INFO_DICT[k]["emoji"]} 가장 가까운 {INFRA_INFO_DICT[k]["ko"]} : {round(related_item_dict[k]["distance"] * 1000)}m </p>'
            # popup_str += f' <p> {INFRA_INFO_DICT[k]["emoji"]} {INFRA_INFO_DICT[k]["ko"]} : {round(related_item_dict[k]["cnt"] )} 개</p>'

        popup = folium.Popup(popup_str, min_width=200, max_width=200)

        folium.Marker(
                [x,y],popup=popup,icon=folium.Icon(icon=icon, color = marker_color)
        ).add_to(m)

        if( True == do):
            for k in related_item_dict.keys():
                folium.Marker(
                    [related_item_dict[k]["lat"],related_item_dict[k]["lng"]],tooltip =  f'{INFRA_INFO_DICT[k]["ko"]}',icon=folium.Icon(icon = f'{INFRA_INFO_DICT[k]["icon"]}', color = 'orange',prefix='fa'),
                ).add_to(m)


def my_map(session:dict,items:list):
    # center on Liberty Bell, add marker
    m = folium.Map(location=session.center["coord"], zoom_start=session.center["level"]
    ,tiles = "https://map.pstatic.net/nrb/styles/basic/1673590395/{z}/{x}/{y}.png?mt=bg.ol.sw", attr = "Naver")
    # markers = plugins.MarkerCluster(transformed_coord_list )
    # markers.add_to(m) 
    with st.spinner() : 
        do = ( len(items) == 1 ) 
        if( len(items) > 0 ):
            icon = 'thumbs-up'  if ( 0 == items[0]['ranking']) else 'home'
            make_marker(items,50,100,m,'lightgray',do)
            make_marker(items,20,50,m,'lightblue',do)
            make_marker(items,1,20,m,'red',do)
            make_marker(items,0,1,m,'orange',do,icon)

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
    st_data = st_folium(m, width=800,height=800)
    return st_data


def header(session:dict, selected_gu:str=""):

    selected_idx = ( GU_INFO.index(selected_gu) if "" != selected_gu else 0)

    option = st.selectbox(
        label = " ",
        options = GU_INFO,
        # session=session.session,
        index = selected_idx
    )

    if( option[-1] != '구'):
        option = ''

    return option


# id : house_id_위도_경도 ( 현재는 이름만 경도 위도 순으로 되어 있음 )
def get_list_component( item:dict, isZzimList=False,clickevent=None):
    item["information"]["price_deposit"] = "문의" if item["information"]["price_deposit"] == None else item["information"]["price_deposit"] 
    item["information"]["price_sales"]   = "문의" if item["information"]["price_sales"] == None else item["information"]["price_sales"] 
    cur_item_info = item["information"]
    zzim_icon = "&#128516;" if( "N" == item["zzim"]) else "&#128525;"
    rank_info = ""  if (0 == item["ranking"]) else f'Rank{item["ranking"]}'
    rank_info = "추천 매물"  if ( ( 0 == item["ranking"])   and ( False == isZzimList) ) else rank_info
    
    related_item_dict = item['related_infra']
    price_str = "전세" if  0 == cur_item_info["price_monthly_rent"] else "월세"
    
    test_devide = cur_item_info["price_deposit"] % 10000
    test_quant = cur_item_info["price_deposit"] // 10000
    deposit_str = f'{test_devide}'if  0 == test_quant else f'{test_quant}억'
    deposit_str = f'{deposit_str} {test_devide}' if ( 0 != test_quant and 0 != test_devide) else f'{deposit_str} ' 
    
    price_str = f'{price_str} {deposit_str}'
    price_str += ''if  0 == cur_item_info["price_monthly_rent"] else f'/{ cur_item_info["price_monthly_rent"] }'

    infra_str = ""
    for k in related_item_dict.keys():
            infra_str += f'{INFRA_INFO_DICT[k]["emoji"]} {round(related_item_dict[k]["distance"] * 1000)}m '

    return f'<div><a href="#" id="{item["house_id"]}_{item["lat"]}_{item["lng"]}">\
        <div style="display:inline-block;vertical-align:top;">\
            <img alt="" draggable="false" src="{cur_item_info["image_thumbnail"]}?w=400&amp;h=300&amp;q=70&amp;a=1" class="css-9pa8cd"  align="top">\
        </div>\
        <div>\
            <div style="display:inline-block;">\
                <a href="#" id="zzim_{item["zzim"]}_{item["house_id"]}">\
                    <div id="heart_{item["zzim"]}">{zzim_icon}</div>\
                </a>\
            </div >\
                <div style="display:inline-block; font-size:50px;"> {rank_info} </div>\
            </div>\
                <div style="font-weight:bold;"> { price_str} {cur_item_info["house_area"]}㎡</div>\
                <div style="font-weight:bold;"> {cur_item_info["address"]} </div>\
                <br>\
            <div> {infra_str} </div>\
        </a></div>\
        <hr/>'


def get_detail_component( item:dict,isZzimList=False,clickevent=None ):

    item["information"]["price_deposit"] = "문의" if item["information"]["price_deposit"] == None else item["information"]["price_deposit"] 
    item["information"]["price_sales"]   = "문의" if item["information"]["price_sales"] == None else item["information"]["price_sales"] 
    cur_item_info = item["information"]
    zzim_icon = "&#128516;" if( "N" == item["zzim"]) else "&#128525;"
    rank_info = ""  if (0 == item["ranking"]) else f'Rank{item["ranking"]}'

    price_str = "전세" if  0 == cur_item_info["price_monthly_rent"] else "월세"
    
    test_devide = cur_item_info["price_deposit"] % 10000
    test_quant = cur_item_info["price_deposit"] // 10000
    deposit_str = f'{test_devide}'if  0 == test_quant else f'{test_quant}억'
    deposit_str = f'{deposit_str} {test_devide}' if ( 0 != test_quant and 0 != test_devide) else f'{deposit_str} ' 
    
    price_str = f'{price_str} {deposit_str}'
    price_str += '' if  0 == cur_item_info["price_monthly_rent"] else f'/{ cur_item_info["price_monthly_rent"] }'

    return f'<div>\
        <div style="display:inline-block;vertical-align:top;">\
            <img alt="" draggable="false" src="{cur_item_info["image_thumbnail"]}?w=400&amp;h=300&amp;q=70&amp;a=1" class="css-9pa8cd"  align="top">\
        </div>\
        <div >\
            <div style="display:inline-block;">\
                <a href="#" id="zzim_{item["zzim"]}_{item["house_id"]}">\
                    <div id="heart_{item["zzim"]}">{zzim_icon}</div>\
                </a>\
            </div>\
            <div style="display:inline-block; font-size:50px;"> {rank_info} </div>\
        </div>\
        <br>\
        <div style="font-weight:bold;"> { price_str} {cur_item_info["house_area"]}㎡</div>\
        <div style="font-weight:bold;"> {cur_item_info["address"]} </div>\
        <br>\
        <div> {cur_item_info["description"]}</div>\
        <hr/>'