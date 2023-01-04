import pyproj
import folium
import pandas as pd
import numpy as np

def project_array(coord, p1_type:str="epsg:5174",  p2_type:str="epsg:4326"):
    """
    좌표계 변환 함수
    - coord: x, y 좌표 정보가 담긴 NumPy Array
    - p1_type: 입력 좌표계 정보 ex) epsg:5179
    - p2_type: 출력 좌표계 정보 ex) epsg:4326
    """
    p1 = pyproj.Proj(init=p1_type)
    p2 = pyproj.Proj(init=p2_type)
    fx, fy = pyproj.transform(p1, p2, coord[:, 0], coord[:, 1])
    return np.dstack([fy,fx])[0]

"""example 
# 경도, 위도 ( x,y )
coord = np.array([[187670.416423662,447030.560396528],[203799.86528368,462533.430210964],[203799.86528368,462533.430210964],[187670.416423662,447030.560396528]])

# 좌표계 정보 설정
p1_type = "epsg:5174"
p2_type = "epsg:4326" # wgs84 

# project_array() 함수 실행
result = project_array(coord[:5], p1_type, p2_type)

print(result)
"""


def get_example_data(data_path:str="/opt/ml/3rdproject/final_team_repo/webserver/frontend/example_data/jigbang_crawl_72.csv",
                     usecols:list=["item_id","jibunAddress","image_thumbnail","매매금액","보증금액","월세금액","title","description","random_location"],
                     rename_cols:list=["id","img","매매금액","보증금액","월세금액","title","summary","description","location"]):
    
    example_data = pd.read_csv(data_path,usecols=usecols) # ,usecols=["좌표정보(X)","좌표정보(Y)"]
    example_data.columns = rename_cols
    example_data.insert(0, 'rank', range(1, 1 + len(example_data)))
    example_data["img"].fillna("",inplace=True)
    example_data["img_size"] = "?w=400&amp;h=300&amp;q=70&amp;a=1"
    example_data["img"] = example_data["img"].str.cat(example_data["img_size"])
    example_data["grid_id"] = 1
    item_list = example_data.to_dict('records')

    return item_list.copy()