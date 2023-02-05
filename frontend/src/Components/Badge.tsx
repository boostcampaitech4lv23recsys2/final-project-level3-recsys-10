import { useCallback } from "react";
import { useNavigate } from "react-router-dom";

export default function Badge() {
  // 찜매물 안나옴  / 추천 매물 빨간색 / ranking 노란색
  return (
    <span className="w-20 bg-pink-100 text-pink-800 text-sm font-medium mr-2 px-2.5 py-0.5 rounded dark:bg-pink-900 dark:text-pink-300">
      추천매물
    </span>
  );
}
