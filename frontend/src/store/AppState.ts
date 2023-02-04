import * as User from "./user";
import * as House from "./house";
import * as Marker from "./marker";

export type AppState = {
  user: User.State;
  house: House.State;
  marker: Marker.State;
};
