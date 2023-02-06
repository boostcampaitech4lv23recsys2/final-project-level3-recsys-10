import * as T from "./types";

export const setLoading = (payload: T.State): T.SetLoadingAction => ({
  type: "@loading/setLoadingAction",
  payload,
});
