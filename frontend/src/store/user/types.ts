import type { Action } from "redux";

export type State = {
  userId: number;
  userGu: string;
  infraList: string[];
};

export type SetUserInfoAction = Action<"@user/setUserInfo"> & {
  payload: State;
};

export type ChangeIdAction = Action<"@user/changeId"> & {
  payload: number;
};

export type ChangeGuAction = Action<"@user/changeGu"> & {
  payload: string;
};

export type ChangeInfraAction = Action<"@user/changeInfra"> & {
  payload: string[];
};

export type Actions =
  | SetUserInfoAction
  | ChangeIdAction
  | ChangeGuAction
  | ChangeInfraAction;
