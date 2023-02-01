import { useEffect, useRef, useState } from "react";
import type { FC } from "react";
import Map from "../Map/Map";
import Recommend from "../Recommend";

type userInfo = {
  gu: string;
};

const Main: FC<userInfo> = ({ gu }) => {
  const mapElement = useRef(null);
  const [houseInfo, setHouseInfo] = useState<HouseInfo>({
    houses: {},
  });

  type HouseInfo = {
    houses: object;
  };

  // Make the `request` function generic
  // to specify the return data type:
  function request<HouseInfo>(
    url: string,
    // `RequestInit` is a type for configuring
    // a `fetch` request. By default, an empty object.
    config: RequestInit = {}

    // This function is async, it will return a Promise:
  ): Promise<void | HouseInfo> {
    // Inside, we call the `fetch` function with
    // a URL and config given:
    return (
      fetch(url, config)
        // When got a response call a `json` method on it
        .then((response) => response.json())
        // and return the result data.
        .then((data) => setHouseInfo(data))
    );
    // We also can use some post-response
    // data-transformations in the last `then` clause.
  }

  // Make the `request` function generic
  // to specify the return data type:
  async function request2<HouseInfo>(
    url: string,
    // `RequestInit` is a type for configuring
    // a `fetch` request. By default, an empty object.
    config: RequestInit = {}

    // This function is async, it will return a Promise:
  ): Promise<HouseInfo> {
    const response = await fetch(url, config);
    return await response.json();
  }

  useEffect(() => {
    request("http://27.96.130.120:30007/map/items", {
      method: "POST",
      mode: "cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({
        user_id: 1,
        user_gu: gu,
        house_ranking: {},
      }),
    });
  }, [gu]);

  return (
    <>
      {/* <button
        style={{
          top: "20.2vw",
          left: "75.2vw",
          zIndex: "2",
          position: "absolute",
        }}
        type="button"
        className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm p-2.5 text-center inline-flex items-center mr-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        필터
      </button>

      <div
        style={{
          top: "15.2vw",
          left: "63.2vw",
          zIndex: "2",
          height: "10vw",
          width: "10vw",
          position: "absolute",
        }}
        className="bg-white rounded-lg white-space: nowrap"
      >
        가격 필터 자리
      </div> */}
      <button
        style={{
          top: "2vh",
          left: "35.2vw",
          width: "20vw",
          zIndex: "2",
          position: "absolute",
        }}
        type="button"
        className="text-gray-900 bg-gradient-to-r from-red-200 via-red-300 to-yellow-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-red-100 dark:focus:ring-red-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
      >
        구 선택 창으로 사용
      </button>
      <button
        style={{
          top: "2vh",
          left: "70vw",
          zIndex: "2",
          position: "absolute",
        }}
        type="button"
        className="text-gray-900 bg-gradient-to-r from-red-200 via-red-300 to-yellow-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-red-100 dark:focus:ring-red-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
      >
        관심목록
      </button>
      <button
        style={{
          bottom: "2vh",
          left: "40.2vw",
          zIndex: "2",
          position: "absolute",
        }}
        type="button"
        className="text-gray-900 bg-gradient-to-r from-red-200 via-red-300 to-yellow-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-red-100 dark:focus:ring-red-400 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"
      >
        현재 화면에서 매물보기
      </button>
      <Map houses={houseInfo["houses"]} />
    </>
  );
};

export default Main;
