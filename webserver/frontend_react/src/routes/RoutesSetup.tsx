import { Routes, Route } from "react-router-dom";
import RequiredAuth from "./RequiredAuth";
import RequiredGu from "./RequiredGu";
import NoMatch from "./NoMatch";
import Main from "./Main";
import SignUp from "./Initial/SignUp";
import Login from "./Initial/Login";
import Login2 from "./Initial/Login2";
import InfoSetting from "./Initial/InfoSetting";

export default function RoutesSetup() {
  return (
    <Routes>
      <Route
        path="/"
        element={
          <RequiredGu>
            {" "}
            <Main gu="강남구" />{" "}
          </RequiredGu>
        }
      ></Route>
      <Route path="/login" element={<Login2 />}></Route>
      <Route path="/signup" element={<SignUp />}></Route>
      <Route
        path="/infra"
        element={
          <RequiredAuth>
            {" "}
            <InfoSetting />{" "}
          </RequiredAuth>
        }
      ></Route>
      <Route path="*" element={<NoMatch />}>
        {" "}
      </Route>
    </Routes>
  );
}
