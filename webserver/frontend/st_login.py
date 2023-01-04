import streamlit as st
import folium
from streamlit_folium import st_folium
import streamlit_authenticator as stauth    #암호 인증
import yaml
import pymysql
import folium
from streamlit_folium import st_folium

with open('user_sample.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#count = 0 => 로그인
#      = 1 => 회원가입
#      = 2 => 둘러보기(인프라 선택)
#      = 3 => 지도

if 'counter' not in st.session_state:
    st.session_state['counter'] = 0

#로그인 페이지 
if st.session_state['counter'] == 0:
    st.title('RecBang')
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        st.session_state['counter'] = 3
        st.experimental_rerun()

    elif authentication_status == False:
        st.error('아이디 혹은 비밀번호가 틀렸습니다.')

    col1, col2 = st.columns(2)

    with col1:
        if st.button("회원가입"):
            st.session_state['counter'] = 1
            st.experimental_rerun()

    with col2:
        if st.button("둘러보기"):
            st.session_state['counter'] = 2
            st.experimental_rerun()

#회원가입 페이지 이동 
elif st.session_state['counter'] == 1:
    with open('user_sample.yaml') as f:
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

                with open('user_sample.yaml', 'w') as f:
                    yaml.safe_dump(yaml_data, f)
                
                st.session_state['counter'] = 2
                st.experimental_rerun()

#인프라 선택 
elif st.session_state['counter'] == 2:
    st.title('원하는 인프라를 선택하세요 ')

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        #Infra("편의점", 1, "con_store")
        st.header("편의점")
        st.image("./image/편의점.jpeg")
        if st.checkbox("편의점" , key = 1):
            con_store = 1
        else:
            con_store = 0

    with col2:
        #Infra("약국", 2, "phar")
        st.header("약국")
        st.image("./image/약국.jpeg")
        if st.checkbox("약국" , key = 2):
            phar = 1
        else:
            phar = 0
    with col3:
        #Infra("커피숍", 3, "cafe")
        st.header("커피숍")
        st.image("./image/커피숍.jpeg")
        if st.checkbox("커피숍" , key = 3):
            cafe = 1
        else:
            cafe = 0
    with col4:
        #Infra("병원", 4, "hospital")
        st.header("병원")
        st.image("./image/병원.jpeg")
        if st.checkbox("병원" , key = 4):
            hospital = 1
        else:
            hospital = 0
    with col5:
    #     Infra("공원", 5)
        st.header("공원")
        st.image("./image/공원.jpeg")
        if st.checkbox("공원" , key = 5):
            park = 1
        else:
            park = 0

    if st.button('제출하기'):
        st.session_state['counter'] = 3
        st.experimental_rerun()

#지도 
elif st.session_state['counter'] == 3:
    m = folium.Map(location=[35.809747, 127.092337], zoom_start=16)
    folium.Marker(
        [35.809747, 127.092337], popup="추천_1", tooltip="추천_1"
    ).add_to(m)
    folium.Marker(
        [35.8, 127.09], popup="추천_2", tooltip="추천_2"
    ).add_to(m)

    st_data = st_folium(m, width = 725)

    if authenticator.logout('Logout', 'main'):
        st.session_state['counter'] = 0

# 닉네임, 이름, 이메일, 비밀번호, 나이, 지역, 폰

#돌아가기
if st.button("로그인 페이지로"):
    st.session_state['counter'] = 0
    st.experimental_rerun()
