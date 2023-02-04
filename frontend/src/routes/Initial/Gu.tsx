import React, { useCallback, useState } from "react";
import type { FC, Dispatch, SetStateAction } from "react";

import Select, { SingleValue, ActionMeta } from "react-select";
import { GU_INFO } from "../../data/config/guConfig";

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

  const onInputChange = useCallback(
    (inputValue: SingleValue<ISelectOption>, a: ActionMeta<ISelectOption>) => {
      setGu((inputValue as ISelectOption).value);
    },
    []
  );

  return (
    <Select
      className={className}
      classNamePrefix="select"
      defaultValue={optionList[0]}
      isDisabled={isDisabled}
      isLoading={isLoading}
      isClearable={isClearable}
      isRtl={isRtl}
      onChange={onInputChange}
      isSearchable={isSearchable}
      options={optionList}
    />
  );
};
