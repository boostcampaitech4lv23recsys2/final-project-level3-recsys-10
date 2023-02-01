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
import Recommend from "./Pages/Recommend";
import { UserInfoProvider } from "./Contexts/UserInfoContext";

import type { Action } from "redux";
import { Provider as ReduxProvider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { useStore } from "./store";

function App() {
  const store = useStore();
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
