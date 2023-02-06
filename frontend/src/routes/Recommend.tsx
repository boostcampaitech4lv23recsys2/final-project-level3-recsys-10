import { useEffect, useRef, useState } from "react";
import type { FC } from "react";
import Card from "../Components/Card";
import { ReactComponent as Back } from "../back.svg";

type userInfo = {
  gu: string;
};

const warningMsg = [
  "집을 계약할 때는 채광 및 환기도 체크해보세요.",
  "화장실에 창문과 환풍기가 없으면 곰팡이가 피기 쉬워요.",
  "화장실 수압이 적당한지 악취가 나지는 않는지, 녹물이 나오는지를 확인해보세요.",
  "집 주변 소음이 심하지 않은지 확인해보세요.",
  "냉장고 뒷쪽과 아랫쪽에 곰팡이가 있진 않은지 확인해보세요.",
  "제시한 옵션이 잘 있는지, 상태는 괜찮은지 확인해보세요.",
];

function getRandomInt(min: number, max: number) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //최댓값은 제외, 최솟값은 포함
}

const Recommend = () => {
  const numOfWarning = warningMsg.length;

  //   if (Object.keys(houseInfo).length === 0) return <></>;
  return (
    // <></>
    <div className="flex flex-col min-h-screen bg-gray-100 border border-gray-300 shadow-xl rounded-xl w-30">
      <div className="flex flex-col items-center justify-center flex-1 max-w-sm px-2 mx-auto">
        <div className="w-full px-6 py-8 text-black bg-white rounded shadow-md">
          <div className="flex justify-center mb-2">
            <img src="hobbang_favicon_outline.png"></img>
            <div> 매물을 검색하고 있습니다.</div>
          </div>
          <div> Tip. {warningMsg[getRandomInt(0, numOfWarning)]}</div>
        </div>
      </div>
    </div>
  );
};

export default Recommend;
