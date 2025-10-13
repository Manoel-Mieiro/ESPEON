import { logout } from "./auth/logout.js";

document.addEventListener("DOMContentLoaded", async () => {
  const exit = document.getElementById("exit_style");
  const profile = document.getElementById("profile");

  const navMap = {
    lectures_nav: "lecture.html",
    reports_nav: "lecture.html",
  };

  // Resolução de nome
  const result = await chrome.storage.session.get("user");
  const username = result.user;
  const alias = username ? username.split("@")[0] : "Dummy";

  if (profile) {
    profile.textContent = alias;
  }

  // Listners para menus de navegação
  for (const [id, url] of Object.entries(navMap)) {
    const item = document.getElementById(id);
    if (item) {
      item.addEventListener("click", async () => {
        // salva no storage a página de destino
        await chrome.storage.session.set({ currentPage: url });
        window.location.href = url;
      });
    }
  }

  // logout
  logout(exit);
});
