import { isDisabled } from "@testing-library/user-event/dist/utils";
import React, { useCallback } from "react";
import Select, { ActionMeta, InputActionMeta, MultiValue } from "react-select";
import { INFRA_INFO_LIST } from "../../data/config/infraConfig";
import type { FC, Dispatch, SetStateAction } from "react";

type ISelectOption = {
  value: string;
  label: string;
  isDisabled: boolean;
};

type IInfraInfo = {
  en: string;
  ko: string;
  code: string;
  img: string;
  icon: string;
  emoji: string;
  is_use: boolean;
};
export const convertToSeletOption = (targetList: IInfraInfo[]) => {
  return targetList.map(
    (item: IInfraInfo): ISelectOption => ({
      value: item.code,
      label: item.ko,
      isDisabled: false,
    })
  );
};

type ISelectedInfra = {
  setInfra: Dispatch<SetStateAction<string[]>>;
  selectedInfra: string[];
};

export const InfraSelect: FC<ISelectedInfra> = ({
  setInfra,
  selectedInfra,
}) => {
  //   const [menuIsOpen, setMenuIsOpen] = React.useState<boolean>();
  const optionList = convertToSeletOption(INFRA_INFO_LIST);

  //   const onInputChange = (
  //     inputValue: string,
  //     { action, prevInputValue }: InputActionMeta
  //   ) => {
  //     if (action === "input-change") {
  //       return inputValue;
  //     }
  //     if (action === "menu-close") {
  //       if (prevInputValue) setMenuIsOpen(true);
  //       else setMenuIsOpen(undefined);
  //     }
  //     return prevInputValue;
  //   };

  const onChange = useCallback(
    (inputValue: MultiValue<ISelectOption>, a: ActionMeta<ISelectOption>) => {
      setInfra(
        (inputValue as MultiValue<ISelectOption>).map(
          (item: ISelectOption) => item.value
        )
      );
    },
    []
  );

  return (
    <Select
      className="mb-4 w-80 basic-single"
      isMulti
      defaultValue={undefined}
      isClearable
      isSearchable
      onChange={onChange}
      name="color"
      options={optionList}
      menuIsOpen={true}
      isOptionDisabled={(option) => {
        console.log(selectedInfra);
        return option.isDisabled || selectedInfra.length >= 3;
      }}
    />
  );
};
