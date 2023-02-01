import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Map from "./Pages/Map/Map";
import Login from "./Pages/Login";
import Main from "./Pages/Main/Main";
import InputBox from "./Components/InputBox";
import Card from "./Components/Card";
import SimpleListCard from "./Components/SimpleListCard";
import DetailListCard from "./Components/DetailListCard";
import Sidebar from "./Components/Sidebar";
import Navbar from "./Components/Navbar";
import { UserInfoProvider } from "./Contexts/UserInfoContext";
import Recommend from "./Pages/Recommend";

import type { Action } from "redux";
import { Provider as ReduxProvider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";

type IUserInfo = {
  user_id: number;
  user_gu: string;
  infra_list: string[];
};

type AppState = {
  user_info: IUserInfo;
  houses_info: any[];
  ex_houses_info: any[];
  cur_marker_list: any[];
};

const initialAppState = {
  user_info: {
    user_id: 0,
    user_gu: "string",
    infra_list: [],
  },
  houses_info: [],
  ex_houses_info: [],
  cur_marker_list: [],
};

const rootReducer = (state: AppState = initialAppState, action: Action) =>
  state;
const store = configureStore({ reducer: rootReducer, middleware: [] });

function App() {
  return (
    <ReduxProvider store={store}>
      <UserInfoProvider>
        <div style={{ position: "relative" }}>
          {/* <Recommend></Recommend> */}
          <Main gu={"용산구"} />
        </div>
      </UserInfoProvider>
    </ReduxProvider>
  );
}

export default App;
