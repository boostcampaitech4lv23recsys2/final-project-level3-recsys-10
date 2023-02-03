import { Routes, Route } from "react-router-dom";
import NoMatch from "./NoMatch";
import Main from "./Main";
import Login from "./Initial/Login";
import InfoSetting from "./Initial/InfoSetting";

export default function RoutesSetup() {
  return (
    <Routes>
      <Route path="/" element={<Main gu="강남구" />}></Route>
      <Route path="/login" element={<Login />}></Route>
      <Route path="/infra" element={<InfoSetting />}></Route>
      <Route path="*" element={<NoMatch />}>
        {" "}
      </Route>
    </Routes>
  );
}
