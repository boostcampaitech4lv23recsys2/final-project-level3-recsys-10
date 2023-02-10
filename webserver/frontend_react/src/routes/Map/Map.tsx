import type { FC } from "react";
import { useCallback, useEffect, useRef, useState } from "react";
import Sidebar from "../../Components/Sidebar";
import "./Map.css";

import { useSelector, useDispatch } from "react-redux";
import * as H from "../../store/house";
import * as U from "../../store/user";
import * as M from "../../store/marker";
import * as L from "../../store/loading";
import * as D from "../../data/fetchByUser";
import { AppState } from "../../store";
import internal from "stream";
import { fetchHouseByCoord } from "../../data";
import { INFRA_INFO_DICT } from "../../data/config/infraConfig";
import { IInfraInfo } from "../../utils/utils";
import Loading from "../Loading";

type HouseInfo = {
  houses: any[];
};

const getBoundsByShowHouse = (targetHouses: any[]) => {
  let minLat = 0;
  let minLng = 0;
  let maxLat = 0;
  let maxLng = 0;
  if (targetHouses.length == 0) {
    // 아직 대상이 업데이트 되지 않음
    return { minLat, minLng, maxLat, maxLng };
  }
  maxLat = targetHouses
    .map((h) => h.lat)
    .reduce((max, curr) => (max < curr ? curr : max));
  minLat = targetHouses
    .map((h) => h.lat)
    .reduce((min, curr) => (min > curr ? curr : min));
  maxLng = targetHouses
    .map((h) => h.lng)
    .reduce((max, curr) => (max < curr ? curr : max));
  minLng = targetHouses
    .map((h) => h.lng)
    .reduce((min, curr) => (min > curr ? curr : min));

  return { minLat, minLng, maxLat, maxLng };
};

const onClickGetCurrentHouses = (map: HTMLElement | null | any) => {
  const { sw, ne } = map.getBounds();
  console.log(sw, ne);
};

const makeMarker = (
  map: HTMLElement | null | any,
  houseInfoList: any[]
): any[] => {
  const houseNum = houseInfoList.length;
  const first = houseNum * 0.25;
  const second = houseNum * 0.75;
  let zIndex = 1;

  return houseInfoList.map((item, idx) => {
    let iconPath = "blue_marker.png";
    const isRecommended = 0 >= item["ranking"];
    // const isAIRecommended = -2 === item["ranking"];
    const isZzim = -1 === item["ranking"];

    if (idx <= first) {
      iconPath = "red_marker.png";
      zIndex = 2;
    } else if (idx > second) {
      iconPath = "gray_marker.png";
      zIndex = 0;
    }

    iconPath = true === isRecommended ? "recommend_marker.png" : iconPath;
    // iconPath = true === isAIRecommended ? "recommend_marker.png" : iconPath;
    iconPath = true === isZzim ? "heart.png" : iconPath;
    zIndex = true === isRecommended ? 3 : zIndex;
    // zIndex = true === isAIRecommended ? 3 : zIndex;

    return new naver.maps.Marker({
      position: new naver.maps.LatLng(item["lat"], item["lng"]),
      icon: {
        url: iconPath,
      },
      zIndex,
      map: map,
    });
  });
};

