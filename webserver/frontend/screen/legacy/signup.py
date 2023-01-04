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

def show_signup(session:dict):
    with open('./config/user_sample.yaml') as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
    info = {'credentials': {'usernames' : {}}}
    # 1. 이름 입력
    username = st.text_input('닉네임을 입력하세요!')
    if username in yaml_data['credentials']['usernames']:
        st.error('사용중인 닉네임 입니다.')
    else:
        if username != '' :
            #if 중복 닉네임
            info['credentials']['usernames'][username] = {'name' : {}}
            info['credentials']['usernames'][username] = {'age' : {}}
            info['credentials']['usernames'][username] = {'sex' : {}}
            info['credentials']['usernames'][username] = {'locate' : {}}
            info['credentials']['usernames'][username] = {'password' : {}}

            name = st.text_input('이름을 입력하세요!')
            if name != '' :
                info['credentials']['usernames'][username]['name'] = name
                
            age = st.text_input('나이를 입력하세요!')
            if age != '' :
                info['credentials']['usernames'][username]['age'] = age

            sex = st.selectbox('성별을 고르시오', ('남자', '여자'))
            #sex = st.text_input('성별을 입력하세요!     ex) 남자, 여자')
            if sex != '' :
                info['credentials']['usernames'][username]['sex'] = sex

            locat = ['강남구','마포구','용산구','영등포구','양천구','중랑구','동대문구','성동구']
            locate = st.selectbox('지역을 선택하세요!', locat)
            #st.title(locate)
            #locate = st.text_input('지역을 입력하세요!  ex) xx구')
            if locate != '' :
                info['credentials']['usernames'][username]['locate'] = locate
                
            password = st.text_input('비밀번호를 입력하세요!', type = 'password')
            if password != '' :
                hashed_passwords = stauth.Hasher([password]).generate()
                #st.subheader(hashed_passwords)
                info['credentials']['usernames'][username]['password'] = hashed_passwords[0]

            if st.button('제출하기'):
                for key, value in info['credentials']['usernames'].items():
                    if key in yaml_data['credentials']['usernames']:
                        yaml_data['credentials']['usernames'][key].extend(value)
                        yaml_data['credentials']['usernames'][key] = list(set(yaml_data['credentials']['usernames'][key]))
                    else:
                        yaml_data['credentials']['usernames'][key] = value

                with open('./config/user_sample.yaml', 'w') as f:
                    yaml.safe_dump(yaml_data, f)
                session['page_counter'] = 2
                st.experimental_rerun()

