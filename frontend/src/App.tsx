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
import { UserInfoProvider } from "./Contexts/UserInfoContext";
import Recommend from "./Pages/Recommend";

function App() {
  return (
    <UserInfoProvider>
      <div style={{ position: "relative" }}>
        {/* <Recommend></Recommend> */}
        <Main gu={"용산구"} />
      </div>
    </UserInfoProvider>
  );
}

export default App;
