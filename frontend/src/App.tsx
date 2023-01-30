import React from "react";
import logo from "./logo.svg";
import "./App.css";
import Map from "./Pages/Map/Map";
import Login from "./Pages/Login";
import Main from "./Pages/Main/Main";
import InputBox from "./Components/InputBox";
import Card from "./Components/Card";

function App() {
  return (
    <div>
      <Main gu={"용산구"} />
    </div>
  );
}

export default App;
