import * as T from "./types";

const initialState: T.State = {
  curHouseList: [],
  exHouseList: [],
  showHouseList: [],
};

export const reducer = (state: T.State = initialState, action: T.Actions) => {
  switch (action.type) {
    case "@house/setHouse":
      return action.payload;
    case "@house/changeCurHouseList": {
      return { ...state, curHouseList: action.payload };
    }
    case "@house/changeExHouseList":
      return { ...state, exHouseList: action.payload };
    case "@house/changeShowHouseList":
      return { ...state, showHouseList: action.payload };
    case "@house/updateHouseZzim": {
      let tmpCurHouseList = state.curHouseList.map((item) => {
        if (item.houseId == action.payload.houseId) {
          const updatedItem = {
            ...item,
            zzim: action.payload.zzim,
          };
          return updatedItem;
        }
        return item;
      });
      return { ...state };
    }
  }
  return state;
};
