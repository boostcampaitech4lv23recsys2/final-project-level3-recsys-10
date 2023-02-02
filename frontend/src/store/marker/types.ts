import type { Action } from "redux";

export type State = {
  curMarkerList: unknown[];
  exMarkerList: unknown[];
};

export type SetMarkerAction = Action<"@marker/setMarker"> & {
  payload: State;
};

export type ChangeCurMarkerAction = Action<"@marker/changeCurMarkerList"> & {
  payload: unknown[];
};

export type ChangeExMarkerAction = Action<"@marker/changeExMarkerList"> & {
  payload: unknown[];
};

export type Actions =
  | SetMarkerAction
  | ChangeCurMarkerAction
  | ChangeExMarkerAction;
