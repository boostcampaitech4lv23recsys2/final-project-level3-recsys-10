import type { Action } from "redux";

export type State = {
  curMarker: any;
  markerList: any[];
};
export type SetMarkerInfoAction = Action<"@marker/setMarkerInfo"> & {
  payload: State;
};

export type ChangeCurMarkerAction = Action<"@marker/changeCurMarker"> & {
  payload: any;
};

export type ClearCurMarkerAction = Action<"@marker/clearCurMarker"> & {};

export type ChangeMarkerList = Action<"@marker/changeMarkerList"> & {
  payload: any[];
};

export type Actions =
  | SetMarkerInfoAction
  | ChangeCurMarkerAction
  | ClearCurMarkerAction
  | ChangeMarkerList;
