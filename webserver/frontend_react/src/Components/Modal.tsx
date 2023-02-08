import { Dispatch, SetStateAction, useEffect, useRef, useState } from "react";
import type { FC } from "react";

export const Modal: FC<{
  setOpenModal: Dispatch<SetStateAction<boolean>>;
}> = ({ setOpenModal }) => {
  const onClickBtn = () => {
    setOpenModal(false);
  };
  //   if (Object.keys(houseInfo).length === 0) return <></>;
  return (
    <div
      className="relative z-10"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <div className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"></div>
      <div className="fixed inset-0 z-10 overflow-y-auto">
        <div className="flex items-end justify-center min-h-full p-4 text-center sm:items-center sm:p-0">
          <div className="relative overflow-hidden text-left transition-all transform bg-white rounded-lg shadow-xl sm:my-8 sm:w-full sm:max-w-lg">
            <div className="px-4 pt-5 pb-4 bg-white sm:p-6 sm:pb-4">
              <div className="sm:flex sm:items-start">
                <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                  <h3
                    className="text-lg font-medium leading-6 text-gray-900"
                    id="modal-title"
                  >
                    1. 마커의 의미
                  </h3>
                  <div className="flex mt-2 mb-2">
                    <img src="recommend_marker.png"></img>
                    <span>추천 매물</span>
                    <img src="red_marker.png"></img>
                    <span>상위 25%</span>
                    <img src="blue_marker.png"></img>
                    <span>상위 75%</span>
                    <img src="gray_marker.png"></img>
                    <span>하위 25%</span>
                  </div>
                  <h3
                    className="mb-2 text-lg font-medium leading-6 text-gray-900"
                    id="modal-title"
                  >
                    2. AI 추천 받기 기능
                  </h3>
                  <span>
                    선택 구에서 다섯 개 이상의 매물에 좋아요를 누른 뒤 사용 가능
                  </span>
                  <h3
                    className="mt-2 mb-2 text-lg font-medium leading-6 text-gray-900"
                    id="modal-title"
                  >
                    3. 현재 화면에서 매물보기 기능
                  </h3>
                  <span>현재 보이는 화면에서 매물보기</span>
                  <h3
                    className="mt-2 mb-2 text-lg font-medium leading-6 text-gray-900"
                    id="modal-title"
                  >
                    4. 설정 변경 기능
                  </h3>
                  <span>인프라 및 기본 구 설정 변경</span>
                </div>
              </div>
            </div>
            <div className="px-4 py-3 bg-gray-50 sm:flex sm:flex-row-reverse sm:px-6">
              <button
                onClick={onClickBtn}
                type="button"
                className="inline-flex justify-center w-full px-4 py-2 text-base font-medium text-white bg-red-600 border border-transparent rounded-md shadow-sm hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm"
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Modal;
