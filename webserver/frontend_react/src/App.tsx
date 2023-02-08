import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Map from "./routes/Map/Map";
import Login from "./Pages/Initial/Login";
import InputBox from "./Components/InputBox";
import Card from "./Components/Card";
import SimpleListCard from "./Components/SimpleListCard";
import DetailListCard from "./Components/DetailListCard";
import Sidebar from "./Components/Sidebar";
import Navbar from "./Components/Navbar";
import Recommend from "./routes/Loading";
import RoutesSetup from "./routes/RoutesSetup";
// import { UserInfoProvider } from "./Contexts/UserInfoContext";

import type { Action } from "redux";
import { Provider as ReduxProvider } from "react-redux";
import { configureStore } from "@reduxjs/toolkit";
import { useStore } from "./store";

import { BrowserRouter } from "react-router-dom";

function App() {
  const store = useStore();
  return (
    <ReduxProvider store={store}>
      <BrowserRouter>
        <RoutesSetup></RoutesSetup>
        <div style={{ position: "relative" }}>
          {/* <Recommend></Recommend> */}
        </div>
      </BrowserRouter>
    </ReduxProvider>
  );
}

export default App;
