import type { Action } from "redux";

export type State = {
  isLoading: boolean;
};

export type SetLoadingAction = Action<"@loading/setLoading"> & {
  payload: State;
};

export type Actions = SetLoadingAction;
