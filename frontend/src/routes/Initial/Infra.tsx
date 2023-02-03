import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { INFRA_INFO_LIST } from "../../data/config/infraConfig";
import SelectSearch from "react-select-search";
import { Gu } from "./Gu";
import { InfraSelect } from "./InfraSelect";
import "react-select-search/style.css";

type IInfraInfo = {
  en: string;
  ko: string;
  code: string;
  img: string;
  icon: string;
  emoji: string;
  is_use: boolean;
};

// {
//     en: "subway",
//     ko: "지하철",
//     code: "01",
//     img: "",
//     icon: "subway_hobbang.png",
//     emoji: "&//128650;",
//     is_use: true,
//   },

export default function Infra() {
  let [selectedInfra, setSelectedInfra] = useState<IInfraInfo[]>([]);
  let [targetInfra, setTargetInfra] = useState<IInfraInfo[]>([]);

  const onClickRemoveIcon = useCallback(
    (code: string) => {
      setTargetInfra([
        ...targetInfra,
        ...selectedInfra.filter((item) => item.code === code),
      ]);
      setSelectedInfra(selectedInfra.filter((item) => item.code !== code));
    },
    [selectedInfra]
  );

  const onClickAddIcon = useCallback(
    (code: string) => {
      setSelectedInfra([
        ...selectedInfra,
        ...targetInfra.filter((item) => item.code === code),
      ]);
      setTargetInfra(targetInfra.filter((item) => item.code !== code));
    },
    [targetInfra]
  );

  useEffect(() => {
    if (0 === selectedInfra.length && 0 === targetInfra.length) {
      setTargetInfra(INFRA_INFO_LIST);
    }
  }, [selectedInfra]);

  const navigate = useNavigate();
  const goBack = useCallback(() => {
    navigate("/");
  }, [navigate]);
  return (
    <>
      <div className="justify-center mt-1 ml-1">
        {/* <InfraSelect></InfraSelect> */}
        <h1 className="mb-10 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
          인프라를 선택해주세요
        </h1>

        <div className="flex">
          {targetInfra?.map((item: IInfraInfo, idx: number) => (
            <div>
              <img
                className="w-16 mr-10"
                src={item.icon}
                alt={item.ko}
                onClick={() => onClickAddIcon(item.code)}
              />
              <span>{item.ko}</span>
            </div>
          ))}
        </div>

        <h1 className="text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
          선택하신 인프라 목록입니다.
        </h1>
        <div>{""}</div>
        <div className="flex">
          {selectedInfra?.map((item: IInfraInfo, idx: number) => (
            <div>
              <img
                className="w-16 mr-10"
                src={item.icon}
                alt={item.ko}
                onClick={() => onClickRemoveIcon(item.code)}
              />
              <span>{item.ko}</span>
            </div>
          ))}
        </div>
        <h1 className="mt-10 mb-10 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl dark:text-white">
          구를 선택해주세요.
        </h1>
        {/* <Gu></Gu> */}
        <button
          type="button"
          className="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 font-medium rounded-full text-sm px-5 py-2.5 text-center mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          onClick={goBack}
        >
          제출하기
        </button>
      </div>
    </>
  );
}
