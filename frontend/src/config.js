const BASE_URL = "http://localhost:8080";

export const API = {
  LOGIN: `${BASE_URL}/auth/login`,
  LOGOUT: `${BASE_URL}/auth/logout`,
  SIGNUP: `${BASE_URL}/auth/signup`,
  PROJECTLIST: `${BASE_URL}/project/list`,
  PROJECTCREATE: `${BASE_URL}/project/create`,
  PROJECTDELETE: `${BASE_URL}/project/delete`,
  PROJECTUPDATE: `${BASE_URL}/project/update`,
  PAGECREATE: `${BASE_URL}/page/create/by-project/`,
  PAGEDELETE: `${BASE_URL}/page/delete`,
  PAGELIST: `${BASE_URL}/page/list/by-project/`,
  REQUESTCREATE: `${BASE_URL}/request/create/by-page/`,
};
