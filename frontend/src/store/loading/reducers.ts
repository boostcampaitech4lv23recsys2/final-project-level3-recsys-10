import { useRef } from "react";
import * as T from "./types";

const initialState: T.State = {
  isLoading: false,
};

export const reducer = (state: T.State = initialState, action: T.Actions) => {
  switch (action.type) {
    case "@loading/setLoading":
      return action.payload;
  }
  return state;
};
