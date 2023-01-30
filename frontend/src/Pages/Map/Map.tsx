import type { FC } from "react";
import { useEffect, useRef, useState } from "react";

type HouseInfo = {
  houses: object;
};

const Map: FC<HouseInfo> = ({ houses }) => {
  const mapElement = useRef(null);

  useEffect(() => {
    const { naver } = window;
    if (!mapElement.current || !naver) return;

    // 지도에 표시할 위치의 위도와 경도 좌표를 파라미터로 넣어줍니다.
    const location = new naver.maps.LatLng(37.5656, 126.9769);
    const mapOptions: naver.maps.MapOptions = {
      center: location,
      zoom: 13,
      zoomControl: false,
    };
    const map = new naver.maps.Map(mapElement.current, mapOptions);
    Object.values(houses).forEach((elem) => {
      let m = new naver.maps.Marker({
        position: new naver.maps.LatLng(elem["lat"], elem["lng"]),
        map: map,
      });
      return m;
    });

    new naver.maps.Marker({
      position: location,
      map,
    });
  }, [houses]);

  return (
    <>
      <div ref={mapElement} style={{ minHeight: "100vh" }} />
    </>
  );
};

export default Map;
