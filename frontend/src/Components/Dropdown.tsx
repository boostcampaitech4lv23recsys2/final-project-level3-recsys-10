import { useCallback, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import * as D from "../data";
import { AppState } from "../store";
import * as U from "../store/user";
import * as H from "../store/house";
import * as L from "../store/loading";

export default function Dropdwon() {
  const [openMenu, setOpenMenu] = useState<boolean>(false);
  const dispatch = useDispatch();

  const { userId, userGu } = useSelector<AppState, U.State>(
    (state) => state.user
  );

  const onClickOpen = () => setOpenMenu(!openMenu);
  const navigate = useNavigate();
  const goBack = useCallback(() => {
    navigate(-1);
  }, [navigate]);

  // userId, userGu 전달하고 찜 목록 받아서 houselist 변경
  const onClickShowHeartList = useCallback(() => {
    dispatch(L.setLoading(true));
    D.fetchHouseByZzim({ user_id: userId, user_gu: userGu })
      .then((houses) => {
        const itemList = Object.values(houses).filter((item: any) =>
          Object.keys(item).includes("house_id")
        );
        if (itemList.length > 0) {
          dispatch(H.changeCurHouseList(itemList));
          dispatch(H.changeShowHouseList(itemList));
        } else {
          alert("관심목록에 정보가 없습니다.");
        }
        dispatch(L.setLoading(false));
      })
      .catch()
      .finally();
  }, [userGu]);

  const onClickLogout = () => {
    dispatch(U.setUserInfo({ userId: 0, userGu: "", infraList: [] }));
    navigate("/login");
  };
  const onClickChangeSetting = useCallback(() => {
    navigate("/infra");
  }, [navigate]);

  return (
    <div className="flex justify-center max-w-sm ">
      <div className="relative my-3">
        <button
          className="text-gray-900 bg-[#F7BE38] hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50 mr-2 mb-2"
          onClick={onClickOpen}
        >
          <div className="flex">
            <svg
              className="w-5 h-5 text-gray-800"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fillRule="evenodd"
                d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                clipRule="evenodd"
              />
            </svg>
            안녕하세요!
          </div>
        </button>

        {openMenu && (
          <div className="absolute left-0 z-20 w-48 py-2 mt-2 bg-white rounded-md shadow-xl">
            {/* <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
            >
              도움말 보기
            </a> */}
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
              onClick={onClickShowHeartList}
            >
              관심목록
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
              onClick={onClickChangeSetting}
            >
              설정 변경
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
              onClick={onClickLogout}
            >
              로그아웃
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
