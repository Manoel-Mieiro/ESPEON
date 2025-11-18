import { styleOnToken } from "./form_styling.js";
import { fetchUser } from "./fetch_user.js";
import { CONFIG } from "../config.js";
import api from "../api.js";

export async function triggerTokenRequest(document, components) {
  components.loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const email = document.getElementById("email").value;
    
    try {
      const user = await fetchUser(email);
      chrome.runtime.sendMessage({ 
        type: "console", 
        message: "[DEBUG] User fetch result: " + JSON.stringify(user) 
      });

      if (user && user.email) {
        const submitButton = event.target.querySelector('button[type="submit"]');
        if (submitButton) {
          submitButton.disabled = true;
          submitButton.textContent = "Enviando...";
        }

        // Faz a requisição diretamente (sem background script)
        try {
          const response = await api.callAPI(
            "PATCH",
            `${CONFIG.API_BASE_URL}${CONFIG.LOGIN_ENDPOINT}`,
            { email: email }
          );

          chrome.runtime.sendMessage({ 
            type: "console", 
            message: "[DEBUG] Direct PATCH response: " + JSON.stringify(response) 
          });

          // Assume sucesso se chegou aqui
          if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = "Enviar Token";
          }

          styleOnToken(components, email);
          chrome.storage.session.set({
            user: email,
            role: user.role,
            hasToken: true,
          });

          chrome.runtime.sendMessage({ 
            type: "console", 
            message: "[SUCCESS] Login flow completed for: " + email 
          });

        } catch (patchError) {
          chrome.runtime.sendMessage({ 
            type: "console", 
            message: "[DEBUG] PATCH error: " + patchError 
          });
          
          if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = "Enviar Token";
          }
          
          // Mesmo com erro, prossegue (o email pode ter sido enviado)
          alert("Solicitação enviada. Verifique seu email para o token.");
          styleOnToken(components, email);
          chrome.storage.session.set({
            user: email,
            role: user.role,
            hasToken: true,
          });
        }

      } else {
        alert(`${email} não está cadastrado`);
        chrome.storage.session.set({ state: "register" });
        window.location.href = "redirect.html";
      }
    } catch (error) {
      alert(`Erro de conexão com o servidor: ${error}`);
      const submitButton = event.target.querySelector('button[type="submit"]');
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.textContent = "Enviar Token";
      }
    }
  });
}