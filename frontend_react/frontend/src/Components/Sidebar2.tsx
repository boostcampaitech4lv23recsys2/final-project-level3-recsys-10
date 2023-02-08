import React from "react";
import { ReactComponent as Back } from "../back.svg";
import SimpleListCard from "./SimpleListCard";
import type { FC } from "react";

type myType = {
  setIsSidebarOpen: (val: boolean) => void;
};

const Sidebar2 = () => {
  return (
    <aside
      style={{ width: "50rem", marginRight: "1vw" }}
      className="fixed top-0 right-0 z-40 h-screen transition-transform-translate-x-full sm:translate-x-5"
    >
      <div className="h-full px-3 py-4 overflow-y-auto dark:bg-gray-800">
        <ul className="space-y-2">
          <li>
            <svg
              className="w-6 h-6"
              aria-hidden="true"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                clip-rule="evenodd"
                fill-rule="evenodd"
                d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
              ></path>
            </svg>
          </li>
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar2;
