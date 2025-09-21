import getFromStorage from "../storage.js";
import api from "../api.js";
import { CONFIG } from "../config.js";

export function submitToken(component, document) {
  component.addEventListener("submit", async (event) => {
    event.preventDefault();
    const email = await getFromStorage("user");
    const token = document.getElementById("tokenValue").value;

    try {
      const response = await api.callAPI(
        "GET",
        `${CONFIG.API_BASE_URL}${CONFIG.LOGIN_ENDPOINT}?email=${email}&token=${token}`
      );
      handleResponse(response, email);
    } catch (error) {
      chrome.runtime.sendMessage({
        type: "console",
        message: `Token/usuário informado incorreto(s): \n${error}`,
      });
      alert("Token Inválido");
    }
  });
}

function handleResponse(response, user) {
  if (response) {
    chrome.runtime.sendMessage({
      type: "console",
      message: `${user} acessou a extensão com sucesso`,
    });
    chrome.storage.session.set({ state: "logged" });
    window.location.href = "redirect.html";
  } else {
    chrome.runtime.sendMessage({
      type: "console",
      message: "Não foi possível acessar o servidor: Token inválido",
    });
    alert("Token Inválido");
  }
}
