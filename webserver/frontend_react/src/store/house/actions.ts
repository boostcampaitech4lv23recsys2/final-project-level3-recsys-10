import type * as T from "./types";

export const setHouse = (payload: T.State): T.SetHouseAction => ({
  type: "@house/setHouse",
  payload,
});

export const changeCurHouseList = (payload: any[]): T.ChangeCurHouseAction => ({
  type: "@house/changeCurHouseList",
  payload,
});

export const changeExHouseList = (payload: any[]): T.ChangeExHouseAction => ({
  type: "@house/changeExHouseList",
  payload,
});

export const changeShowHouseList = (
  payload: any[]
): T.ChangeShowHouseAction => ({
  type: "@house/changeShowHouseList",
  payload,
});

export const updateHouseZzim = (payload: {
  houseId: number;
  zzim: string;
}): T.UpdateHouseZzimAction => ({
  type: "@house/updateHouseZzim",
  payload,
});
