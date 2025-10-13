import { fillTeacher, fillSubjects } from "./lecture/fields.js";
import { logout } from "./auth/logout.js";
import { submitLecture } from "./lecture/lecture_submission.js";

document.addEventListener("DOMContentLoaded", async () => {
  const exit = document.getElementById("exit");
  const form = document.getElementById("form_lecture");
  const selector = document.getElementById("subject");
  const back = document.getElementById("back");

  // armazena o estado atual da página
  const currentPage = await chrome.storage.session.get("currentPage");

  fillTeacher();
  fillSubjects(selector);
  logout(exit);

  // é um listener que aguarda o clique para efetuar o logout
  submitLecture(form);

  if (back) {
    back.addEventListener("click", async () => {
      await chrome.storage.session.remove("currentPage");
      // volta para redirect.html, que fará o roteamento
      window.location.href = "redirect.html";
    });
  }
});
