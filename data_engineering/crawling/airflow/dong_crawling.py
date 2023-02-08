import requests
import json
import pandas as pd
import geohash2
import warnings
from config import DONG_INFO, TEST_DONG_INFO
from tqdm import tqdm
from datetime import datetime

warnings.filterwarnings('ignore')

# 직방에서 서울시의 원룸/오피스텔 정보를 크롤링한다.

def get_item_id_by_roomtype(addr,roomtype): # 동이름 넣으면 정보 반환하도록

    url = f"https://apis.zigbang.com/v2/search?leaseYn=N&q=서울시 {addr}&serviceType={roomtype}"
    response = requests.get(url)
    data = response.json()["items"][0]
    lat, lng = data["lat"], data["lng"]
    geohash = geohash2.encode(lat, lng, precision=5)

    url = f"https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang\
&geohash={geohash}&needHasNoFiltered=true&rent_gteq=0&sales_type_in=전세|월세&service_type_eq={roomtype}"
    response = requests.get(url)
    items = response.json()["items"]
    ids = [item["item_id"] for item in items]

    return ids

def get_simple_item_info(ids:list,dong:str):

    num_of_ids = len(ids)
    mock = num_of_ids // 500
    divided = num_of_ids % 500

    url = "https://apis.zigbang.com/v2/items/list"

    collect_df = pd.DataFrame()

    for idx in range (mock + 1 ):
        start_idx = idx * 500
        end_idx = ( idx + 1 ) * 500
 
        end_idx = num_of_ids - 1 if( end_idx >= num_of_ids ) else end_idx

        check_ids = ids[start_idx : end_idx]


        params = {
            "domain": "zigbang",
            "withCoalition": "true",
            "item_ids": check_ids
        }

        response = requests.post(url, params)
        items = response.json()["items"]
        # columns = ["item_id", "sales_type", "deposit", "rent", "address1", "manage_cost"]
        temp_df = pd.DataFrame(items)
        temp_df = temp_df[temp_df["address1"].str.contains(dong)].reset_index(drop = True)
        collect_df = pd.concat([temp_df,collect_df])
        # df = df.rename(columns = {"address1": "주소", "sales_type": "유형","deposit": "보증금", "rent": "월세", "manage_cost": "관리비"})
    return collect_df

def get_detail_item_info(target_list:list):

    df = pd.DataFrame()

    for item_id in tqdm(target_list):
        url = f'https://apis.zigbang.com/v2/items/{item_id}'

        req = requests.get(url)
        data= json.loads(req.text)
        item= data['item']

        single_data = pd.Series(item.values())
        df = df.append(single_data, ignore_index=True)

    return df

# 현재 서울시 한정, '서울시' 가 하드코딩 되어 있다. 
def get_whole_house_info_from_zigbang():

    total_key_list = []

    for cur_dong in TEST_DONG_INFO.keys():

        room_item_ids = get_item_id_by_roomtype( cur_dong,roomtype ="원룸")
        room_item_ids.append(get_item_id_by_roomtype(cur_dong,roomtype ="오피스텔"))
        total_key_list = total_key_list + list(get_simple_item_info(room_item_ids,cur_dong).item_id)

    res = get_detail_item_info(total_key_list)
    res.to_csv(f'house_info_{datetime.now().date()}.csv')