import { useCallback, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Dropdwon() {
  const [openMenu, setOpenMenu] = useState<boolean>(false);

  const onClickOpen = () => setOpenMenu(!openMenu);
  const navigate = useNavigate();
  const goBack = useCallback(() => {
    navigate(-1);
  }, [navigate]);
  return (
    <div className="flex justify-center h-screen ml-80">
      <div className="relative my-32">
        <button
          className="relative z-10 block p-2 bg-white rounded-md focus:outline-none"
          onClick={onClickOpen}
        >
          <svg
            className="w-5 h-5 text-gray-800"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </svg>
        </button>

        {openMenu && (
          <div className="absolute left-0 z-20 w-48 py-2 mt-2 bg-white rounded-md shadow-xl">
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
            >
              your profile
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
            >
              Your projects
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
            >
              Help
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
            >
              Settings
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-sm text-gray-700 capitalize hover:bg-blue-500 hover:text-white"
            >
              Sign Out
            </a>
            <a>
              <input
                type="range"
                min="0"
                max="100"
                value="40"
                className="multi-range"
              />
            </a>
          </div>
        )}
      </div>
    </div>
  );
}
