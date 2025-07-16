import { fillTeacher,fillSubjects } from "./lecture/fields.js";
import { logout } from "./auth/logout.js";
import { submitLecture } from "./lecture/lecture_submission.js";


document.addEventListener("DOMContentLoaded", () => {
  const exit = document.getElementById("exit");
  const form = document.getElementById("form_lecture");
  const selector = document.getElementById("subject");
  fillTeacher();
  fillSubjects(selector);
  logout(exit);
  // é um listener que aguarda o clique para efetuar o logout
  submitLecture(form);
});
