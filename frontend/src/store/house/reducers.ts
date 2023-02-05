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
        if (item.house_id == action.payload.houseId) {
          const updatedItem = {
            ...item,
            zzim: action.payload.zzim,
          };
          return updatedItem;
        }
        return item;
      });

      let tmpCurHouseList2 = state.showHouseList.map((item) => {
        if (item.house_id == action.payload.houseId) {
          const updatedItem = {
            ...item,
            zzim: action.payload.zzim,
          };
          return updatedItem;
        }
        return item;
      });
      return {
        ...state,
        curHouseList: tmpCurHouseList,
        showHouseList: tmpCurHouseList2,
      };
    }
  }
  return state;
};
