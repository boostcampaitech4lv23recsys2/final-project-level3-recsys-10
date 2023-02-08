# :house: 인프라 기반 부동산 매물 추천

![윤곽선2](https://user-images.githubusercontent.com/79534756/217191115-e98677e5-bf84-4262-9564-924a3d2de764.png)



## 1. 프로젝트 소개

- 개요
    
     → 주변 시설 7가지에 대한 선호도를 바탕으로 한 원룸/오피스텔 매물 추천
    
    - 주변 시설 7가지 : 지하철, 편의점, 대형마트, 카페, 약국, 영화관, 헬스장
- 기존 서비스와 비교
    - 차별점 : 가격과 인프라 정보를 반영하여 원룸과 오피스텔 중심으로 매물 추천


<img width="673" alt="스크린샷 2023-02-07 오후 4 25 58" src="https://user-images.githubusercontent.com/65005242/217582223-9529677b-d445-44e6-945a-c4bc074a77a9.png">


- 사이트맵

   ![스크린샷 2023-02-09 오전 1 39 02](https://user-images.githubusercontent.com/65005242/217593947-217fd10a-f71e-47f3-a73c-19b4207f6181.png)




## 2. 프로젝트 구조

- Architecture Diagram
    
![recsys10-architecture2](https://user-images.githubusercontent.com/65005242/217582562-f83a067d-bdc1-43e9-b607-9040f3488f4e.png)

    
- Activity Diagram
    
![recsys10-UML_2](https://user-images.githubusercontent.com/65005242/217582603-1b1af485-301b-45d0-8bef-5a015b089ca5.png)

    
    - 신규 회원이나 ‘좋아요’ 한 매물이 하나도 없는 사용자
        - 인프라 점수가 높은 순으로 순위를 매겨 추천
    - ‘좋아요’ 한 매물이 다섯 개 미만 사용자
        - Content-based filtering 으로 ‘좋아요’한 매물과 유사한 매물을 함께 추천
    - ‘좋아요’ 한 매물이 다섯 개 이상인 사용자
        - `AI 추천 받기` 버튼을 눌렸을 때 LightGCN 모델을 활용하여 매물 추천
        
- 프로젝트 구조





## 3. 프로젝트 진행 방법

- 프로젝트 일정
    
![스크린샷 2023-02-08 오후 3 16 15](https://user-images.githubusercontent.com/65005242/217583065-4a192e98-7faa-4111-818f-ea77bd526126.png)

    
- 협업 방법
    - GitFlow
    
       ![recsys10-gitflow](https://user-images.githubusercontent.com/65005242/217583246-08a97b9a-7a73-4677-b02c-59eee1efb284.png)


        
        - main, feature, dev, release 4종류 branch 사용
        - branch를 Task별로 세분화하여 코드 이슈 및 conflict에 유연한 대처
    - Notion
        - 프로젝트 업무현황
            - TODO, In Progress, Paused/Blocked, Done 4가지로 분류하여 개인 업무 공유 및 관리
        - 프로젝트 타임라인
            - 프로젝트 일정을 타임라인으로 가시화
            - 일자 별 진행 현황 파악 용이
    - GIt Issue
        - Issue별 Commit관리
        - 작업 내용 파악 용이
    - 개발 Tool

      <img width="583" alt="스크린샷 2023-02-07 오후 4 28 54" src="https://user-images.githubusercontent.com/65005242/217583304-2e463931-75cf-452e-9e7f-b19f058a866f.png">


## 4. 모델

### User Scenario

1. Cold Start 문제를 해결하기 위해 Rule-based 와 Content-based 를 함께 사용
2. 유저가 선호하는 매물이 특정 지역(구)에서 일정 개수 이상이 되었을 때 LightGCN 모델 활용

### Rule-based Model

- 적정 거리 내 인프라 별 최단 거리 및 개수를 정규화
- 사용자가 선택한 인프라를 기반으로 스코어링하여 랭킹

### Content-based Filtering

- 유저가 선호 매물로 선택한 아이템을 기반으로 벡터화 → 유사도 높은 매물을 추천

### ML Model : LightGCN

- Interaction 데이터를 기반으로 그래프를 연결하여 관계성을 표시
- 직접적으로 연결된 아이템이 아니더라도 노드를 통해 접근 가능하기 때문에 직접적인 Interaction이 불필요함

→ 유저의 찜 목록을 매물과의 Interaction으로 사용

→ 해당 유저가 선택한 인프라에 대한 거리 점수를 아이템 행렬의 추가 정보로 사용


## 7. 팀 소개

- 팀 이름: 추천해조(Recommend-Seaweed)
- 팀 구성 및 역할


|![아이스크림호방](https://user-images.githubusercontent.com/65005242/217590558-6a123c71-4777-423b-a0f6-d5f39e79ff19.PNG)|![초콜릿 호빵](https://user-images.githubusercontent.com/65005242/217589793-6fe272ed-9ff4-418c-a419-3f745488b0dc.PNG)|![image (5)](https://user-images.githubusercontent.com/65005242/217591028-03132bea-43c8-4fd1-8b65-4ea761831e09.png)|![image (4)](https://user-images.githubusercontent.com/65005242/217590196-fdaf23a2-8bd5-4396-9eba-32e6800f29cc.png)|![image (3)](https://user-images.githubusercontent.com/65005242/217590580-98d6e948-2cd9-4fa0-b4fa-9de85e39a520.png)|![커피호빵](https://user-images.githubusercontent.com/65005242/217590135-2743d6fa-f103-43d4-baee-ed636d2a2ad3.PNG)|
|----|----|----|----|----|----|
|[구혜인](https://github.com/hyein99?tab=repositories)|[권은채](https://github.com/dmscornjs)|[박건영](https://github.com/kuuneeee)|[장현우](https://github.com/jhu8802)|[정현호](https://github.com/Heiness)|[허유진](https://github.com/hobbang2)|
|* Backend 총괄 <br> * Backend API 설계 및 map API 구현 <br> * Inference API 구현 <br> * DataBase 설계|* 로그인/회원가입 API 구현 <br> * 데이터 크롤링 및 EDA <br> * 데이터 검증|* 모델 비교분석 및 모델링 <br> * Inference 코드 구현 <br> * 찜목록 API 구현 <br> * ML 모델 API 구현 <br> * 캐릭터 아이콘 디자인 |* Stremalit 구현 <br> * 사용자 Session 유지 처리 구현 <br> * 데이터 검증|* 프로젝트 기획 <br> * 데이터 정제 및 EDA <br> * 스코어링 알고리즘 <br> * Content-based Filtering 적용 |* Streamlit 구현 <br> * React 구현 <br> * Airflow 적용 <br> * Docekr적용 <br> * FastAPI ORM 구현|


