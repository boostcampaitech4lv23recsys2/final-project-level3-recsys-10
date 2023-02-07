import type { ChangeEvent, ChangeEventHandler } from "react";
import { useState, useCallback } from "react";
import { useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import * as D from "../../data";
import * as U from "../../store/user";
import { genSaltSync, hashSync } from "bcrypt-ts";

type SignUpFormType = Record<"name" | "password" | "age" | "sex", string>;
const initialFormState = { name: "", password: "", age: "0", sex: "0" };

// export const hashPasswordP = (password: string): Promise<string> => {
//   return new Promise<string>(async (resolve, reject) => {
//     try {
//       // const salt = await bcrypt.genSalt();
//       // const hash = await bcrypt.hash(password, salt);
//       const salt = genSaltSync(12);
//       const hash = hashSync(encodeURI(password), salt);
//       console.log(hash);
//       resolve(hash);
//     } catch (e) {
//       reject(e);
//     }
//   });
// };

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
    D.fetchCheckDoubleName(name).then((data) => {
      if (data === false) {
        alert("중복된 이름이 있습니다. ");
      }
      setIsCompleteDoubleCheck(data);
    });
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

    const salt = genSaltSync(12);
    const hash = hashSync(encodeURI(password), salt);

    D.fetchSignUp({
      name: name,
      pw: hash,
      user_age: parseInt(age),
      user_sex: parseInt(sex),
      user_type: "Y",
    } as D.IUserSignUp)
      .then((data) => {
        dispatch(U.setUserId(data));
        navigate("/infra");
      })
      .catch()
      .finally();
  }, [name, password, age, sex, navigate, isCompleteDoubleCheck]);

  return (
    <div className="flex flex-col min-h-screen bg-gray-100 border border-gray-300 shadow-xl rounded-xl">
      <div className="flex flex-col items-center justify-center flex-1 max-w-sm px-2 mx-auto">
        <div className="w-full px-6 py-8 text-black bg-white rounded shadow-md">
          <img className="mb-8 " src="hobbang_banner_outline.png"></img>
          <div className="flex items-center justify-between">
            <input
              type="text"
              className="p-3 mb-4 mr-1 input outline outline-[#ffc600] rounded-lg bg-white"
              name="name"
              placeholder="닉네임"
              defaultValue={undefined}
              onChange={changed("name")}
              disabled={isCompleteDoubleCheck}
              autoFocus
            />
            <button
              type="submit"
              className="mb-4 btn bg-[#ffc600]  hover:bg-[#F7BE38]/90 "
              onClick={onClickDouble}
            >
              {isCompleteDoubleCheck ? "확인 해제" : "중복 확인"}
            </button>
          </div>
          <input
            type="password"
            className="w-full p-3 mb-4 input  outline outline-[#ffc600] rounded-lg bg-white"
            name="password"
            placeholder="비밀번호"
            defaultValue={undefined}
            onChange={changed("password")}
          />
          <input
            type="text"
            className="w-full p-3 mb-4 input outline outline-[#ffc600] rounded-lg bg-white"
            name="age"
            placeholder="나이"
            defaultValue={undefined}
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
          <select
            onChange={changed("sex")}
            name="sex"
            className="w-full mb-4 input  outline outline-[#ffc600] rounded-lg bg-white"
          >
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
            className="w-full btn bg-[#ffc600]  hover:bg-[#F7BE38]/90 "
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
