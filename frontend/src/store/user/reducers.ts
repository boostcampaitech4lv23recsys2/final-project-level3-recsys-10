import * as T from "./types";

const initialState: T.State = { userId: 0, userGu: "", infraList: [] };

export const reducer = (state: T.State = initialState, action: T.Actions) => {
  switch (action.type) {
    case "@user/setUserInfo":
      return action.payload;
    case "@user/changeGu":
      return { ...state, userGu: action.payload };
    case "@user/changeInfra":
      return { ...state, userInfra: action.payload };
  }
  return state;
};
