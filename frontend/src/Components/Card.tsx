import { useCallback, useEffect, useRef, useState } from "react";
import type { FC } from "react";
import { ReactComponent as Heart } from "../heart.svg";

import { useSelector, useDispatch } from "react-redux";
import * as H from "../store/house";
import * as U from "../store/user";
import * as D from "../data/fetchByUser";
import { AppState } from "../store";
import { makeFeeStr, makeInfraHtml } from "../utils/utils";
import { resolve } from "path";

type myType = {
  item: any;
};
const Card: FC<myType> = ({ item }) => {
  useEffect(() => {}, []);
  const imgPath = `https://ic.zigbang.com/ic/items/${item["information"]["zigbang_id"]}/2.jpg?w=800&h=600&q=70&a=1`;
  const wholeFee = makeFeeStr(item);
  const { house_area, address, zigbang_id } = item["information"];
  const infraHtml = makeInfraHtml(item["related_infra"]);
  const { zzim, house_id, ranking } = item;
  const isZzim = "Y" === item["zzim"];
  const isRecommended = 0 === ranking;
  const dispatch = useDispatch();
  const { userId } = useSelector<AppState, U.State>((state) => state.user);
  const onClickHeart = useCallback(() => {
    const nextZzim = "N" === zzim ? "Y" : "N";
    D.fetchZzimRegister({
      user_id: userId,
      house_id,
      zzim_yn: nextZzim,
    })
      .then((data) => {
        dispatch(H.updateHouseZzim({ houseId: house_id, zzim: nextZzim }));
        item["zzim"] = nextZzim;
      })
      .catch(() => {})
      .finally(() => {});
  }, [item]);

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
          onClick={onClickHeart}
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
        <img src={imgPath} className="card-img-top" alt="..." />
      </div>
      <div className="card-body">
        {isRecommended && <span className="badge-high">추천매물</span>}
        {ranking > 0 && (
          <span className="badge-middle">{`랭킹 ${ranking} 위`}</span>
        )}
        <h5 className="card-title">{`${address}`} </h5>
        <h5 className="card-title">{`${wholeFee} | ${house_area}㎡`} </h5>
        <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
          {infraHtml}
        </p>
        <p className="card-text">
          {item["information"]["description"].replace(/<br>/g, "\n")}
        </p>
        <a
          href="#"
          className="btn"
          style={{ background: "#FFC600", color: "black" }}
          onClick={() =>
            window.open(
              `https://www.zigbang.com/home/oneroom/items/${zigbang_id}`,
              "_blank"
            )
          }
        >
          직방에서 매물 더 보기
        </a>
      </div>
    </div>
  );
};

export default Card;
