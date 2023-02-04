import * as T from "./types";

const initialState: T.State = { curMarker: undefined, markerList: [] };

export const reducer = (state: T.State = initialState, action: T.Actions) => {
  switch (action.type) {
    case "@marker/setMarkerInfo":
      return action.payload;
    case "@marker/changeCurMarker":
      return { ...state, curMarker: action.payload };
    case "@marker/clearCurMarker":
      return { ...state, curMarker: undefined };
    case "@marker/changeMarkerList":
      return { ...state, markerList: action.payload };
  }
  return state;
};