const Map: FC<HouseInfo> = ({ houses }) => {
  const mapElement = useRef<HTMLElement | null | any>(null);
  const { naver } = window;
  let [curMap, setCurMap] = useState<any>(null);
  let [markerList, setMarkerList] = useState<any>([]);
  let [houseMarkerList, setHouseMarkerList] = useState<any>([]);
  let [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(true);

  const clickedMarker = useRef<any | null>(null);

  const dispatch = useDispatch();
  const houseInfoManage = useSelector<AppState, H.State>(
    (state) => state.house
  );

  const isLoading = useSelector<AppState, L.State>((state) => state.loading);
  const { curMarker } = useSelector<AppState, M.State>((state) => state.marker);
  const { userId, userGu } = useSelector<AppState, U.State>(
    (state) => state.user
  );

  const onClickCurrentScreen = () => {
    let minLng = curMap.getBounds().getSW().x;
    let minLat = curMap.getBounds().getSW().y;
    let maxLng = curMap.getBounds().getNE().x;
    let maxLat = curMap.getBounds().getNE().y;
    dispatch(L.setLoading(true));

    fetchHouseByCoord({
      user_id: userId,
      user_gu: userGu,
      min_lat: minLat,
      min_lng: minLng,
      max_lat: maxLat,
      max_lng: maxLng,
    }).then(({ houses, code }) => {
      dispatch(L.setLoading(false));
      const itemList = Object.values(houses).filter((item: any) =>
        Object.keys(item).includes("house_id")
      );

      if (code > 0 && itemList.length > 0) {
        dispatch(H.changeCurHouseList(itemList));
        dispatch(H.changeShowHouseList(itemList));
      } else {
        alert("현재 위치에 매물이 없습니다.");
      }
    });
  };

  const onClickAIBtn = () => {
    dispatch(L.setLoading(true));

    D.fetchHouseByRecommend({
      userId,
      userGu,
    }).then(({ houses, code }) => {
      dispatch(L.setLoading(false));
      if (houses === undefined || code <= 0) {
        alert(
          `${userGu}에서 다섯 개 이상의 매물에 좋아요를 누른 뒤 다시 시도해주세요.`
        );
      } else {
        const itemList = Object.values(houses).filter((item: any) =>
          Object.keys(item).includes("house_id")
        );
        if (code > 0 && itemList.length > 0) {
          dispatch(H.changeCurHouseList(Object.values(houses)));
          dispatch(H.changeShowHouseList(Object.values(houses)));
        }
      }
    });
  };

  useEffect(() => {
    if (!mapElement.current || !naver) return;
    if (houses.length === 0) return;

    // 구가 바뀌었으니 보여줄 매물을 전체 매물로 설정
    // dispatch(H.changeShowHouseList(houses));
    // sidebar 열어준다.
    setIsSidebarOpen(true);

    // 지도에 표시할 위치의 위도와 경도 좌표를 파라미터로 전달
    const { minLat, minLng, maxLat, maxLng } = getBoundsByShowHouse(houses);

    // const location = new naver.maps.LatLng(37.5656, 126.9769);
    const mapOptions: naver.maps.MapOptions = {
      bounds: new naver.maps.LatLngBounds(
        new naver.maps.LatLng(minLat, minLng),
        new naver.maps.LatLng(maxLat, maxLng)
      ),
      // center: location, bound 에 의해 결정됨
      // zoom: 13,bound 에 의해 결정됨
      zoomControl: false,
    };
    const map = new naver.maps.Map(mapElement.current, mapOptions);
    setCurMap(map);

    const clickMarkerEvent: any = (event: any, idx: number) => {
      // if (false == markerList.empty) {
      //   markerList.forEach((item: any) => item.setMap(null));
      // }
      if (!!clickedMarker.current) {
        // BOUNCE 중지
        clickedMarker.current.setAnimation(0);
      }

      // BOUNCE
      event.overlay.setAnimation(1);
      clickedMarker.current = event.overlay;

      const curDetailInfo = houses[idx]["related_infra"];
      map.setZoom(16);
      map.panTo(event.coord);

      let curMarkerList: any = [];
      curMarkerList = Object.keys(curDetailInfo).map((infraKey: string) => {
        return new naver.maps.Marker({
          position: new naver.maps.LatLng(
            curDetailInfo[infraKey]["lat"],
            curDetailInfo[infraKey]["lng"]
          ),
          icon: {
            content: [
              '<div class="pin bounce">',
              INFRA_INFO_DICT[infraKey as keyof IInfraInfo]["emoji"],
              INFRA_INFO_DICT[infraKey as keyof IInfraInfo]["ko"],
              "</div>",
            ].join(""),
          },
          // icon: "hobbang_favicon_outline.png",
          map: map,
        });
      });
      D.fetchAddClickLog({
        user_id: userId,
        house_id: houses[idx]["house_id"],
        log_type: "M",
      })
        .then()
        .catch()
        .finally();

      // Object.values(curDetailInfo).forEach((item: any) => {
      //   let curMarker = new naver.maps.Marker({
      //     position: new naver.maps.LatLng(item["lat"], item["lng"]),
      //     icon: {
      //       content: [
      //         '<div class="pin bounce">',
      //         INFRA_INFO_DICT["01"]["ko"],
      //         "</div>",
      //       ].join(""),
      //     },
      //     // icon: "hobbang_favicon_outline.png",
      //     map: map,
      //   });
      //   curMarkerList.push(curMarker);
      // });
      setIsSidebarOpen(true);
      // 이전에 있던 infra markr 제거 후 현재 infra marker 로 설정
      setMarkerList((markers: any) => {
        markers.forEach((item: any) => item.setMap(null));
        return curMarkerList;
      });
      dispatch(H.changeShowHouseList([houses[idx]]));
    };

    const houseInfoList = houses;
    const houseNum = houseInfoList.length;

    let markers: any = makeMarker(map, houseInfoList);
    // forEach 를 이용하면 marker 가 순서대로 담기지 않을 수 있다.
    // for (let idx = 0; idx < houseNum; ++idx) {
    //   const curItem = houseInfoList[idx];
    //   let marker = new naver.maps.Marker({
    //     position: new naver.maps.LatLng(curItem["lat"], curItem["lng"]),
    //     icon: {
    //       url: "recommend_marker.png",
    //     },
    //     map: map,
    //   });
    //   markers.push(marker);
    // }

    // var marker = new naver.maps.Marker({
    //   position: new naver.maps.LatLng(37.3595704, 127.105399),
    //   icon: {
    //     content: [
    //       '<div class="crown"></dev>',
    //       '<div class="pin bounce">',
    //       "상금",
    //       "</div>",
    //       '<div class="pin bounce">',
    //       "500만원",
    //       "</div>",
    //     ].join(""),
    //   },
    //   map: map,
    // });

    for (let idx = 0; idx < houseNum; ++idx) {
      naver.maps.Event.addListener(markers[idx], "click", (e) =>
        clickMarkerEvent(e, idx)
      );
    }

    setHouseMarkerList((m: any) => {
      m.forEach((item: any) => item.setMap(null));
      return markers;
    });
  }, [houses]);

  if (houses.length === 0 && true === isLoading) return <Loading></Loading>;
  else {
    return (
      <>
        {true == isSidebarOpen && (
          <Sidebar
            setIsSidebarOpen={setIsSidebarOpen}
            itemList={houseInfoManage.showHouseList}
            markerList={houseMarkerList}
          />
        )}

        {/* <div className="z-10 top-10 absolute duration-300 group  text-gray-900  focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50 mr-2 mb-2">
          <img src="hobbang_favicon_outline.png"></img>
          <span className="absolute hidden group-hover:flex -top-2 -right-3 translate-x-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm before:content-[''] before:absolute before:top-1/2  before:right-[100%] before:-translate-y-1/2 before:border-8 before:border-y-transparent before:border-l-transparent before:border-r-gray-700">
            인공지능 추천 버튼 ! <br></br> 다섯개 이상의 매물에 <br></br>
            좋아요를 누르고 <br></br>저를 눌려보세요.<br></br>선택하신 구에서 더
            정교한 매물 추천을 드립니다.
          </span>
        </div> */}

        {
          <button
            style={{
              left: "0.5vw",
              top: "10vh",
              zIndex: "2",
              position: "absolute",
            }}
            type="button"
            className="duration-300 group  text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50 mr-2 mb-2"
            onClick={onClickAIBtn}
          >
            {`AI 매물 추천`}
            <span className="absolute hidden group-hover:flex -top-2 -right-3 translate-x-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm before:content-[''] before:absolute before:top-1/2  before:right-[100%] before:-translate-y-1/2 before:border-8 before:border-y-transparent before:border-l-transparent before:border-r-gray-700">
              인공지능 추천 버튼 ! <br></br> 해당 구에서 <br></br> 다섯개 이상의
              매물에 <br></br>
              좋아요를 보유한 분들께 <br></br>선택하신 구에서 더 정교한 매물
              추천을 드립니다.
            </span>
          </button>
        }

        {/* <button
          style={{
            left: "0.5vw",
            top: "20vh",
            zIndex: "2",
            position: "absolute",
          }}
          type="button"
          className="duration-300 group  text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50 mr-2 mb-2"
        >
          {`${userGu} 가격`}
          <div className="absolute hidden group-hover:flex -top-2 -right-3 translate-x-full w-48 px-2 py-1 bg-gray-700 rounded-lg text-center text-white text-sm before:content-[''] before:absolute before:top-1/2  before:right-[100%] before:-translate-y-1/2 before:border-8 before:border-y-transparent before:border-l-transparent before:border-r-gray-700">
            전세{" "}
            <a>
              <input
                type="range"
                min="0"
                max="100"
                value="40"
                className="multi-range"
              />
            </a>
          </div>
        </button> */}
        <button
          style={{
            bottom: "2vh",
            left: "43vw",
            zIndex: "2",
            position: "absolute",
          }}
          type="button"
          className="text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50 mr-2 mb-2"
          onClick={onClickCurrentScreen}
        >
          현재 화면에서 매물보기
        </button>
        <div ref={mapElement} style={{ minHeight: "100vh" }} />
      </>
    );
  }
};

export default Map;
