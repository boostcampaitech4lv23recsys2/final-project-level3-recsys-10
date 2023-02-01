import { IUserInfo } from "./AppState";
import type { Action } from "redux";

export type SetUserInfoAction = Action<"setUserInfo"> & {
  userInfo: IUserInfo;
};

export type Actions = SetUserInfoAction;
