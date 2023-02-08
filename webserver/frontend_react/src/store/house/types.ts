import type { Action } from "redux";

export type State = {
  curHouseList: any[];
  exHouseList: any[];
  showHouseList: any[];
};

export type SetHouseAction = Action<"@house/setHouse"> & {
  payload: State;
};

export type ChangeCurHouseAction = Action<"@house/changeCurHouseList"> & {
  payload: any[];
};

export type ChangeExHouseAction = Action<"@house/changeExHouseList"> & {
  payload: any[];
};

export type ChangeShowHouseAction = Action<"@house/changeShowHouseList"> & {
  payload: any[];
};

export type UpdateHouseZzimAction = Action<"@house/updateHouseZzim"> & {
  payload: {
    houseId: number;
    zzim: string;
  };
};

export type Actions =
  | SetHouseAction
  | ChangeCurHouseAction
  | ChangeExHouseAction
  | ChangeShowHouseAction
  | UpdateHouseZzimAction;
