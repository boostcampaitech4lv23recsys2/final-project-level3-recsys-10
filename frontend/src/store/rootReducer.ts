import type { AppState } from "./AppState";

import { combineReducers } from "redux";
import * as User from "./user";
import * as House from "./house";

export const rootReducer = combineReducers({
  user: User.reducer,
  house: House.reducer,
});
