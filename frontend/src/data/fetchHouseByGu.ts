import { URLSearchParams } from "url";
import {
  BACKEND_ADDRESS,
  DOMAIN_INFO,
  FETCH_BASIC_OPTION,
} from "./config/serverConfig";

export type IUser = {
  user_id: number;
  user_gu: string;
  infra_list: string[] | null;
};
