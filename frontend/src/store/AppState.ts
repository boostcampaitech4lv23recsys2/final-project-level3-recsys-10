import * as User from "./user";
import * as House from "./house";
import * as Marker from "./marker";
import * as Loading from "./loading";

export type AppState = {
  user: User.State;
  house: House.State;
  marker: Marker.State;
  loading: Loading.State;
};
