import * as T from "./types";

const initialState: T.State = { curMarkerList: [], exMarkerList: [] };

export const reducer = (state: T.State = initialState, action: T.Actions) => {
  switch (action.type) {
    case "@marker/setMarker":
      return action.payload;
    case "@marker/changeCurMarkerList":
      return { ...state, curMarkerList: action.payload };
    case "@marker/changeExMarkerList":
      return { ...state, exMarkerList: action.payload };
  }
  return state;
};
