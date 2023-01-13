import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit_authenticator as stauth    #암호 인증
import yaml
import pymysql
import folium
from streamlit_folium import st_folium

import os.path

#count = 0 => 로그인
#      = 1 => 회원가입
#      = 2 => 둘러보기(인프라 선택)
#      = 3 => 지도

def show_login(session:dict):
    # print(os.getcwd())
    # print("check" , os.spath.isfile("/opt/ml/3rdproject/final_team_repo/webserver/frontend/config/user_sample.yaml") )
    with open('./config/user_sample.yaml') as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
    )

    st.title('RecBang')
    name, authentication_status, username = authenticator.login('Login', 'main')

    if True == authentication_status:
        session['page_counter'] = 3
        # return 3 # 지도 화면으로 전환

    elif False == authentication_status :
        st.error('아이디 혹은 비밀번호가 틀렸습니다.')

    col1, col2 = st.columns(2)

    with col1:
        if st.button("회원가입"):
            session['page_counter'] = 1
            st.experimental_rerun()
            # return 1 # 회원가입

    with col2:
        if st.button("둘러보기"):
            session['page_counter'] = 2
            st.experimental_rerun()
            # return 2 # infra 선택 화면으로 전환 