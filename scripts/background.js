import api from "./api.js";
import record from "./record.js";
import { CONFIG } from "./config.js";
import button from "./button.js";

chrome.storage.session.set({ regexValidated: false });
let lastValidatedTitle = "";

async function shouldRecord() {
  const { recording } = await chrome.storage.session.get("recording");
  return recording;
}

function normalizeTeamsTitle(title) {
  // Remove o sufixo " | Microsoft Teams"
  title = title.replace(/\s*\|\s*Microsoft Teams\s*$/i, "");

  // Divide pelos pipes e pega o último item não vazio
  const parts = title.split("|").map(p => p.trim()).filter(Boolean);
  return parts.length > 0 ? parts[parts.length - 1] : title;
}


async function validateTitle(tab) {
  let regexValidated = await chrome.storage.session.get("regexValidated");
  let meeting = await chrome.storage.session.get(["lectureLink"]);

  if (
    !tab.title ||
    tab.title === lastValidatedTitle ||
    regexValidated.regexValidated ||
    (meeting && Object.keys(meeting).length === 0)
  ) {
    return;
  }

  console.log("[validateTitle] tab.title =", tab.title);
  lastValidatedTitle = tab.title;

  const normalizedTitle = normalizeTeamsTitle(tab.title);
  console.log("[validateTitle] normalizedTitle =", normalizedTitle);

  const isValid = record.isTitleValid(normalizedTitle);
  console.log("VALIDAÇÃO REGEX =>", isValid);

  if (isValid && regexValidated.regexValidated === false) {
    await chrome.storage.session.set({ regexValidated: true });
    await chrome.storage.session.set({ shouldMonitor: true });
    await chrome.storage.session.set({ entrypoint: tab.id });
    console.log("Regex válida, ativando monitoramento");
    await chrome.storage.session.set({ recording: true });
    console.log("GRAVAÇÃO INICIADA");
  }
}


chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.type === "click_event") {
    console.log("Click event captured in current webpage");
  } else if (request.type === "console") {
    console.log(request.message);
  } else if (request.type === "tabData") {
    api.callAPI(
      "POST",
      `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
      request.payload
    );
  }
});

chrome.tabs.onActivated.addListener(async (activeInfo) => {
  //busca tab e valida REGEX
  console.log("[onActivate] VALIDANDO REGEX");
  const tab = await chrome.tabs.get(activeInfo.tabId);
  await validateTitle(tab);

  // verifica se prossegue com base na validação anterior
  let flagMonitor = await chrome.storage.session.get(["shouldMonitor"]);
  if (!flagMonitor) return;

  if (!(await shouldRecord())) return;

  const lecture = await chrome.storage.session.get(["lectureLink"]);
  const expectedTab = await chrome.storage.session.get(["entrypoint"]);
  const lectureTab = await chrome.tabs.get(expectedTab.entrypoint);
  const student = await record.retrieveUser();
  console.log("[TAB.ID] = ", tab.id);
  console.log("[ENTYPOINT.ID] = ", expectedTab);

  if (tab.id !== expectedTab.entrypoint) {
    console.log(`[onActivated] ${student} left Microsoft Teams tab`);

    const payload = record.buildPayload(
      lectureTab,
      tab,
      lecture.lectureLink,
      "onActivated",
      student
    );

    api.callAPI(
      "POST",
      `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
      payload
    );
  }
});

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete") {
    console.log("[onUpdated] VALIDANDO REGEX");
    // valida REGEX
    await validateTitle(tab);

    // verifica se prossegue
    let flagMonitor = await chrome.storage.session.get(["shouldMonitor"]);
    if (!flagMonitor) return;
    if (!(await shouldRecord())) return;

    const lecture = await chrome.storage.session.get(["lectureLink"]);
    const expectedTab = await chrome.storage.session.get(["entrypoint"]);
    const lectureTab = await chrome.tabs.get(expectedTab.entrypoint);
    const student = await record.retrieveUser();

    console.log("[TAB.ID] = ", tab.id);
    console.log("[ENTYPOINT.ID] = ", expectedTab);

    if (tab.id !== expectedTab.entrypoint) {
      console.log(`[onUpdated] ${student} left Microsoft Teams tab`);

      const payload = record.buildPayload(
        lectureTab,
        tab,
        lecture.lectureLink,
        "onActivated",
        student
      );

      api.callAPI(
        "POST",
        `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
        payload
      );
    }
  }
});
