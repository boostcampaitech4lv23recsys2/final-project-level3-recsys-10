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
from config.config import BACKEND_ADDRESS, DOMAIN_INFO, GU_INFO, INFRA_INFO
from screen.components import header

#count = 0 => 로그인
#      = 1 => 회원가입
#      = 2 => 둘러보기(인프라 선택)
#      = 3 => 지도

# id = drop
# pw = 1234

def show_login(session:dict):
    # print(os.getcwd())
    # print("check" , os.spath.isfile("/opt/ml/3rdproject/final_team_repo/webserver/frontend/config/user_sample.yaml") )
    st.image("./image/hobbang_banner_outline.png",width = 600)
    #폼 부분
    with st.form("login_page"):
        user_name = st.text_input('User name')
        password_login = st.text_input('Password', type = 'password')
        #password_login = password_login.
        #hashed_password = bcrypt.hashpw(password_login.encode('utf-8'), bcrypt.gensalt())
        #hashed_password = bcrypt.hashpw(password_login.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        submit = st.form_submit_button("Login")
        if submit:
            try:
                url  = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['users'],DOMAIN_INFO['login']])

                users_login = {'name' : str(user_name),
                                'pw' : str(password_login)}

                x = requests.post(url, data=json.dumps(users_login))
                check = x.json()
                print(check)

                session.cur_user_info['user_id'] = check['user_id']
                session.cur_user_info['user_gu'] = check['user_gu']

                if check["user_gu"] == None and check['msg'] == "로그인에 성공했습니다.":
                    session.page_counter = 2 #Infra Page
                    st.experimental_rerun()

                elif check["user_gu"] != '' and check['msg'] == "로그인에 성공했습니다.":
                    session.page_counter = 3 #Map Page
                    st.experimental_rerun()

                elif check['msg'] ==  '아이디 혹은 비밀번호가 일치하지 않습니다.':
                    st.error(f'아이디 혹은 비밀번호가 일치하지 않습니다.')
            except Exception as e:
                st.error(f'아이디 혹은 비밀번호를 입력해주세요.')

    # name, authentication_status, username = authenticator.login('Login', 'main')

    # if True == authentication_status:
    #     session.page_counter = 3
    #     st.experimental_rerun()

    #     # return 3 # 지도 화면으로 전환

    # elif False == authentication_status :
    #     st.error('아이디 혹은 비밀번호가 틀렸습니다.')

    col1, col2 = st.columns(2)
    # print(session.page_counter)

    with col1:
        if st.button("회원가입"):
            session.page_counter = 1
            st.experimental_rerun()
            # return 1 # 회원가입

    with col2:
        pass
        # if st.button("둘러보기"):
        #     url  = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['users'],DOMAIN_INFO['join']])
        #     USERS_INFO = {'name' : str(datetime.now().timestamp()),
        #                   'pw' : None,
        #                   'user_sex' : None,
        #                   'user_age' : None,
        #                   'user_type' : str('N')}
            
        #     x = requests.post(url, data=json.dumps(USERS_INFO))
        #     check = x.json()
        #     session.cur_user_info['user_id'] = check['user_id'] 

        #     session.page_counter = 2
        #     st.experimental_rerun()
            # return 2 # infra 선택 화면으로 전환 


def show_signup(session:dict):

    def validation_submit_user_info(user_info:dict):

        if( ( '' == user_info['name'] ) or
            ( '' == user_info['pw'] ) or
            ( True == ( user_info['user_sex'] not in ['남자','여자'] ) ) or
            (  user_info['user_age'] < 1920 and user_info['user_age'] > 2006 ) ) : 
            
            return False         

        return True 

    st.title("회원가입")
    submit_user_info = {
        "name":"",
        "pw":"",
        "user_sex":0,
        "user_age":0,
        "user_type": 'Y',
    }

    age_list = [age for age in range(2006, 1920,-1)]
    #age_list.insert(0,'나이를 선택하세요.')

