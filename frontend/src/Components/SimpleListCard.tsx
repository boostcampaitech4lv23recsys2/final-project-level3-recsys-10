import { useEffect, useRef, useState } from "react";
import type { FC } from "react";

type userInfo = {
  gu: string;
};

const SimpleListCard = () => {
  useEffect(() => {}, []);

  //   if (Object.keys(houseInfo).length === 0) return <></>;
  return (
    <a
      href="#"
      className="grid grid-cols-2 flex flex-col items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row md:max-w-xl hover:bg-gray-100 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700"
    >
      <img
        className="ml-1 object-cover w-full rounded-t-lg rounded-r-lg h-96 md:h-auto md:w-auto md:rounded-none md:rounded-l-lg md:rounded-r-lg"
        src="https://ic.zigbang.com/ic/items/35171998/12.jpg?w=800&h=600&q=70&a=1"
        alt=""
      />
      <div className="flex flex-col justify-between p-4 leading-normal">
        <strong className="mb-2 text-lg font-bold tracking-tight text-gray-900 dark:text-white">
          월세 200만원
        </strong>
        <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
          이런 저런 집입니다.
        </p>
      </div>
    </a>
  );
};

export default SimpleListCard;
