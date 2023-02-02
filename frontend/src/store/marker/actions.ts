import type * as T from "./types";

export const setMarker = (payload: T.State): T.SetMarkerAction => ({
  type: "@marker/setMarker",
  payload,
});

export const changeCurMarkerList = (
  payload: unknown[]
): T.ChangeCurMarkerAction => ({
  type: "@marker/changeCurMarkerList",
  payload,
});

export const changeExMarkerList = (
  payload: unknown[]
): T.ChangeExMarkerAction => ({
  type: "@marker/changeExMarkerList",
  payload,
});
