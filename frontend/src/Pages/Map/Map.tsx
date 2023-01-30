import type { FC } from "react";
import { useEffect, useRef, useState } from "react";

type HouseInfo = {
  houses: object;
};

const Map: FC<HouseInfo> = ({ houses }) => {
  const mapElement = useRef(null);
  const { naver } = window;
  let [showList, setShowList] = useState(Object.values(houses));
  let [markerList, setMarkerList] = useState<any>([]);

  useEffect(() => {
    if (!mapElement.current || !naver) return;

    // 지도에 표시할 위치의 위도와 경도 좌표를 파라미터로 넣어줍니다.
    const location = new naver.maps.LatLng(37.5656, 126.9769);
    const mapOptions: naver.maps.MapOptions = {
      center: location,
      zoom: 13,
      zoomControl: false,
    };
    const map = new naver.maps.Map(mapElement.current, mapOptions);

    const clickMarkerEvent: any = (event: any, idx: number) => {
      if (false == markerList.empty) {
        markerList.forEach((item: any) => item.setMap(null));
      }
      const curDetailInfo = Object.values(houses)[idx]["related_infra"];
      map.setZoom(16);
      map.panTo(event.coord);

      let curMarkerList: any = [];
      Object.values(curDetailInfo).forEach((item: any) => {
        let curMarker = new naver.maps.Marker({
          position: new naver.maps.LatLng(item["lat"], item["lng"]),
          icon: "hobbang_favicon_outline.png",
          map: map,
        });
        curMarkerList.push(curMarker);
      });
      setMarkerList((markers: any) => {
        markers.forEach((item: any) => item.setMap(null));
        return curMarkerList;
      });
    };

    const houseInfoList = Object.values(houses);
    const houseNum = houseInfoList.length;

    let markers = [];
    // forEach 를 이용하면 marker 가 순서대로 담기지 않을 수 있다.
    for (let idx = 0; idx < houseNum; ++idx) {
      const curItem = houseInfoList[idx];
      let marker = new naver.maps.Marker({
        position: new naver.maps.LatLng(curItem["lat"], curItem["lng"]),
        map: map,
      });

      markers.push(marker);
    }

    for (let idx = 0; idx < houseNum; ++idx) {
      naver.maps.Event.addListener(markers[idx], "click", (e) =>
        clickMarkerEvent(e, idx)
      );
    }
  }, [houses]);

  return (
    <>
      <div ref={mapElement} style={{ minHeight: "100vh" }} />
    </>
  );
};

export default Map;
