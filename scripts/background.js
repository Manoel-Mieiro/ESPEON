import api from "./api.js";
import record from "./record.js";
import { CONFIG } from "./config.js";
import button from "./button.js";
import { 
  logger, 
  titleLogger, 
  tabLogger, 
  storageLogger,
  apiLogger 
} from "./logger.js";

// Inicialização
chrome.storage.session.set({ regexValidated: false });
logger.info('Storage session inicializado - regexValidated: false');
let lastValidatedTitle = "";

async function shouldRecord() {
  const { recording } = await chrome.storage.session.get("recording");
  logger.debug(`shouldRecord() - recording: ${recording}`);
  return recording;
}

function normalizeTeamsTitle(title) {
  logger.debug(`Normalizando título: "${title}"`);
  
  // Remove o sufixo " | Microsoft Teams"
  title = title.replace(/\s*\|\s*Microsoft Teams\s*$/i, "");
  logger.debug(`Após remover sufixo Teams: "${title}"`);

  const parts = title.split("|").map(p => p.trim()).filter(Boolean);
  const result = parts.length > 0 ? parts[parts.length - 1] : title;
  
  logger.debug(`Título normalizado: "${result}"`);
  return result;
}

async function validateTitle(tab) {
  try {
    const { regexValidated } = await chrome.storage.session.get("regexValidated");
    const { lectureLink } = await chrome.storage.session.get(["lectureLink"]);

    titleLogger.debug('Validando título', {
      tabTitle: tab.title,
      lastValidatedTitle,
      regexValidated,
      hasLectureLink: !!lectureLink
    });

    if (
      !tab.title ||
      tab.title === lastValidatedTitle ||
      regexValidated ||
      !lectureLink
    ) {
      titleLogger.debug('Validação ignorada - condição não atendida');
      return;
    }

    titleLogger.info(`Iniciando validação do título: "${tab.title}"`);
    lastValidatedTitle = tab.title;

    const normalizedTitle = normalizeTeamsTitle(tab.title);
    titleLogger.debug(`Título normalizado para validação: "${normalizedTitle}"`);

    const isValid = record.isTitleValid(normalizedTitle);
    titleLogger.info(`Resultado validação REGEX: ${isValid}`, {
      normalizedTitle,
      isValid
    });

    if (isValid && !regexValidated) {
      await chrome.storage.session.set({ regexValidated: true });
      await chrome.storage.session.set({ shouldMonitor: true });
      await chrome.storage.session.set({ entrypoint: tab.id });
      
      storageLogger.info('Storage atualizado após regex válida', {
        regexValidated: true,
        shouldMonitor: true,
        entrypoint: tab.id
      });

      await chrome.storage.session.set({ recording: true });
      titleLogger.info('GRAVAÇÃO INICIADA - Regex válida detectada');
    }
  } catch (error) {
    titleLogger.error('Erro na validação do título', error);
  }
}

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  logger.debug('Mensagem recebida', {
    type: request.type,
    sender: sender.tab?.id
  });

  if (request.type === "click_event") {
    logger.info("Click event capturado na webpage");
  } else if (request.type === "console") {
    logger.info("Mensagem da content script", request.message);
  } else if (request.type === "tabData") {
    apiLogger.info("Enviando dados para API", {
      url: `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
      payloadSize: JSON.stringify(request.payload).length
    });
    
    api.callAPI(
      "POST",
      `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
      request.payload
    );
  }
});