# 1. 이름 입력
    with st.form("same_check"):
        submit_user_info['name'] = st.text_input('닉네임을 입력하세요!')
        
        #submitted = st.form_submit_button("중복확인")

        #if username != '' :
            #if 중복 닉네임
       
        submit_user_info['user_age'] = int(st.selectbox('출생연도를 선택하세요!',age_list))
        # age = st.text_input('나이를 입력하세요!')
        # if age != '' :
        #     submit_user_info['age'] = int(age)

        submit_user_info['user_sex'] = st.selectbox('성별을 고르시오', ('남자', '여자'))
        #sex = st.text_input('성별을 입력하세요!     ex) 남자, 여자')

        submit_user_info['pw'] = st.text_input('비밀번호를 입력하세요!', type = 'password')

        if submit_user_info['pw'] != '' :
            #hashed_passwords = stauth.Hasher([password]).generate()
            #hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = bcrypt.hashpw(submit_user_info['pw'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            submit_user_info['pw'] = hashed_password

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
            session.page_counter = 2
            st.experimental_rerun()
            # if False == validation_submit_user_info(submit_user_info) : 
            #     st.error("정보가 올바르지 않습니다. 모든 정보를 확인해주세요.")
            # # url  = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['users'],DOMAIN_INFO['name'],"/",str(username)])
            # else : 
            #     url  = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['users'],DOMAIN_INFO['name'], '/',submit_user_info['name']])
            #     name_check_res = requests.get(url)
            #     name_check_val = name_check_res.json()

            #     if name_check_val['res'] == "중복된 이름이 있습니다":
            #         st.error('중복된 이름이 있습니다. 닉네임을 확인해주세요.')

            #     elif name_check_val['res'] == "사용할 수 있는 이름입니다":
            #         url  = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['users'],DOMAIN_INFO['join']])
            #         # USERS_INFO = {'name' : str(username),
            #         #                 'pw' : str(hashed_password),
            #         #                 'user_sex' : int(0) if sex == '남자' else int(1),
            #         #                 'user_age' : int(age),
            #         #                 'user_type' : str('Y')}
            #         submit_user_info['user_sex'] =  0 if submit_user_info['user_sex'] == '남자' else 1
            #         submit_user_info['user_type'] = 'Y'
            #         join_check_res = requests.post(url, data=json.dumps(submit_user_info))
            #         join_check_val = join_check_res.json()
            #         session.cur_user_info['user_id'] = join_check_val['user_id'] 
            #         session.page_counter = 2
            #         st.experimental_rerun()

            #x = requests.post(url,data=json.dumps(user))
            # if username in yaml_data['credentials']['usernames']:
            #     st.error('사용중인 닉네임 입니다.')
            # else:
                #print(str(hashed_passwords[0]))


