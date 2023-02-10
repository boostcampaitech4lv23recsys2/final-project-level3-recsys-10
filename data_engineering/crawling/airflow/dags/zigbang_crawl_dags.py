from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from dong_crawling import get_whole_house_info_from_zigbang
from classify_house_by_grid import match_grid_id
from airflow.providers.mysql.operators.mysql import MySqlOperator

# Database HOUSE_INFO2 의 스키마와 맞추어줘야 하는 문제 
# 스키마를 엑셀이나 csv 또는 sqlite 같은 문서로 관리하여 자동화하는 방법이 있음 

default_args = {
    'owner': 'hobbang',
    'depends_on_past': False,  # 이전 DAG의 Task가 성공, 실패 여부에 따라 현재 DAG 실행 여부가 결정. False는 과거의 실행 결
과 상관없이 매일 실행한다
    'start_date': datetime(2022, 4, 25),
    'retires': 1,  # 실패시 재시도 횟수
    'retry_delay': timedelta(minutes=5)  # 만약 실패하면 5분 뒤 재실행
}

# 크롤링한 매물 데이터에 없는 직방 매물은 팔린 것으로 간주한다. 
# popular 추가
create_str = f'''
CREATE  TABLE   IF  NOT EXISTS
`HOUSE_INFO2` (
  `house_id` int NOT NULL AUTO_INCREMENT,
  `zigbang_id` int NOT NULL,
  `latlng` point DEFAULT NULL,
  `grid_id` int DEFAULT NULL,
  `sales_type` varchar(255) DEFAULT NULL,
  `service_type` varchar(255) DEFAULT NULL,
  `house_area` float DEFAULT NULL,
  `price_sales` int DEFAULT 0,
  `price_deposit` int DEFAULT 0,
  `price_monthly_rent` int DEFAULT 0,
  `manage_cost` int DEFAULT 0,
  `address` varchar(255) DEFAULT NULL,
  `local1` varchar(20) DEFAULT NULL,
  `local2` varchar(20) DEFAULT NULL,
  `title` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `image_thumbnail` varchar(255) DEFAULT NULL,
  `images` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `images_cnt` int DEFAULT NULL,
  `floor` varchar(10) DEFAULT NULL,
  `floor_total` varchar(10) DEFAULT NULL,
  `bathroom_cnt` int DEFAULT NULL,
  `register_date` datetime NOT NULL,
  `update_date` datetime NOT NULL,
  `sold_yn` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'N',
   PRIMARY KEY (`house_id`) USING BTREE,
   UNIQUE INDEX `zigbang_id` (`zigbang_id`) USING BTREE,
   INDEX `grid_id` (`grid_id`) USING BTREE,
   CONSTRAINT `HOUSE_INFO2_ibfk_1` FOREIGN KEY (`grid_id`) REFERENCES `GRID` (`grid_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=475148 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
'''

update_str = f'''
BEGIN
UPDATE  HOUSE_INFO2
SET     sold_yn = 'Y'
WHERE   zigbang_id  NOT IN (SELECT item_id FROM ORG_ZIGBANG_HOUSE)
END
'''

select_str = f'''
SELECT  grid_id
FROM    house_info_with_grid
'''

# 이전 매물 데이터에 없는 매물은 새로 생긴 것으로 간주한다. 
insert_str =  f'''
INSERT  INTO HOUSE_INFO2(zigbang_id,
latlng,
grid_id,
sales_type,
service_type,
house_area,
price_sales,
price_deposit,
price_monthly_rent,
manage_cost,
address,
local1,
local2,
title,
description,
image_thumbnail,
images,
images_cnt,
floor,
floor_total,
bathroom_cnt,
register_date,
update_date,
sold_yn)  
SELECT  item_id, POINT(lng,lat), grid_id, sales_type, service_type,
        전용면적_m2, 매매금액, 보증금액, 월세금액, manage_cost,
        address, local1,local2, title, description, image_thumbnail,
        images, images_cnt, floor, floor_all, bathroom_count,
        register_date,update_date,sold_yn
  FROM  ORG_ZIGBANG_HOUSE
 WHERE  item_id not in (select zigbang_id from HOUSE_INFO2)
'''

# with 구문으로 DAG 정의
with DAG(
        dag_id='zigbang_whole_test',
        default_args=default_args,
        schedule_interval='@once', # 하루마다 
        tags=['my_dags']
) as dag:

    python_crawling_zigbang= PythonOperator(
        task_id='zigbang_crawl',
        python_callable=get_whole_house_info_from_zigbang
    )

    python_match_grid_info = PythonOperator(
        task_id='zigbang_match_grid',
        python_callable=match_grid_id
    )

    # HOUSE_INFO2 table 없으면 생성하기 
    mysql_create_house = MySqlOperator(
        task_id="create_house_info2",
        mysql_conn_id="hobbang-mysql",
        sql=create_str
    )

    # id 비교해서 새 item 넣어주기
    mysql_select_house = MySqlOperator(
        task_id="create_insert_info2",
        mysql_conn_id="hobbang-mysql",
        sql=insert_str
    )

    # mysql_update_house 제외 : 모델 고도화를 위해 업데이트 중지
    python_crawling_zigbang >> python_match_grid_info >> mysql_create_house >> mysql_select_house
