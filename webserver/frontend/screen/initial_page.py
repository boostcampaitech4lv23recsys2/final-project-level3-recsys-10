import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit_authenticator as stauth    #암호 인증
import yaml
import pymysql
import folium
from streamlit_folium import st_folium
import requests
import bcrypt   #암호화
from datetime import datetime

import json
from config.config import BACKEND_ADDRESS, DOMAIN_INFO, GU_INFO
from screen.components import header

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
    #폼 부분
    st.title('로그인')
    with st.form("login_page"):
        user_name = st.text_input('User name')
        password_login = st.text_input('Password', type = 'password')
        #hashed_password = bcrypt.hashpw(password_login.encode('utf-8'), bcrypt.gensalt())
        hashed_password = bcrypt.hashpw(password_login.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        submit = st.form_submit_button("Login")
        if submit:
            url  = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['users'],DOMAIN_INFO['login']])

            users_login = {'name' : str(user_name),
                            'pw' : hashed_password}
                            #str(hashed_password) }

            x = requests.post(url, data=json.dumps(users_login))
            #print(msg['test'])
        #user_authentication -> 백 형식에 맞게 리퀘스트 보내기


    # name, authentication_status, username = authenticator.login('Login', 'main')

    # if True == authentication_status:
    #     session['page_counter'] = 3
    #     st.experimental_rerun()

    #     # return 3 # 지도 화면으로 전환

    # elif False == authentication_status :
    #     st.error('아이디 혹은 비밀번호가 틀렸습니다.')

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
    def disable():  
        st.session_state["disabled"] = True

    st.title("회원가입")
    with open('./config/user_sample.yaml') as f:
        yaml_data = yaml.load(f, Loader=yaml.SafeLoader)
    info = {'credentials': {'usernames' : {}}}

# 1. 이름 입력
    with st.form("same_check"):
        username = st.text_input('닉네임을 입력하세요!')
        #submitted = st.form_submit_button("중복확인")

        #if username != '' :
            #if 중복 닉네임
        info['credentials']['usernames'][username] = {'age' : {}}
        info['credentials']['usernames'][username] = {'sex' : {}}
        info['credentials']['usernames'][username] = {'locate' : {}}
        info['credentials']['usernames'][username] = {'password' : {}}

        age = st.text_input('나이를 입력하세요!')
        if age != '' :
            info['credentials']['usernames'][username]['age'] = age

        sex = st.selectbox('성별을 고르시오', ('남자', '여자'))
        #sex = st.text_input('성별을 입력하세요!     ex) 남자, 여자')
        if sex != '' :
            info['credentials']['usernames'][username]['sex'] = sex

        password = st.text_input('비밀번호를 입력하세요!', type = 'password')
        if password != '' :
            #hashed_passwords = stauth.Hasher([password]).generate()
            #hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            #st.subheader(hashed_passwords)
            #info['credentials']['usernames'][username]['password'] = hashed_passwords[0]


        # url  = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['signup']])
        # user = { 
            
        # }
        # requests.post(url, data=json.dumps(user))

        # if st.button('제출하기'):
        #     # TODO url,port config file 로 빼기

        #     # url = 'http://27.96.130.120:30002/login'
        #     # user = {
        #     #     "name" : "yujin",
        #     #     "age" : 29,
        #     #     "location":"수영구",
        #     #     "passwd": 1214
        #     # }
        #     # x = requests.post(url,data=json.dumps(user))
        #     # print(x)

        # for key, value in info['credentials']['usernames'].items():
        #     if key in yaml_data['credentials']['usernames']:
        #         yaml_data['credentials']['usernames'][key].extend(value)
        #         yaml_data['credentials']['usernames'][key] = list(set(yaml_data['credentials']['usernames'][key]))
        #     else:
        #         yaml_data['credentials']['usernames'][key] = value

        # with open('./config/user_sample.yaml', 'w') as f:
        #     yaml.safe_dump(yaml_data, f)


        submit = st.form_submit_button("제출하기")
        if submit:
            url  = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['users'],DOMAIN_INFO['join']])
            print(url)
            #x = requests.post(url,data=json.dumps(user))
            if username in yaml_data['credentials']['usernames']:
                st.error('사용중인 닉네임 입니다.')
            else:
                #print(str(hashed_passwords[0]))
                print(url)
                USERS_INFO = {'name' : str(username),
                            'pw' : str(hashed_password),
                            "user_sex" : int(0) if sex == '남자' else int(1),
                            "user_age" : int(age),
                            # "register_date" : str(datetime.now()),
                            # "update_date" : str(datetime.now()),
                            "user_type" : CHAR('Y')}
                
                print(USERS_INFO)
                # 사용 주석
                x = requests.post(url, data=json.dumps(USERS_INFO))
                session['page_counter'] = 2
                st.experimental_rerun()


"""
{'subway':'01','cs':'02','mart':'03','park':'04','cafe':'05','phar':'06','theater':'07'}
"""
def show_infra(session:dict, selected_gu:str=""):
    with st.form("show_infra_page"):
        locat = GU_INFO
        st.title('희망 거주 지역을 선택하세요 ')
        locate = header(session,selected_gu)

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

        submit = st.form_submit_button("제출하기")
        if submit:
            if check_cnt >=3:
                url = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['signup'],DOMAIN_INFO['']])
                #USERS_INFRA -> 어떻게 보낼지 확인하기 
                # USERS_INFRA = {'uesr_id' : ,
                #                'gu' : gu
                #                 'infra_type' : ,
                #                 'infra_yn' : }
                session['cur_user_info'] = {
                    "user_id" : 1,
                    "selected_gu" : locate,
                    "infra_type" : ["01","04","03"]
                }
                session['page_counter'] = 3
                st.experimental_rerun()
            else:
                st.error('3개 이상 선택하시오')




        
        # url = 'http://27.96.130.120:30002/infra'
        # infra = {
        #     "user_id" : 6,
        #     "select_infra":7
        # }
        # x = requests.post(url,data=json.dumps(infra))
        # print(x)

        
    # '''
    # 로그인
    # id, pw(hashing) -> request   -> 인프라 정보가 없다 -> 회원 인프라 선택 페이지  
    #                     -> 아이디 비밀번호가 틀리다 -> fail
    #                     -> 인프라 정보, 아이디, 비밀번호 다 ok -> Map 페이지

    # 회원가입
    # id, pw(hashing), age, sex -> request -> 아이디 중복 -> st.error('중복된 닉네임 입니다.')
    #                             -> 빈칸 -> st.error('xx을 입력하지 않으셨습니다.')
    #                             -> 정상 -> Infra Page

    # 인프라 선택
    # 회원 인프라 선택 -> request : id, pw(hashing), age, sex, gu, infra
    # 비회원 인프라 선택 -> request : id(timestamp?), gu, infra
    
    # '''