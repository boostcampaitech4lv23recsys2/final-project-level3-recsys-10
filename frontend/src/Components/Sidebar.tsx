import React from "react";
import { ReactComponent as Back } from "../back.svg";
import SimpleListCard from "./SimpleListCard";
import type { FC } from "react";

type myType = {
  setIsSidebarOpen: (val: boolean) => void;
};

const Sidebar: FC<myType> = ({ setIsSidebarOpen }) => {
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
          <li>
            <a
              href="#"
              className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <SimpleListCard></SimpleListCard>
            </a>
          </li>
          <hr className="h-px my-8 bg-gray-200 border-0 dark:bg-gray-700"></hr>
          <li>
            <a
              href="#"
              className="flex items-center p-2 text-base font-normal text-gray-900 rounded-lg dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <SimpleListCard></SimpleListCard>
            </a>
          </li>
          <hr className="h-px my-8 bg-gray-200 border-0 dark:bg-gray-700"></hr>
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar;