"""
{'subway':'01','cs':'02','mart':'03','park':'04','cafe':'05','phar':'06','theater':'07'}
"""
def show_infra(session:dict, selected_gu:str="",user_type:int=0):
    with st.form("show_infra_page"):
        locat = GU_INFO
        st.title('희망 거주 지역을 선택하세요 ')
        locate = header(session,selected_gu)
        st.title('원하는 인프라를 선택하세요 (3개 이상) ')

        num_of_infra = len(INFRA_INFO)
        quotient  = num_of_infra // 2 
        remainder = num_of_infra % 2 

        upper_col_list = st.columns(quotient + remainder)
        lower_col_list = st.columns(quotient)
        col_list = upper_col_list + lower_col_list

        check_cnt = 0 
        select_list = [False] * ( num_of_infra + 1 ) 

        # make_colum_by_infra(upper_col_list,check_cnt,select_infra)
        # make_colum_by_infra(lower_col_list,check_cnt,select_infra, len(upper_col_list))

        # TODO 함수화
        for idx, col in enumerate(col_list) : 
            with col :
                item_name = INFRA_INFO[idx]['ko']
                item_key = INFRA_INFO[idx]['code']
                int_item_key = int(item_key)

                st.header(item_name)
                st.image(f'./image/{item_name}.jpg')
                
                if st.checkbox(f'{item_name}' , key = f'{item_key}'):
                    check_cnt += 1 
                    select_list[int_item_key] = True
                else:
                    select_list[int_item_key] = False
        
        # for idx, col in enumerate(lower_col_list) : 
        #     idx += len(upper_col_list)
        #     with col :
        #         item_name = INFRA_INFO[idx]['ko']
        #         item_key = INFRA_INFO[idx]['code']
        #         st.header(item_name)
        #         st.image(f'./image/{item_name}.jpeg')
                
        #         if st.checkbox(f'{item_name}' , key = f'{item_key}'):
        #             check_cnt += 1 
        #             select_list[idx] = True
        #         else:
        #             select_list[idx] = False

        # col1, col2, col3, col4 = st.columns(4) 
        # col5, col6, col7,col8 = st.columns(4)
        # check_cnt = 0

        # with col1:
        #     st.header("편의점")
        #     st.image("./image/편의점.jpeg")
        #     if st.checkbox("편의점" , key = 1):
        #         con_store = 1
        #         check_cnt += 1
        #         print(check_cnt)
        #     else:
        #         print("편의점")
        #         con_store = 0
                
        # with col2:
        #     st.header("약국")
        #     st.image("./image/약국.jpeg")
        #     if st.checkbox("약국" , key = 2):
        #         phar = 1
        #         check_cnt += 1
        #         print(check_cnt)
        #     else:
        #         phar = 0

        # with col3:
        #     st.header("카페")
        #     st.image("./image/카페.jpeg")
        #     if st.checkbox("카페" , key = 3):
        #         cafe = 1
        #         check_cnt += 1
        #         print(check_cnt)
        #     else:
        #         cafe = 0

        # with col4:
        #     st.header("병원")
        #     st.image("./image/병원.jpeg")
        #     if st.checkbox("병원" , key = 4):
        #         hospital = 1
        #         check_cnt += 1
        #     else:
        #         hospital = 0

        # with col5:
        #     st.header("공원")
        #     st.image("./image/공원.jpeg")
        #     if st.checkbox("공원" , key = 5):
        #         park = 1
        #         check_cnt += 1
        #     else:
        #         park = 0

        # with col6:
        #     st.header("대형마트")
        #     st.image("./image/대형마트.jpeg")
        #     if st.checkbox("대형마트" , key = 6):
        #         mart = 1
        #         check_cnt += 1
        #     else:
        #         mart = 0

        # with col7:
        #     st.header("영화관")
        #     st.image("./image/영화관.jpeg")
        #     if st.checkbox("영화관" , key = 7):
        #         theater = 1
        #         check_cnt += 1
        #     else:
        #         theater = 0

        # with col8:
        #     st.header("지하철")
        #     st.image("./image/지하철.jpeg")
        #     if st.checkbox("지하철" , key = 8):
        #         subway = 1
        #         check_cnt += 1
        #     else:
        #         subway = 0



        submit = st.form_submit_button("제출하기")
        if submit:
            if locate == '원하는 구를 선택하세요.':
                st.error('구를 선택하세요.')
            elif check_cnt >=3:
                # url = ''.join([BACKEND_ADDRESS,DOMAIN_INFO['signup'],DOMAIN_INFO['']])
                #USERS_INFRA -> 어떻게 보낼지 확인하기 
                # USERS_INFRA = {'uesr_id' : ,
                #                'gu' : gu
                #                 'infra_type' : ,
                #                 'infra_yn' : }
                selected_infra_list = []
                #print('select_list : ', select_list)
                for idx, is_select in enumerate(select_list):

                    if ( True == is_select ):
                        value_str = f'0{idx}' if  ( ( idx // 10 ) == 0 ) else f'{idx}'
                        #print('value_str : ',value_str) 
                        selected_infra_list.append(value_str)
                    idx += 1
                    

                    #print('-----------------------')
                # session['ex_user_info'] = session.cur_user_info
                session.cur_user_info['user_gu'] = locate
                session.item_list = []
                infra_user_info = {
                "user_id" :session.cur_user_info['user_id'],
                "user_gu" :session.cur_user_info['user_gu'],
                "infra": selected_infra_list
                }
 
                url = ''.join([BACKEND_ADDRESS, DOMAIN_INFO['users'], DOMAIN_INFO['infra']])
                res = requests.post(url,data=json.dumps(infra_user_info) )

                session.page_counter = 3
                st.experimental_rerun()
            else:
                st.error('희망 인프라를 3개 이상 선택하시오')
        
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