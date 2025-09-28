import { logout } from "./auth/logout.js";

document.addEventListener("DOMContentLoaded", async () => {
  const exit = document.getElementById("exit_style");
  const profile = document.getElementById("profile");

  const result = await chrome.storage.session.get("user");

  const username = result.user;

  const alias = username ? username.split("@")[0] : "Dummy";

  if (profile) {
    profile.textContent = alias;
  }

  logout(exit);
});
