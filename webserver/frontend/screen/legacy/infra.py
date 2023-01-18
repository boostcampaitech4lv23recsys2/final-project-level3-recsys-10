import streamlit as st

#count = 0 => 로그인
#      = 1 => 회원가입
#      = 2 => 둘러보기(인프라 선택)
#      = 3 => 지도

def show_infra(session:dict):

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
        session['page_counter'] = 3
        st.experimental_rerun()

