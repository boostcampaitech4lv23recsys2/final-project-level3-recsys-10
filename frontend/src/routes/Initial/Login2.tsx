import type { ChangeEvent, ChangeEventHandler } from "react";
import { useState, useCallback } from "react";
import { useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import * as D from "../../data";
import * as U from "../../store/user";
import { genSaltSync, hashSync } from "bcrypt-ts";

type SignUpFormType = Record<"name" | "password", string>;
const initialFormState = { name: "", password: "" };

export const hashPasswordP = (password: string): Promise<string> => {
  return new Promise<string>(async (resolve, reject) => {
    try {
      // const salt = await bcrypt.genSalt();
      // const hash = await bcrypt.hash(password, salt);
      const salt = genSaltSync(12);
      const hash = hashSync(encodeURI(password), salt);
      console.log(hash);
      resolve(hash);
    } catch (e) {
      reject(e);
    }
  });
};

export default function Login2() {
  const [{ name, password }, setForm] =
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
  const navigate = useNavigate();

  // const onClickDouble = useCallback(() => {
  //   if (true === isCompleteDoubleCheck) {
  //     setIsCompleteDoubleCheck(false);
  //     return;
  //   } else if ("" === name) {
  //     alert("이름을 입력해주세요");
  //     return;
  //   }
  //   D.fetchCheckDoubleName(name).then((data) => setIsCompleteDoubleCheck(data));
  // }, [name, isCompleteDoubleCheck]);

  const validCheck = useCallback(() => {
    if ("" === name || undefined === name) return "name";
    if ("" === password || undefined === password) return "password";

    hashPasswordP(password).then((hashed) => {
      D.fetchLogin({ name, pw: password }).then(
        ({ user_id, user_gu, infra_list, code }) => {
          dispatch(
            U.setUserInfo({
              userId: user_id,
              userGu: user_gu,
              infraList: infra_list as string[],
            })
          );
          if (code === false) {
            alert("로그인에 실패했습니다. ");
            navigate("/login");
          } else if (user_gu === "") {
            navigate("/infra");
          } else {
            navigate("/");
          }
        }
      );
    });

    return "";
  }, [name, , password]);

  // 구가 바뀌었으니 보여줄 매물을 전체 매물로 설정

  return (
    <div className="flex flex-col min-h-screen bg-gray-100 border border-gray-300 shadow-xl rounded-xl">
      <div className="flex flex-col items-center justify-center flex-1 max-w-sm px-2 mx-auto">
        <div className="w-full px-6 py-8 text-black bg-white rounded shadow-md">
          <img className="mb-8 " src="hobbang_banner_outline.png"></img>
          <input
            type="text"
            className="w-full p-3 mb-4 input input-primary"
            name="name"
            placeholder="닉네임"
            defaultValue={undefined}
            onChange={changed("name")}
            disabled={isCompleteDoubleCheck}
            autoFocus
          />
          <input
            type="password"
            className="w-full p-3 mb-4 input input-primary"
            name="password"
            placeholder="비밀번호"
            defaultValue={undefined}
            onChange={changed("password")}
          />
          <div className="flex items-center justify-between">
            <button
              className="px-4 py-2 font-bold text-white bg-[#ffc600] rounded hover:bg-blue-700 focus:outline-none focus:shadow-outline"
              type="submit"
              onClick={validCheck}
            >
              로그인
            </button>
            <a
              className="inline-block text-sm font-bold text-[#ffc600] align-baseline hover:text-[#ffc600]"
              href="#"
              onClick={() => navigate("/signup")}
            >
              회원가입
            </a>
            {/* <a
              className="inline-block text-sm font-bold text-blue-500 align-baseline hover:text-blue-800"
              href="#"
            >
              둘러보기
            </a> */}
          </div>
          <p className="mt-3 text-xs text-center text-gray-500">
            &copy;2023 Hobbang Corp. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
}
