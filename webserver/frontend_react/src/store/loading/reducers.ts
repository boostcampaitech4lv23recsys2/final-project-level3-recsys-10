import { useRef } from "react";
import * as T from "./types";

const initialState: T.State = false;

export const reducer = (state: boolean = initialState, action: T.Actions) => {
  switch (action.type) {
    case "@loading/setLoadingAction":
      return action.payload;
  }
  return state;
};
