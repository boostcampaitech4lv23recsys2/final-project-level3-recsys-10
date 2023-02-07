import React from "react";
import { ReactComponent as Back } from "../back.svg";
import SimpleListCard from "./SimpleListCard";
import Card from "./Card";
import type { FC } from "react";

import { useSelector, useDispatch } from "react-redux";
import * as H from "../store/house";
import * as U from "../store/user";
import { AppState } from "../store";
import { INFRA_INFO_DICT } from "../data/config/infraConfig";
import { IInfraInfo } from "../utils/utils";

type myType = {
  setIsSidebarOpen: (val: boolean) => void;
  itemList: any;
  markerList: any;
};

const Sidebar: FC<myType> = ({ setIsSidebarOpen, itemList, markerList }) => {
  const itemCnt = itemList.length;
  const isShowDetail = 1 === itemCnt;

  const dispatch = useDispatch();
  const houseInfoManage = useSelector<AppState, H.State>(
    (state) => state.house
  );

  const { infraList } = useSelector<AppState, U.State>((state) => state.user);

  const infraStr = infraList
    .map((item: string) => INFRA_INFO_DICT[item as keyof IInfraInfo]["ko"])
    .join(", ");

  return (
    <aside className="fixed top-0 right-0 z-40 h-screen min-h-screen duration-300 ease-in-out transition-transform-translate-x-full sm:translate-x-5 md:flex">
      <div className="h-full px-3 py-4 overflow-y-auto bg-white dark:bg-gray-800">
        <ul className="space-y-2">
          <li key="detail-btn">
            <button
              onClick={
                isShowDetail
                  ? () =>
                      dispatch(
                        H.changeShowHouseList(houseInfoManage.curHouseList)
                      )
                  : () => setIsSidebarOpen(false)
              }
              className="items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <Back></Back>
            </button>
            <span className="w-20 bg-pink-100 text-pink-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-pink-900 dark:text-pink-300">
              선택한 인프라 : {infraStr}
            </span>
          </li>
          {itemList?.map((item: any, idx: number) => {
            return (
              <li
                key={item["house_id"]}
                onClick={
                  !isShowDetail
                    ? () => {
                        dispatch(H.changeShowHouseList([item]));
                        markerList[idx].trigger("click");
                      }
                    : undefined
                }
              >
                {!isShowDetail && <SimpleListCard item={item}></SimpleListCard>}
                {isShowDetail && <Card item={item}></Card>}
                <hr className="h-px my-8 bg-gray-200 border-0 dark:bg-gray-700"></hr>
              </li>
            );
          })}
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar;
