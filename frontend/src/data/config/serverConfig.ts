export const setting = {
  backend: {
    protocol: process.env.REACT_APP_PROTOCOL,
    address: process.env.REACT_APP_BACKEND_IP,
    port: process.env.REACT_APP_BACKEND_PORT,
  },
  domain: {
    users: "/users",
    join: "/join", // FT101, FT102
    infra: "/infra", // FT103
    login: "/login", // FT104
    name: "/name", // FT106
    map: "/map",
    items: "/items", // FT201,
    zoom: "/zoom", // FT202
    zzim: "/zzim",
    register: "/register", // FT302
    unregister: "/unregister", // FT303
    click: "/click", // FT401, FT402
    recommend: "/recommend",
  },
  basic_option: {
    // need to add proper method and body or data in each function
    method: "",
    mode: "cors" as RequestMode,
    cache: "no-cache" as RequestCache,
    credentials: "same-origin" as RequestCredentials,
    headers: {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
    },
    body: JSON.stringify({}),
  },
};

export const BACKEND_ADDRESS = `${setting["backend"]["protocol"]}${setting["backend"]["address"]}:${setting["backend"]["port"]}`;
export const DOMAIN_INFO = setting["domain"];
export let FETCH_BASIC_OPTION = setting["basic_option"];
