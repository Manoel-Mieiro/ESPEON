import { logout } from "./auth/logout.js";

document.addEventListener("DOMContentLoaded", () => {
  const exit = document.getElementById("exit_style");
  logout(exit);
});
