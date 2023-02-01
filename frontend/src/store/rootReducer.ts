import type { Action } from "redux";
import type { Actions } from "./action";
import type { AppState } from "./AppState";

const initialAppState = {
  user_info: {
    user_id: 0,
    user_gu: "string",
    infra_list: [],
  },
  houses_info: [],
  ex_houses_info: [],
  cur_marker_list: [],
};

export const rootReducer = (
  state: AppState = initialAppState,
  action: Actions
) => {
  switch (action.type) {
    case "setUserInfo":
      return { ...state, userInfo: action.userInfo }; // action 을 반영한 상태 반환
  }
  return state;
};
