import { useCallback, useEffect, useRef, useState } from "react";
import type { FC } from "react";
import Map from "../Map/Map";
import Recommend from "../Recommend";
import { fetchHouseByCoord } from "../../data/fetchByUser";
import { useSelector, useDispatch } from "react-redux";
import * as H from "../../store/house";
import * as D from "../../data";
import { AppState } from "../../store";

type userInfo = {
  gu: string;
};

const Main: FC<userInfo> = ({ gu }) => {
  const houseInfoManage = useSelector<AppState, H.State>(
    (state) => state.house
  );
  const dispatch = useDispatch();

  const getCurrentHouseInfo = useCallback(() => {
    D.fetchHouseByGu({ userId: 1, userGu: gu })
      .then((houses) => dispatch(H.changeCurHouseList(Object.values(houses))))
      .catch()
      .finally();
  }, [dispatch]);

  const mapElement = useRef(null);

  useEffect(() => {
    getCurrentHouseInfo();
  }, [gu]);

  return (
    <>
      {/* <button
        style={{
          top: "20.2vw",
          left: "75.2vw",
          zIndex: "2",
          position: "absolute",
        }}
        type="button"
        className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2.5 text-center inline-flex items-center mr-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        필터
      </button>

      <div
        style={{
          top: "15.2vw",
          left: "63.2vw",
          zIndex: "2",
          height: "10vw",
          width: "10vw",
          position: "absolute",
        }}
        className="bg-white rounded-lg white-space: nowrap"
      >
        가격 필터 자리
      </div> */}
      <button
        style={{
          top: "2vh",
          left: "35.2vw",
          width: "20vw",
          zIndex: "2",
          position: "absolute",
        }}
        type="button"
        className="text-gray-900 bg-gradient-to-r from-red-200 via-red-300 to-yellow-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-red-100 dark:focus:ring-red-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
      >
        구 선택 창으로 사용
      </button>
      <button
        style={{
          top: "2vh",
          left: "70vw",
          zIndex: "2",
          position: "absolute",
        }}
        type="button"
        className="text-gray-900 bg-gradient-to-r from-red-200 via-red-300 to-yellow-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-red-100 dark:focus:ring-red-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
      >
        관심목록
      </button>

      <Map houses={houseInfoManage["curHouseList"]} />
    </>
  );
};

export default Main;
