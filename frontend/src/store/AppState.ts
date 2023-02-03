import * as User from "./user";
import * as House from "./house";

export type AppState = {
  user: User.State;
  house: House.State;
};
