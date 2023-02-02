import { useEffect, useRef, useState } from "react";
import type { FC } from "react";
import { ReactComponent as Heart } from "../heart.svg";

type myType = {
  item: any;
};
export const getFeeStr = (fee: number): string => {
  let remainder = fee % 10000;
  let quotient = Math.floor(fee / 10000);
  let res = `${quotient}억 ${remainder}`;
  res = 0 === quotient ? res.slice(3) : res;
  res = 0 === remainder ? res.slice(0, res.length - 1) : res;
  return res;
};

export const getSalesTypeStr = (rentFee: number): string => {
  return 0 == rentFee ? "전세" : "월세";
};

export const getWholeFeeStr = (
  salesStr: string,
  feeStr: string,
  rentFee: number
): string => {
  let res = `${salesStr} ${feeStr}`;

  if (0 !== rentFee) {
    res = `${res} / ${rentFee}`;
  }

  return res;
};

const SimpleListCard: FC<myType> = ({ item }) => {
  useEffect(() => {}, []);

  const imgPath = `${item["information"]["image_thumbnail"]}?w=800&h=600&q=70&a=1`;
  const title = item["information"]["title"];
  const curFeeStr = getFeeStr(item["information"]["price_deposit"]);
  const curSalesType = getSalesTypeStr(
    item["information"]["price_monthly_rent"]
  );
  const wholeFee = getWholeFeeStr(
    curSalesType,
    curFeeStr,
    item["information"]["price_monthly_rent"]
  );

  const address = item["information"]["address"];
  const isZzim = "Y" === item["zzim"];

  //   if (Object.keys(houseInfo).length === 0) return <></>;
  return (
    <a
      href="#"
      className="flex grid flex-col items-center grid-cols-2 bg-white border border-gray-200 rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700"
    >
      <div style={{ position: "relative" }}>
        <button
          style={{
            bottom: "0",
            right: "0.3vw",
            position: "absolute",
            height: "180%",
          }}
        >
          {/* <Heart fill="#ff385c" /> */}
          {true === isZzim ? <Heart fill="#ff385c" /> : <Heart />}
        </button>
        <img
          className="object-cover w-full ml-1 rounded-t-lg rounded-r-lg h-96 md:h-auto md:w-auto md:rounded-none md:rounded-l-lg md:rounded-r-lg"
          src={imgPath}
          alt=""
        />
      </div>
      <div className="flex flex-col justify-between p-4 leading-normal">
        <strong className="mb-2 text-lg font-bold tracking-tight text-gray-900 dark:text-white">
          {wholeFee}
        </strong>
        <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
          {address}
        </p>
        <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
          {title}
        </p>
      </div>
    </a>
  );
};

export default SimpleListCard;
