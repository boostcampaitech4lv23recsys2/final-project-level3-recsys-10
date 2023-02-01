import React from "react";
import { ReactComponent as Back } from "../back.svg";
import SimpleListCard from "./SimpleListCard";
import Card from "./Card";
import type { FC } from "react";

type myType = {
  setIsSidebarOpen: (val: boolean) => void;
  itemList: any;
};

const Sidebar: FC<myType> = ({ setIsSidebarOpen, itemList }) => {
  const itemCnt = itemList.length;
  const isShowDetail = 1 === itemCnt;

  return (
    <aside
      style={{ width: "26rem", marginRight: "1vw" }}
      className="fixed top-0 right-0 z-40 h-screen transition-transform-translate-x-full sm:translate-x-5"
    >
      <div className="h-full px-3 py-4 overflow-y-auto bg-white dark:bg-gray-800">
        <ul className="space-y-2">
          <li>
            <button
              onClick={() => setIsSidebarOpen(false)}
              className="items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <Back></Back>
            </button>
          </li>
          {itemList?.map((item: any) => {
            return (
              <li>
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
