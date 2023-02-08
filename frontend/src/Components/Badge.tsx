import { useEffect, useRef, useState } from "react";
import type { FC } from "react";

type userInfo = {
  gu: string;
};

type IBadgeInfo = {
  importance: number;
  rank: number;
};

// ranking 이랑 importance
const Badge: FC<IBadgeInfo> = ({ importance, rank }) => {
  useEffect(() => {}, []);
  if (importance === 1) {
    const className = "badge-high";
  }

  //   if (Object.keys(houseInfo).length === 0) return <></>;
  return (
    <span className="w-20 bg-pink-100 text-pink-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-pink-900 dark:text-pink-300">
      추천매물
    </span>
  );
};

export default Badge;
