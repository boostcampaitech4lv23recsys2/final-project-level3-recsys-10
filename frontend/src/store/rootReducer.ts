import type { AppState } from "./AppState";

import { combineReducers } from "redux";
import * as User from "./user";

export const rootReducer = combineReducers({
  user: User.reducer,
});
