document.addEventListener("DOMContentLoaded", () => {
  const viewBtn = document.getElementById("view_reports");
  const emitBtn = document.getElementById("emit_reports");
  const backBtn = document.getElementById("back");

  if (viewBtn) {
    viewBtn.addEventListener("click", async () => {
      await chrome.storage.session.set({ currentPage: "reports_list.html" });
      window.location.href = "reports_list.html";
    });
  }

  if (emitBtn) {
    emitBtn.addEventListener("click", async () => {
      await chrome.storage.session.set({ currentPage: "reports_post.html" });
      window.location.href = "reports_post.html";
    });
  }

  if (backBtn) {
    backBtn.addEventListener("click", async () => {
      await chrome.storage.session.set({ currentPage: "teacher.html" });
      window.location.href = "teacher.html";
    });
  }
});
