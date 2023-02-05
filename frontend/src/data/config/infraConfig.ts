// 230117 backend {'subway':'01','cs':'02','mart':'03','park':'04','cafe':'05','phar':'06','theater':'07'}
export const setting = {
  infra: {
    "01": {
      en: "subway",
      ko: "지하철",
      code: "01",
      img: "",
      icon: "subway_hobbang.png",
      emoji: "🚊",
      is_use: true,
    },
    "02": {
      en: "convenience store",
      ko: "편의점",
      code: "02",
      img: "",
      icon: "store_hobbang.png",
      emoji: "🍱",
      is_use: true,
    },
    "03": {
      en: "mart",
      ko: "대형마트",
      code: "03",
      img: "",
      icon: "shopping-cart",
      emoji: "🛍",
      is_use: true,
    },
    "04": {
      en: "park",
      ko: "공원",
      code: "04",
      img: "",
      icon: "futbol-o",
      emoji: "🐶",
      is_use: false,
    },
    "05": {
      en: "cafe",
      ko: "카페",
      code: "05",
      img: "",
      icon: "coffee",
      emoji: "🍩",
      is_use: true,
    },
    "06": {
      en: "pharmacy",
      ko: "약국",
      code: "06",
      img: "",
      icon: "ambulance",
      emoji: "💊",
      is_use: true,
    },
    "07": {
      en: "theater",
      ko: "영화관",
      code: "07",
      img: "",
      icon: "movie_hobbang.png",
      emoji: "🎬",
      is_use: true,
    },
    "08": {
      en: "gym",
      ko: "헬스장",
      code: "08",
      img: "",
      icon: "health_hobbang.png",
      emoji: "💪",
      is_use: true,
    },
  },
};

// export const INFRA_INFO = list(filter(lambda infra: infra["is_use"] == True,[*setting["infra"].values()]))
export const INFRA_INFO_LIST = Object.values(setting["infra"]).filter(
  (infra) => infra.is_use === true
);

export const INFRA_INFO_DICT = setting["infra"];
