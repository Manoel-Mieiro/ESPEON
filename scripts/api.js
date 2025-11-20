import { apiLogger } from './logger.js';

async function callAPI(method, server, payload) {
  let response = null;
  try {
    apiLogger.debug(`Chamando API: ${method} ${server}`, payload);
    
    response = await fetch(server, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  } catch (error) {
    apiLogger.error(`Erro ao chamar API: ${error}`);
    return null;
  }

  if (response && response.ok) {
    const data = await response.json();
    apiLogger.info(`Sucesso na API: ${JSON.stringify(data)}`);
    return data;
  } else {
    apiLogger.warn(`Falha na API: ${response ? response.status : "Sem resposta"}`);
    return null;
  }
}

export default { callAPI };