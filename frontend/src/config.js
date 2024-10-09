const BASE_URL = "http://localhost:8080";

export const API = {
  LOGIN: `${BASE_URL}/auth/login`,
  LOGOUT: `${BASE_URL}/auth/logout`,
  SIGNUP: `${BASE_URL}/auth/signup`,
  PROJECTLIST: `${BASE_URL}/project/list`,
  PROJECT_PAGE_CREATE: `${BASE_URL}/project-page/create`,
  PROJECTDELETE: `${BASE_URL}/project/delete`,
  PROJECTUPDATE: `${BASE_URL}/project/update`,
  PAGECREATE: `${BASE_URL}/page/create/by-project/`,
  PAGEDELETE: `${BASE_URL}/page/delete`,
  PAGEUPDATE: `${BASE_URL}/page/update`,
  PAGELIST: `${BASE_URL}/page/list/by-project/`,
};
