import { useEffect, useRef, useState } from "react";
import type { FC } from "react";
import { ReactComponent as Heart } from "../heart.svg";

type targetInfo = {
  house: object;
};

const Card = () => {
  useEffect(() => {}, []);

  //   if (Object.keys(houseInfo).length === 0) return <></>;
  return (
    <div
      className="card"
      style={{
        margin: "0 1vw",
        width: "18rem",
        display: "inline-block",
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
        <img
          src="https://ic.zigbang.com/ic/items/35171998/12.jpg?w=800&h=600&q=70&a=1"
          className="card-img-top"
          alt="..."
        />
      </div>
      <div className="card-body">
        <h5 className="card-title">Card title</h5>
        <p className="card-text">
          Some quick example text to build on the card title and make up the
          bulk of the card's content.
        </p>
        <a href="#" className="btn btn-primary">
          Go somewhere
        </a>
      </div>
    </div>
  );
};

export default Card;
