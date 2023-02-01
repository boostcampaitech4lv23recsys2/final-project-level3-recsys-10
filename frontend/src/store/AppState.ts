export type IUserInfo = {
  user_id: number;
  user_gu: string;
  infra_list: string[];
};

export type AppState = {
  user_info: IUserInfo;
  houses_info: any[];
  ex_houses_info: any[];
  cur_marker_list: any[];
};
