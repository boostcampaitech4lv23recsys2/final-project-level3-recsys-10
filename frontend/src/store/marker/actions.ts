import type * as T from "./types";

export const setMarkerInfo = (payload: T.State): T.SetMarkerInfo => ({
  type: "@marker/setMarkerInfo",
  payload,
});

export const setChangeCurMarker = (
  payload: number
): T.ChangeCurMarkerAction => ({
  type: "@marker/changeCurMarker",
  payload,
});

export const setUpdateCurMarker = (
  payload: string
): T.ClearCurMarkerAction => ({
  type: "@marker/clearCurMarker",
});

export const setChangeMarkerList = (payload: string[]): T.ChangeMarkerList => ({
  type: "@marker/changeMarkerList",
  payload,
});
