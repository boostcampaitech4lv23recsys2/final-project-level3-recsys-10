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
    <form className="relative">
      <div className="mb-80">
        <InfraSelect
          setInfra={setInfraInfo}
          selectedInfra={infraInfo}
        ></InfraSelect>
      </div>
      <div>
        <Gu setGu={setGuInfo}></Gu>
      </div>
      <button
        type="button"
        className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        onClick={goMain}
      >
        집 보러 가기
      </button>
    </form>
  );
}
