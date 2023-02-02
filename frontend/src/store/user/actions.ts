import type * as T from "./types";

export const setUserInfo = (payload: T.State): T.SetUserInfoAction => ({
  type: "@user/setUserInfo",
  payload,
});

export const setChangeGu = (payload: string): T.ChangeGuAction => ({
  type: "@user/changeGu",
  payload,
});

export const setChangeInfra = (payload: string[]): T.ChangeInfraAction => ({
  type: "@user/changeInfra",
  payload,
});
