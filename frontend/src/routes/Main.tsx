import { useCallback, useEffect, useRef, useState } from "react";
import type { FC } from "react";
import Map from "./Map/Map";
import Recommend from "./Loading";
import { useSelector, useDispatch } from "react-redux";
import * as H from "../store/house";
import * as U from "../store/user";
import * as L from "../store/loading";
import * as D from "../data";
import { AppState } from "../store";

import { Gu } from "../routes/Initial/Gu";
import { ReactComponent as Heart } from "../heart.svg";
import Dropdown from "../Components/Dropdown";

type userInfo = {
  gu: string;
};

const Main: FC<userInfo> = ({ gu }) => {
  const dispatch = useDispatch();

  const [curUserGu, setCurUserGu] = useState<string>("");
  const houseInfoManage = useSelector<AppState, H.State>(
    (state) => state.house
  );

  const { userId, userGu } = useSelector<AppState, U.State>(
    (state) => state.user
  );

  const isLoading = useSelector<AppState, L.State>((state) => state.loading);

  const getCurrentHouseInfo = useCallback(() => {
    dispatch(L.setLoading(true));
    D.fetchHouseByGu({ userId: userId, userGu: userGu })
      .then((houses) => {
        const itemList = Object.values(houses).filter((item: any) =>
          Object.keys(item).includes("house_id")
        );
        dispatch(H.changeCurHouseList(itemList));
        dispatch(H.changeShowHouseList(itemList));
        dispatch(L.setLoading(false));
      })
      .catch()
      .finally();
  }, [userGu]);

  const mapElement = useRef(null);

  useEffect(() => {
    dispatch(U.setChangeGu(curUserGu));
  }, [curUserGu]);

  useEffect(() => {
    getCurrentHouseInfo();
  }, [userGu]);

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
      {/* <button
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
      </button> */}
      <div className="absolute z-10 justify-center flex-1 max-w-sm px-2 mx-auto">
        <div className="flex items-center justify-between">
          <div
            className="max-w-md"
            style={{
              top: "2vh",
              left: "43.2vw",
              position: "fixed",
            }}
          >
            {" "}
            {!isLoading && <Gu setGu={setCurUserGu} className="z-10 mr-2"></Gu>}
          </div>
          {!isLoading && <Dropdown></Dropdown>}
          {/* <button className="text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50 mr-2 mb-2">
            AI추천
          </button> */}

          {/* <button
            style={{
              top: "2vh",
              position: "fixed",
            }}
            type="button"
            className="text-gray-900 bg-gradient-to-r from-red-200 via-red-300 to-yellow-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-red-100 dark:focus:ring-red-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
          >
            <Heart />
          </button> */}
        </div>
      </div>
      {!isLoading && <Map houses={houseInfoManage["curHouseList"]} />}
      {isLoading && <Recommend />}
    </>
  );
};

export default Main;
