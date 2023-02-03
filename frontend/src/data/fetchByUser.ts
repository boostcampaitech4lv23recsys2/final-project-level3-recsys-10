// User 정보를 활용하여 data 를 가져오는 함수 구현
import { request } from "http";
import { URLSearchParams } from "url";
import {
  BACKEND_ADDRESS,
  DOMAIN_INFO,
  FETCH_BASIC_OPTION,
} from "./config/serverConfig";

export type IUser = {
  user_id: number;
  user_gu: string;
  infra_list: string[] | null;
};

export type IUserSignUp = {
  name: string;
  pw: string;
  user_age: number | null;
  user_sex: number | null;
  user_type: string;
  register_date: Date | null;
  update_date: Date | null;
};

// user_id 와 user_gu 정보로 해당 gu 에서 hosue information 을 받아오는 함수
export const fetchHouseByGu = ({
  userId,
  userGu,
}: {
  userId: number;
  userGu: string;
}): Promise<any> =>
  new Promise((resolve, reject) => {
    let requestOption = FETCH_BASIC_OPTION;
    requestOption["method"] = "POST";
    requestOption["body"] = JSON.stringify({
      user_id: userId,
      user_gu: userGu,
      house_ranking: {},
    });
    fetch(
      `${BACKEND_ADDRESS}${DOMAIN_INFO["map"]}${DOMAIN_INFO["items"]}`,
      requestOption
    )
      // fetch("http://27.96.130.120:30007/users/login")
      .then((res) => res.json())
      .then((data: any) => {
        // console.log(data);
        const { houses } = data as { houses: any };
        resolve(houses);
      })
      .catch(reject);
  });

// 현재 화면에서 매물정보를 불러오는 함수
export const fetchHouseByCoord = ({
  user_id,
  user_gu,
  min_lat,
  min_lng,
  max_lat,
  max_lng,
}: {
  user_id: number;
  user_gu: string;
  min_lat: number;
  min_lng: number;
  max_lat: number;
  max_lng: number;
}): Promise<any> =>
  new Promise((resolve, reject) => {
    let requestOption: RequestInit = FETCH_BASIC_OPTION;
    requestOption["method"] = "POST";
    requestOption["body"] = JSON.stringify({
      user_id,
      user_gu,
      house_ranking: {},
      min_lat,
      min_lng,
      max_lat,
      max_lng,
    });
    console.log(requestOption);
    console.log(
      `${BACKEND_ADDRESS}${DOMAIN_INFO["map"]}${DOMAIN_INFO["items"]}${DOMAIN_INFO["zoom"]}`
    );
    fetch("http://27.96.130.120:30007/map/items/zoom", requestOption)
      // fetch("http://27.96.130.120:30007/users/login")
      .then((res) => res.json())
      .then((data: unknown) => {
        console.log(data);
        const { houses } = data as { houses: unknown };
        resolve(houses);
      })
      .catch(reject);
  });

// 클릭 로그를 기록하는 함수
export const fetchAddClickLog = ({
  user_id,
  house_id,
  log_type,
}: {
  user_id: number;
  house_id: number;
  log_type: string;
}): Promise<boolean> =>
  new Promise((resolve, reject) => {
    let requestOption = FETCH_BASIC_OPTION;
    requestOption["method"] = "POST";
    requestOption["body"] = JSON.stringify({
      user_id,
      house_id,
      log_type,
    });
    fetch(
      `${BACKEND_ADDRESS}${DOMAIN_INFO["map"]}${DOMAIN_INFO["items"]}${DOMAIN_INFO["click"]}`,
      requestOption
    )
      // fetch("http://27.96.130.120:30007/users/login")
      .then((res) => res.json())
      .then((data: unknown) => {
        console.log(data);
        resolve(true);
      })
      .catch(reject);
  });

// 회원가입 함수
export const fetchSignUp = (signUpInfo: IUserSignUp): Promise<boolean> =>
  new Promise((resolve, reject) => {
    let requestOption = FETCH_BASIC_OPTION;
    requestOption["method"] = "POST";
    requestOption["body"] = JSON.stringify(signUpInfo);
    fetch(`${BACKEND_ADDRESS}${DOMAIN_INFO["users"]}${DOMAIN_INFO["join"]}`)
      // fetch("http://27.96.130.120:30007/users/login")
      .then((res) => res.json())
      .then((data: unknown) => {
        console.log(data);
        resolve(true); // TODO 수정 필요
      })
      .catch(reject);
  });

