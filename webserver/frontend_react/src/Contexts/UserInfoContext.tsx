import { List } from "postcss/lib/list";
import type { FC, PropsWithChildren } from "react";
import { createContext, useContext } from "react";

type ContextType = {
  userId: number;
  userGu: string;
  userInfra: string[];
};

const defaultContextValue: ContextType = {
  userId: -1,
  userGu: "",
  userInfra: [""],
};

export const UserInfoContext = createContext<ContextType>(defaultContextValue);

type UserInfoProviderProps = {};
export const UserInfoProvider: FC<PropsWithChildren<UserInfoProviderProps>> = ({
  children,
  ...props
}) => {
  const userId = -1;
  const userGu = "";
  const userInfra = [""];
  const value = {
    userId,
    userGu,
    userInfra,
  };
  return <UserInfoContext.Provider value={value} children={children} />;
};

export const useUserInfo = () => {
  const { userId, userGu, userInfra } = useContext(UserInfoContext);
  return { userId, userGu, userInfra };
};
