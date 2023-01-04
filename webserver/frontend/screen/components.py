import pandas as pd 
import folium
import streamlit as st
from streamlit_folium import st_folium
from streamlit_custom_toggle import st_custom_toggle
import streamlit.components.v1 as components
import random
from folium.map import Marker
from folium import plugins

def my_map(session:dict,items:list):
    # default center : 강남역
    center = [37.4920372,127.0567124] 
    # center on Liberty Bell, add marker
    m = folium.Map(location=center, zoom_start=10)
    # markers = plugins.MarkerCluster(transformed_coord_list )
    # markers.add_to(m) 
    with st.spinner() : 
        for item in items[:40]:
            x,y = item["location"].split(',')
            popup = folium.Popup(f"{item['description'][:100]}", min_width=200, max_width=200)
            folium.Marker(
                [x,y], popup=popup, tooltip=f"{item['title']}",icon=folium.Icon(icon = 'home', color = 'red')
            ).add_to(m)

        for item in items[40:60]:
            x,y = item["location"].split(',')
            popup = folium.Popup(f"{item['description'][:100]}", min_width=200, max_width=200)
            folium.Marker(
                [x,y], popup=popup, tooltip=f"{item['title']}",icon=folium.Icon(icon = 'home', color = 'blue')
            ).add_to(m)

        for item in items[60:]:
            x,y = item["location"].split(',')
            popup = folium.Popup(f"{item['description'][:100]}", min_width=200, max_width=200)
            folium.Marker(
                [x,y], popup=popup, tooltip=f"{item['title']}",icon=folium.Icon(icon = 'home', color = 'lightblue')
            ).add_to(m)

    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=1250,height=1250)
    return st_data


def header(session:dict):
    col1, col2, col3 = st.columns(3)
    with col1:
        option = st.selectbox(
            label = "시",
            options = ("시", "Home phone", "Mobile phone"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled
        )

    with col2:
        option = st.selectbox(
            label = "군",
            options = ("군", "Home phone", "Mobile phone"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled
        )

    with col3:
        option = st.selectbox(
            label = "구",
            options = ("구", "Home phone", "Mobile phone"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled
        )


def get_list_component( item:dict, clickevent=None):
    
    return f'<div>\
        <div style="display:inline-block;vertical-align:top;" onclick={clickevent}>\
            <img alt="" draggable="false" src={item["img"]} class="css-9pa8cd"  align="top">\
        </div>\
        <div style="display:inline-block;">\
            <div>\
                <button type="button" class="btn_grpshare" style="display:inline-block;">\
                    <span class="ico_comm ico_likebig">좋아요</span>\
                </button>\
                <div style="display:inline-block;"> {item["rank"]} </div>\
                <div> {item["title"]} </div>\
            </div>\
            <div> {item["summary"]} </div>\
            <details>\
                <summary>상세보기</summary>\
                <div> {item["description"]} </div>\
            </details>\
        </div>\
        <hr/>'


def get_detail_component( item:dict,clickevent=None ):
    
    return f'<div>\
        <div style="display:inline-block;vertical-align:top;" onclick={clickevent}>\
            <img alt="" draggable="false" src={item["img"]} class="css-9pa8cd"  align="top">\
        </div>\
        <div >\
            <div style="display:inline-block;">\
                <button type="button" class="btn_grpshare" style="display:inline-block;">\
                    <span class="ico_comm ico_likebig">좋아요</span>\
                </button>\
            </div>\
            <div style="display:inline-block;"> {item["rank"]} </div>\
        </div>\
        <div> {item["title"]} </div>\
        <div> {item["description"]} </div>\
        <hr/>'