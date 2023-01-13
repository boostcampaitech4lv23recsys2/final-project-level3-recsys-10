import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit_authenticator as stauth    #암호 인증
import yaml
import pymysql
import folium
from streamlit_folium import st_folium
import requests

import json
from config.config import BACKEND_ADDRESS, DOMAIN_INFO, GU_INFO

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
        st.experimental_rerun()

        # return 3 # 지도 화면으로 전환

    elif False == authentication_status :
        st.error('아이디 혹은 비밀번호가 틀렸습니다.')

    col1, col2 = st.columns(2)
    # print(session['page_counter'])

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

            locat = GU_INFO
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
                # TODO url,port config file 로 빼기

                # url = 'http://27.96.130.120:30002/login'
                # user = {
                #     "name" : "yujin",
                #     "age" : 29,
                #     "location":"수영구",
                #     "passwd": 1214
                # }
                # x = requests.post(url,data=json.dumps(user))
                # print(x)

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





def show_infra(session:dict):

    locat = GU_INFO
    st.title('희망 거주 지역을 선택하세요 ')
    locate = st.selectbox(' ',locat)

    st.title('원하는 인프라를 선택하세요 (3개 이상) ')

    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)
    check_cnt = 0

    with col1:
        st.header("편의점")
        st.image("./image/편의점.jpeg")
        if st.checkbox("편의점" , key = 1):
            con_store = 1
            check_cnt += 1
        else:
            con_store = 0
            
    with col2:
        st.header("약국")
        st.image("./image/약국.jpeg")
        if st.checkbox("약국" , key = 2):
            phar = 1
            check_cnt += 1
        else:
            phar = 0

    with col3:
        st.header("카페")
        st.image("./image/카페.jpeg")
        if st.checkbox("카페" , key = 3):
            cafe = 1
            check_cnt += 1
        else:
            cafe = 0

    with col4:
        st.header("병원")
        st.image("./image/병원.jpeg")
        if st.checkbox("병원" , key = 4):
            hospital = 1
            check_cnt += 1
        else:
            hospital = 0

    with col5:
        st.header("공원")
        st.image("./image/공원.jpeg")
        if st.checkbox("공원" , key = 5):
            park = 1
            check_cnt += 1
        else:
            park = 0

    with col6:
        st.header("대형마트")
        st.image("./image/대형마트.jpeg")
        if st.checkbox("대형마트" , key = 6):
            mart = 1
            check_cnt += 1
        else:
            mart = 0

    with col7:
        st.header("영화관")
        st.image("./image/영화관.jpeg")
        if st.checkbox("영화관" , key = 7):
            theater = 1
            check_cnt += 1
        else:
            theater = 0

    with col8:
        st.header("지하철")
        st.image("./image/지하철.jpeg")
        if st.checkbox("지하철" , key = 8):
            subway = 1
            check_cnt += 1
        else:
            subway = 0

    if check_cnt >= 3:
        if st.button('제출하기'):
            session['page_counter'] = 3
            print(check_cnt)
            st.experimental_rerun()
    else:
        st.button('제출하기', disabled = True)
        print(check_cnt)




        
        # url = 'http://27.96.130.120:30002/infra'
        # infra = {
        #     "user_id" : 6,
        #     "select_infra":7
        # }
        # x = requests.post(url,data=json.dumps(infra))
        # print(x)

        