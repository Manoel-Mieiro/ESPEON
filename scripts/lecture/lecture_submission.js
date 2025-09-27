import api from "../api.js";
import { CONFIG } from "../config.js";
import { initClipboardCopyListener } from "./clipboard.js";
import { getFormData } from "./fields.js";
import { handleView, restoreView, triggerViewHandling } from "./handle.view.js";
import { fillWithTitle } from "./lecture_title.js";

let clipboardData;
let lectureField;
let backBtn;

export async function submitLecture(component) {
  component.addEventListener("submit", async (event) => {
    event.preventDefault();

    const lectureField = document.getElementById("lecture_content");
    const backBtn = document.getElementById("back_lecture");

    const clipboardData = getFormData();

    try {
      // Converte o email do docente em UUID
      const teacherUUID = await getTeacherIdByEmail(clipboardData.teacher_id);
      clipboardData.teacher_id = teacherUUID;

      chrome.storage.session.set({ lecture: clipboardData });

      // Envia para a API
      const response = await api.callAPI(
        "POST",
        `${CONFIG.API_BASE_URL}${CONFIG.LECTURES_ENDPOINT}`,
        clipboardData
      );

      // Atualiza a view
      handleView(clipboardData);
      await fillWithTitle(clipboardData, lectureField);
      triggerViewHandling(backBtn);

      chrome.runtime.sendMessage({
        type: "console",
        message: `Aula enviada com sucesso: ${JSON.stringify(clipboardData)}`,
      });
    } catch (error) {
      chrome.runtime.sendMessage({
        type: "console",
        message: `Aula não pode ser criada: \n${error}`,
      });
      alert(`Falha ao criar aula`);
    }
  });
}

async function getTeacherIdByEmail(email) {
  try {
    const response = await api.callAPI(
      "GET",
      `${CONFIG.API_BASE_URL}/users/${email}`
    );
    if (!response) throw new Error("Professor não encontrado");
    return response.user_id;
  } catch (error) {
    chrome.runtime.sendMessage({
      type: "console",
      message: `[getTeacherIdByEmail] Falha: ${error}`,
    });
    throw error;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initClipboardCopyListener();
  chrome.storage.session.get(["lecture"], (result) => {
    if (result.lecture) {
      clipboardData = result.lecture;
      console.log(`clipboardData: ${result.lecture}`)
      lectureField = document.getElementById("lecture_content");
      backBtn = document.getElementById("back_lecture");

      restoreView();
      fillWithTitle(clipboardData, lectureField);
      triggerViewHandling(backBtn);

      chrome.runtime.sendMessage({
        type: "console",
        message: `DOMContentLoaded: ${clipboardData}`,
      });
    } else {
      chrome.runtime.sendMessage({
        type: "console",
        message: `DOMContentLoaded: Had no content`,
      });
    }
  });
});
