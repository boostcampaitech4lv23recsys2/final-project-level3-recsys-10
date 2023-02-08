import type { FC, PropsWithChildren } from "react";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import * as U from "../store/user";
import * as D from "../data";
import { AppState } from "../store";

type RequireAuthProps = {};

const RequireAuth: FC<PropsWithChildren<RequireAuthProps>> = ({ children }) => {
  const { userId } = useSelector<AppState, U.State>((state) => state.user);
  const navigate = useNavigate();

  useEffect(() => {
    if (userId === 0) navigate("/login");
  }, [userId, navigate]);

  return <>{children}</>;
};

export default RequireAuth;