chrome.tabs.onActivated.addListener(async (activeInfo) => {
  try {
    tabLogger.info('Tab activated', { tabId: activeInfo.tabId });
    
    // Busca tab e valida REGEX
    const tab = await chrome.tabs.get(activeInfo.tabId);
    tabLogger.debug('Tab details', {
      id: tab.id,
      title: tab.title,
      url: tab.url
    });

    await validateTitle(tab);

    // Verifica se prossegue com base na validação anterior
    const { shouldMonitor } = await chrome.storage.session.get(["shouldMonitor"]);
    tabLogger.debug('Status do monitoramento', { shouldMonitor });

    if (!shouldMonitor) {
      tabLogger.debug('Monitoramento desativado - ignorando evento');
      return;
    }

    if (!(await shouldRecord())) {
      tabLogger.debug('Gravação não está ativa - ignorando evento');
      return;
    }

    const lecture = await chrome.storage.session.get(["lectureLink"]);
    const expectedTab = await chrome.storage.session.get(["entrypoint"]);
    const lectureTab = await chrome.tabs.get(expectedTab.entrypoint);
    const student = await record.retrieveUser();

    tabLogger.debug('Dados para comparação', {
      currentTab: tab.id,
      expectedTab: expectedTab.entrypoint,
      student,
      hasLectureLink: !!lecture.lectureLink
    });

    if (tab.id !== expectedTab.entrypoint) {
      tabLogger.warn(`🚪 ${student} saiu da tab do Teams`, {
        fromTab: expectedTab.entrypoint,
        toTab: tab.id,
        toTitle: tab.title
      });

      const payload = record.buildPayload(
        lectureTab,
        tab,
        lecture.lectureLink,
        "onActivated",
        student
      );

      apiLogger.info('Enviando payload para API (onActivated)');
      api.callAPI(
        "POST",
        `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
        payload
      );
    } else {
      tabLogger.debug('Usuário permanece na tab do Teams');
    }
  } catch (error) {
    tabLogger.error('Erro no onActivated', error);
  }
});

chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
  try {
    if (changeInfo.status === "complete") {
      tabLogger.info('📄 Tab updated', {
        tabId,
        status: changeInfo.status,
        title: tab.title,
        url: tab.url
      });

      // Valida REGEX
      await validateTitle(tab);

      // Verifica se prossegue
      const { shouldMonitor } = await chrome.storage.session.get(["shouldMonitor"]);
      tabLogger.debug('Status do monitoramento', { shouldMonitor });

      if (!shouldMonitor) {
        tabLogger.debug('Monitoramento desativado - ignorando evento');
        return;
      }

      if (!(await shouldRecord())) {
        tabLogger.debug('Gravação não está ativa - ignorando evento');
        return;
      }

      const lecture = await chrome.storage.session.get(["lectureLink"]);
      const expectedTab = await chrome.storage.session.get(["entrypoint"]);
      const lectureTab = await chrome.tabs.get(expectedTab.entrypoint);
      const student = await record.retrieveUser();

      tabLogger.debug('Dados para comparação', {
        currentTab: tab.id,
        expectedTab: expectedTab.entrypoint,
        student,
        hasLectureLink: !!lecture.lectureLink
      });

      if (tab.id !== expectedTab.entrypoint) {
        tabLogger.warn(`🚪 ${student} saiu da tab do Teams`, {
          fromTab: expectedTab.entrypoint,
          toTab: tab.id,
          toTitle: tab.title
        });

        const payload = record.buildPayload(
          lectureTab,
          tab,
          lecture.lectureLink,
          "onUpdated",
          student
        );

        apiLogger.info('Enviando payload para API (onUpdated)');
        api.callAPI(
          "POST",
          `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
          payload
        );
      } else {
        tabLogger.debug('Usuário permanece na tab do Teams');
      }
    }
  } catch (error) {
    tabLogger.error('Erro no onUpdated', error);
  }
});

globalThis.debugExtension = {
  async getStatus() {
    const status = await chrome.storage.session.get([
      'regexValidated', 
      'shouldMonitor', 
      'recording', 
      'entrypoint', 
      'lectureLink'
    ]);
    logger.info('Status completo da extensão', status);
    return status;
  },
  
  async resetValidation() {
    await chrome.storage.session.set({ regexValidated: false });
    lastValidatedTitle = "";
    logger.info('Validação resetada');
  },
  
  async forceRecording() {
    await chrome.storage.session.set({ recording: true });
    logger.info('Gravação forçada ativada');
  },
  
  async clearStorage() {
    await chrome.storage.session.clear();
    logger.info('Storage session limpo');
  }
};

logger.info('Background script inicializado com sistema de logs');