// // 닉네임 중복 확인 함수
// export const fetchCheckDoubleName = (name: string): Promise<boolean> =>
//   new Promise((resolve, reject) => {
//     let requestOption = FETCH_BASIC_OPTION;
//     requestOption["method"] = "GET";
//     fetch(
//       `${BACKEND_ADDRESS}${DOMAIN_INFO["map"]}${DOMAIN_INFO["items"]}${DOMAIN_INFO["click"]}` +
//         new URLSearchParams({ name })
//     )
//       // fetch("http://27.96.130.120:30007/users/login")
//       .then((res) => res.json())
//       .then((data: unknown) => {
//         console.log(data);
//         resolve(true); // TODO 수정 필요
//       })
//       .catch(reject);
//   });

// name 과 pw 를 이용하여 login 요청
// TODO pw 는 암호화되어 있어야 함
export const fetchLogin = ({
  name,
  pw,
}: {
  name: string;
  pw: string;
}): Promise<IUser> =>
  new Promise((resolve, reject) => {
    let requestOption = FETCH_BASIC_OPTION;
    requestOption["method"] = "POST";
    requestOption["body"] = JSON.stringify({ name, pw });
    fetch(
      `${BACKEND_ADDRESS}${DOMAIN_INFO["users"]}${DOMAIN_INFO["login"]}`,
      requestOption
    )
      // fetch("http://27.96.130.120:30007/users/login")
      .then((res) => res.json())
      .then((data: unknown) => {
        console.log(data);
        const { user_id, user_gu, infra_list } = data as IUser;
        resolve({ user_id, user_gu, infra_list });
      })
      .catch(reject);
  });

// Backend Server에 user 가 선택한 infra 정보 전달
export const fetchAddInfra = ({
  user_id,
  user_type,
  user_gu,
  infra_list,
}: {
  user_id: number;
  user_type: string;
  user_gu: string;
  infra_list: string[];
}): Promise<unknown> =>
  new Promise((resolve, reject) => {
    let requestOption = FETCH_BASIC_OPTION;
    requestOption["method"] = "POST";
    requestOption["body"] = JSON.stringify({
      user_id,
      user_type,
      user_gu,
      infra: infra_list,
      resister_time: new Date(),
    });
    fetch(
      `${BACKEND_ADDRESS}${DOMAIN_INFO["users"]}${DOMAIN_INFO["infra"]}`,
      requestOption
    )
      // fetch("http://27.96.130.120:30007/users/login")
      .then((res) => res.json())
      .then((data: unknown) => {
        console.log(data);
        resolve(true);
      })
      .catch(reject);
  });

// User 의 zzim 목록을 전달 받는 함수
export const fetchHouseByZzim = ({
  user_id,
  user_gu,
}: {
  user_id: number;
  user_gu: string;
}): Promise<unknown> =>
  new Promise((resolve, reject) => {
    let requestOption = FETCH_BASIC_OPTION;
    requestOption["method"] = "POST";
    requestOption["body"] = JSON.stringify({
      user_id,
      user_gu,
      house_ranking: {},
    });
    fetch(
      `${BACKEND_ADDRESS}${DOMAIN_INFO["zzim"]}${DOMAIN_INFO["items"]}`,
      requestOption
    )
      // fetch("http://27.96.130.120:30007/users/login")
      .then((res) => res.json())
      .then((data: unknown) => {
        console.log(data);
        const { houses } = data as { houses: unknown };
        resolve(houses);
      })
      .catch(reject);
  });

// User 의 zzim 목록을 전달 받는 함수
export const fetchZzimRegister = ({
  user_id,
  house_id,
  zzim_yn,
}: {
  user_id: number;
  house_id: number;
  zzim_yn: string;
}): Promise<boolean> =>
  new Promise((resolve, reject) => {
    let requestOption = FETCH_BASIC_OPTION;
    requestOption["method"] = "POST";
    requestOption["body"] = JSON.stringify({
      user_id,
      house_id,
      zzim_yn,
    });
    fetch(
      `${BACKEND_ADDRESS}${DOMAIN_INFO["zzim"]}${DOMAIN_INFO["items"]}${DOMAIN_INFO["register"]}`,
      requestOption
    )
      // fetch("http://27.96.130.120:30007/users/login")
      .then((res) => res.json())
      .then((data: unknown) => {
        console.log(data);
        resolve(true);
      })
      .catch(reject);
  });
