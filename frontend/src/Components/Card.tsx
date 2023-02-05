import { useEffect, useRef, useState } from "react";
import type { FC } from "react";
import { ReactComponent as Heart } from "../heart.svg";

import { useSelector, useDispatch } from "react-redux";
import * as H from "../store/house";
import { AppState } from "../store";
import { makeFeeStr, makeInfraHtml } from "../utils/utils";

type myType = {
  item: any;
};
const Card: FC<myType> = ({ item }) => {
  useEffect(() => {}, []);
  const imgPath = `https://ic.zigbang.com/ic/items/${item["information"]["zigbang_id"]}/2.jpg?w=800&h=600&q=70&a=1`;
  console.log(item["information"]["zigbang_id"]);
  const wholeFee = makeFeeStr(item);
  const { house_area, address } = item["information"];
  const infraHtml = makeInfraHtml(item["related_infra"]);

  //   if (Object.keys(houseInfo).length === 0) return <></>;
  return (
    <div
      className="card md:max-w-xl"
      style={{
        margin: "0 1vw",
        display: "inline-block",
        whiteSpace: "pre-wrap",
        // top: "10vw",
        // left: "20vw",
      }}
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
          <Heart />
        </button>
        <img src={imgPath} className="card-img-top" alt="..." />
      </div>
      <div className="card-body">
        <h5 className="card-title">{`${address}`} </h5>
        <h5 className="card-title">{`${wholeFee} | ${house_area}㎡`} </h5>
        <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
          {infraHtml}
        </p>
        <p className="card-text">
          {item["information"]["description"].replace(/<br>/g, "\n")}
        </p>
        <a href="#" className="btn btn-primary">
          Go somewhere
        </a>
      </div>
    </div>
  );
};

export default Card;
