import { useEffect, useRef, useState } from "react";
import type { FC } from "react";
import Card from "../Components/Card";
import { ReactComponent as Back } from "../back.svg";

type userInfo = {
  gu: string;
};

const Recommend = () => {
  useEffect(() => {}, []);

  //   if (Object.keys(houseInfo).length === 0) return <></>;
  return (
    <></>
    // <div
    //   style={{
    //     left: "0",
    //     top: "0",
    //     position: "fixed",
    //     background: "rgba(0, 0, 0, 0.7)",
    //     minHeight: "100vh",
    //     width: "100%",
    //     height: "100%",
    //     color: "#fffff",
    //     zIndex: "4",
    //   }}
    // >
    //   <div
    //     style={{
    //       position: "absolute",
    //       display: "block",
    //       textAlign: "center",
    //       margin: "10",
    //       float: "left",
    //       textAlignLast: "center",
    //     }}
    //   >
    //     <Card></Card>
    //     <Card></Card>
    //     <Card></Card>
    //   </div>
    // </div>
  );
};

export default Recommend;
