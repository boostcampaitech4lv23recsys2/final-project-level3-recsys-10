import * as T from "./types";

export const setMarkerInfo = (payload: T.State): T.SetMarkerInfoAction => ({
  type: "@marker/setMarkerInfo",
  payload,
});

export const setChangeCurMarker = (
  payload: number
): T.ChangeCurMarkerAction => ({
  type: "@marker/changeCurMarker",
  payload,
});

export const setUpdateCurMarker = (): T.ClearCurMarkerAction => ({
  type: "@marker/clearCurMarker",
});

export const setChangeMarkerList = (payload: string[]): T.ChangeMarkerList => ({
  type: "@marker/changeMarkerList",
  payload,
});
