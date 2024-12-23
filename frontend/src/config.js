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
  PAGERUN: `${BASE_URL}/page/run/`,
  PAGELIST: `${BASE_URL}/page/list/by-project/`,
  ALLPAGERUN: `${BASE_URL}/page/run/by-project/`,
  SCANLIST: `${BASE_URL}/scan/list/by-page/`,
  GETIMAGE: `${BASE_URL}/image/`,
  MAKESCHEDULE: `${BASE_URL}/schedule/create/by-project/`,
  GETSCHEDULELIST: `${BASE_URL}/schedule/list`,
};
