import React, { useCallback, useState } from "react";
import type { FC, Dispatch, SetStateAction } from "react";

import Select, { SingleValue, ActionMeta } from "react-select";
import { GU_INFO } from "../../data/config/guConfig";

import * as U from "../../store/user";
import { useSelector } from "react-redux";
import { AppState } from "../../store";

export interface ISelectOption {
  readonly value: string;
  readonly label: string;
}

export const convertToSeletOption = (targetList: string[]) => {
  return targetList.map(
    (item: string): ISelectOption => ({ value: item, label: item })
  );
};

const optionList = convertToSeletOption(GU_INFO);

export const Gu: FC<{
  setGu: Dispatch<SetStateAction<string>>;
  className: string | undefined;
}> = ({ setGu, className }) => {
  const [isClearable, setIsClearable] = useState(true);
  const [isSearchable, setIsSearchable] = useState(true);
  const [isDisabled, setIsDisabled] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isRtl, setIsRtl] = useState(false);

  const { userId, userGu } = useSelector<AppState, U.State>(
    (state) => state.user
  );

  const guIdx = GU_INFO.indexOf(userGu);

  const onInputChange = useCallback(
    (inputValue: SingleValue<ISelectOption>, a: ActionMeta<ISelectOption>) => {
      const retValue =
        (inputValue as ISelectOption).value.length > 5
          ? ""
          : (inputValue as ISelectOption).value;
      setGu(retValue);
    },
    []
  );

  return (
    <Select
      className={className}
      classNamePrefix="select"
      defaultValue={optionList[guIdx]}
      isDisabled={isDisabled}
      isLoading={isLoading}
      isRtl={isRtl}
      onChange={onInputChange}
      isSearchable={isSearchable}
      options={optionList}
    />
  );
};
