import type { ChangeEvent, ChangeEventHandler } from "react";
import { useState, useCallback } from "react";
import { useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import * as D from "../../data";
import * as U from "../../store/user";

type SignUpFormType = Record<"name" | "password" | "age" | "sex", string>;
const initialFormState = { name: "", password: "", age: "0", sex: "0" };

export default function SignUp() {
  const [{ name, password, age, sex }, setForm] =
    useState<SignUpFormType>(initialFormState);

  const [isCompleteDoubleCheck, setIsCompleteDoubleCheck] =
    useState<boolean>(false);

  const changed = useCallback(
    (key: string) => (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      setForm((obj) => ({ ...obj, [key]: e.target.value }));
    },
    []
  );

  const dispatch = useDispatch();

  const onClickDouble = useCallback(() => {
    if (true === isCompleteDoubleCheck) {
      setIsCompleteDoubleCheck(false);
      return;
    } else if ("" === name) {
      alert("이름을 입력해주세요");
      return;
    }
    D.fetchCheckDoubleName(name).then((data) => setIsCompleteDoubleCheck(data));
  }, [name, isCompleteDoubleCheck]);

  const validCheck = useCallback(() => {
    const numAge = parseInt(age);
    const numSex = parseInt(sex);

    if ("" === name) return "name";
    if ("" === password) return "password";
    if (numAge > 100 || numAge < 16) return "age";
    if (numSex < 0 || numSex >= 3) return "sex";
    if (false === isCompleteDoubleCheck) return "doublecheck";

    return "";
  }, [name, age, sex, password, isCompleteDoubleCheck]);

  // 구가 바뀌었으니 보여줄 매물을 전체 매물로 설정
  const navigate = useNavigate();
  const createAccount = useCallback(() => {
    if ("" !== validCheck()) {
      alert(`입력 정보를 다시 확인해주세요. ${validCheck()}`);
      return;
    }

    D.fetchSignUp({
      name: name,
      user_age: parseInt(age),
      user_sex: parseInt(sex),
      user_type: "Y",
    } as D.IUserSignUp)
      .then((data) => {
        console.log(data);
        dispatch(U.setUserId(1));
      })
      .catch()
      .finally();
    navigate("/infra");
  }, [name, password, age, sex, navigate]);

  return (
    <div className="flex flex-col min-h-screen bg-gray-100 border border-gray-300 shadow-xl rounded-xl">
      <div className="flex flex-col items-center justify-center flex-1 max-w-sm px-2 mx-auto">
        <div className="w-full px-6 py-8 text-black bg-white rounded shadow-md">
          <img className="mb-8 " src="hobbang_banner_outline.png"></img>
          <div className="flex items-center justify-between">
            <input
              type="text"
              className="p-3 mb-4 mr-1 input input-primary"
              name="name"
              placeholder="닉네임"
              value={undefined}
              onChange={changed("name")}
              disabled={isCompleteDoubleCheck}
              autoFocus
            />
            <button
              type="submit"
              className="mb-4 btn btn-primary"
              onClick={onClickDouble}
            >
              {isCompleteDoubleCheck ? "중복 해제" : "중복 확인"}
            </button>
          </div>
          <input
            type="password"
            className="w-full p-3 mb-4 input input-primary"
            name="password"
            placeholder="비밀번호"
            value={undefined}
            onChange={changed("password")}
          />
          <input
            type="text"
            className="w-full p-3 mb-4 input input-primary"
            name="age"
            placeholder="나이"
            value={undefined}
            onChange={changed("age")}
          />
          {/* <input
            type="text"
            className="w-full p-3 mb-4 input input-primary"
            name="sex"
            placeholder="성별"
            value={undefined}
            onChange={changed("sex")}
          /> */}
          <select onChange={changed("sex")} name="sex" className="w-full mb-4">
            <option value="0" className="w-full p-3 mb-2">
              {" "}
              남자
            </option>
            <option value="1" className="w-full p-3 mb-2">
              {" "}
              여자
            </option>
          </select>

          <button
            type="submit"
            className="w-full btn btn-primary"
            onClick={createAccount}
          >
            편의시설 고르러 가기
          </button>
          <p className="mt-3 text-xs text-center text-gray-500">
            &copy;2023 Hobbang Corp. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}
