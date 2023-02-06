import { useCallback, useEffect, useRef, useState } from "react";
import type { FC } from "react";
import { ReactComponent as Heart } from "../heart.svg";
import { makeFeeStr, makeInfraHtml } from "../utils/utils";
import * as H from "../store/house";
import * as D from "../data/fetchByUser";
import * as U from "../store/user";
import { AppState } from "../store";
import { useDispatch, useSelector } from "react-redux";

type myType = {
  item: any;
};

const SimpleListCard: FC<myType> = ({ item }) => {
  useEffect(() => {}, []);

  const imgPath = `${item["information"]["image_thumbnail"]}?w=800&h=600&q=70&a=1`;
  const title = item["information"]["title"];
  const wholeFee = makeFeeStr(item);

  const houseArea = item["information"]["house_area"];
  const address = item["information"]["address"];
  const infraHtml = makeInfraHtml(item["related_infra"]);
  const { zzim, house_id, ranking } = item;
  const isZzim = "Y" === item["zzim"];
  const isRecommended = 0 === ranking;
  const { userId } = useSelector<AppState, U.State>((state) => state.user);
  const dispatch = useDispatch();

  const onClickHeart = useCallback(() => {
    const nextZzim = "N" === zzim ? "Y" : "N";
    D.fetchZzimRegister({
      user_id: userId,
      house_id,
      zzim_yn: nextZzim,
    })
      .then((data) => {
        dispatch(H.updateHouseZzim({ houseId: house_id, zzim: nextZzim }));
      })
      .catch(() => {})
      .finally(() => {});
  }, []);

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
        {isRecommended && <span className="badge-high">추천매물</span>}
        {ranking > 0 && (
          <span className="badge-middle">{`랭킹 ${ranking} 위`}</span>
        )}
        <div className="flex">
          <strong className="mb-2 text-lg font-bold tracking-tight text-gray-900">
            {`${wholeFee} | ${houseArea}㎡`}
          </strong>
        </div>
        <p className="mb-3 font-normal text-gray-700 dark:text-gray-400">
          {infraHtml}
        </p>
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
