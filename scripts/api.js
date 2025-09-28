async function callAPI(method, server, payload) {
  let response = null;
  try {
    response = await fetch(server, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });
  } catch (error) {
    chrome.runtime.sendMessage({
      type: "console",
      message: `[callAPI] Erro ao chamar API: ${error}`,
    });
    return null;
  }

  if (response && response.ok) {
    const data = await response.json();
    chrome.runtime.sendMessage({
      type: "console",
      message: `[callAPI] Sucesso: ${JSON.stringify(data)}`,
    });
    return data;
  } else {
    chrome.runtime.sendMessage({
      type: "console",
      message: `[callAPI] Falha: ${
        response ? response.status : "Sem resposta"
      }`,
    });
    return null;
  }
}

export default { callAPI };
