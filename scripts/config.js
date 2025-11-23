const ENV = 'DSV'

const BASE_URLS = {
  DSV: "http://localhost:8183",
  PRD: "https://espeon.onrender.com"
};
export const CONFIG = {
  ENV: ENV,
  API_BASE_URL: BASE_URLS[ENV],
  API_ENDPOINT: "/traces",
  USERS_ENDPOINT: "/users",
  LOGIN_ENDPOINT: "/login/token",
  LECTURES_ENDPOINT: "/lectures",
  SUBJECTS_ENDPOINT: "/subjects",
  REPORTS_ENDPOINT: "/reports"
};