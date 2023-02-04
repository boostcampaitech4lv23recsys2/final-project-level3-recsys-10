import { useCallback, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Gu } from "./Gu";
import { InfraSelect } from "./InfraSelect";

import { GU_INFO } from "../../data/config/guConfig";
import { fetchAddInfra } from "../../data/fetchByUser";
import { useDispatch, useSelector } from "react-redux";

import * as U from "../../store/user";
import { AppState } from "../../store";
import { useSelect } from "react-select-search";

export default function InfoSetting() {
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [infraInfo, setInfraInfo] = useState<string[]>([]);
  const [guInfo, setGuInfo] = useState<string>("");

  const submitValidation = (): boolean => {
    if (4 < guInfo.length || 0 >= guInfo.length) return false;
    if (0 == infraInfo.length) return false;
    return true;
  };

  const curUserId = useSelector<AppState, U.State>(
    (state) => state.user
  ).userId;

  const goMain = useCallback(() => {
    if (false == submitValidation()) {
      alert("인프라와 구 정보를 모두 선택해주세요");
    } else {
      fetchAddInfra({
        user_id: curUserId,
        user_type: "",
        user_gu: guInfo,
        infra_list: infraInfo,
      })
        .then(({ user_id, user_gu, infra_list }) => {
          dispatch(
            U.setUserInfo({
              userId: user_id,
              userGu: user_gu,
              infraList: infra_list as string[],
            })
          );
          navigate("/");
        })
        .catch((e) => alert("오류가 발생했습니다. 잠시 후 다시 시도해주세요."))
        .finally();
      // userinfo 등록
      // navigation
      // fetch
    }
  }, [guInfo, infraInfo]);
  return (
    <div className="flex flex-col min-h-screen bg-gray-100 border border-gray-300 shadow-xl rounded-xl">
      <div className="flex flex-col items-center justify-center flex-1 max-w-sm px-2 mx-auto">
        <div className="w-full px-6 py-8 text-black bg-white rounded shadow-md">
          <form className="relative">
            <div>
              <Gu
                setGu={setGuInfo}
                className="z-10 mb-4 w-80 basic-single"
              ></Gu>
            </div>
            <div className="mb-80">
              <InfraSelect
                setInfra={setInfraInfo}
                selectedInfra={infraInfo}
              ></InfraSelect>
            </div>

            <button
              type="button"
              className="w-full btn text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
              onClick={goMain}
            >
              집 보러 가기
            </button>
          </form>
          <p className="text-xs text-center text-gray-500">
            &copy;2023 Hobbang Corp. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}
