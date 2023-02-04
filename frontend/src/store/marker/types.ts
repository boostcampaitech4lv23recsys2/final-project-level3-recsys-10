import type { Action } from "redux";

export type State = {
  curMarker: unknown;
  markerList: unknown[];
};
export type SetMarkerInfoAction = Action<"@marker/setMarkerInfo"> & {
  payload: State;
};

export type ChangeCurMarkerAction = Action<"@marker/changeCurMarker"> & {
  payload: unknown;
};

export type ClearCurMarkerAction = Action<"@marker/clearCurMarker"> & {};

export type ChangeMarkerList = Action<"@marker/changeMarkerList"> & {
  payload: unknown[];
};

export type Actions =
  | SetMarkerInfoAction
  | ChangeCurMarkerAction
  | ClearCurMarkerAction
  | ChangeMarkerList;
