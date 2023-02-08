import { INFRA_INFO_DICT } from "../data/config/infraConfig";

const getFeeStr = (fee: number): string => {
  let remainder = fee % 10000;
  let quotient = Math.floor(fee / 10000);
  let res = `${quotient}억 ${remainder}`;
  res = 0 === quotient ? res.slice(3) : res;
  res = 0 === remainder ? res.slice(0, res.length - 1) : res;
  return res;
};

const getSalesTypeStr = (rentFee: number): string => {
  return 0 == rentFee ? "전세" : "월세";
};

const getWholeFeeStr = (
  salesStr: string,
  feeStr: string,
  rentFee: number
): string => {
  let res = `${salesStr} ${feeStr}`;

  if (0 !== rentFee) {
    res = `${res} / ${rentFee}`;
  }

  return res;
};

export const makeFeeStr = (houseInfo: any): string => {
  const curFeeStr = getFeeStr(houseInfo["information"]["price_deposit"]);
  const curSalesType = getSalesTypeStr(
    houseInfo["information"]["price_monthly_rent"]
  );
  const wholeFee = getWholeFeeStr(
    curSalesType,
    curFeeStr,
    houseInfo["information"]["price_monthly_rent"]
  );

  return wholeFee;
};

type IInfraDetailInfo = {
  cnt: number;
  distance: number;
  lat: number;
  lng: number;
};

export type IInfraInfo = {
  "01": IInfraDetailInfo;
  "02": IInfraDetailInfo;
  "03": IInfraDetailInfo;
  "04": IInfraDetailInfo;
  "05": IInfraDetailInfo;
  "06": IInfraDetailInfo;
  "07": IInfraDetailInfo;
  "08": IInfraDetailInfo;
};

// export const makeInfraHtml = (infraInfo: any): string => {
export const makeInfraHtml = (infraInfo: IInfraInfo): string => {
  return Object.keys(infraInfo)
    .map((infra: string) => {
      const curDist = Math.round(
        infraInfo[infra as keyof IInfraInfo]["distance"] * 100
      );
      return `${
        INFRA_INFO_DICT[infra as keyof IInfraInfo]["emoji"]
      } : ${curDist}m`;
    })
    .join(", ");
};
