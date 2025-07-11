import record from "./record.js";
import button from "./button.js";
document.addEventListener("DOMContentLoaded", async () => {
  const btn = document.getElementById("start");
  const exit = document.getElementById("exit");

  if (!btn) {
    console.error("Botão não encontrado");
    return;
  }

  const hasState = await chrome.storage.session.get(["recording"]);
  const lecture = document.getElementById("lecture_link");

  if (hasState.recording === undefined) {
    await chrome.storage.session.set({ recording: false });
  }

  // cuida do estilo condicional do botão ao sofrer load
  await button.handleMeetingInput(btn, lecture);


  btn.addEventListener("click", async () => {
    const [tab] = await record.getTab();
    if (!lecture.value && btn.id === "start") {
      chrome.runtime.sendMessage({
        type: "console",
        message: "ERRO: o link da reunião está vazio.",
      });
      alert("Por favor, insira o Link da reunião");
      return;
    } else {
      if(btn.id === "start"){
        await chrome.storage.session.set({ lectureLink: lecture.value });
        await record.startLecture(tab, lecture.value);
      } 
      else{
        chrome.storage.session.remove(["lectureLink"]);
        chrome.storage.session.remove(["recording"]);
        chrome.storage.session.remove(["shouldMonitor"]);
        chrome.storage.session.set({ regexValidated: false });
      }
      await button.handleMeetingInput(btn, lecture);
    }
  });

  exit?.addEventListener("click", () => {
    chrome.storage.session.clear(() => {
      const error = chrome.runtime.lastError;
      if (error) {
        console.error(error);
      }
      window.location.href = "redirect.html";
    });
  });
});
