#### Funções

- **`retrieveUser`**  
  Recupera o usuário armazenado na sessão do Chrome (`chrome.storage.session`). Retorna uma **Promise** que resolve com o valor do usuário ou rejeita caso ocorra algum erro.

- **`stopRecording`**  
  Interrompe a gravação atual. Evita múltiplas chamadas simultâneas usando a flag `isStopping` e envia uma mensagem de log com o usuário que parou a gravação.

- **`recordTabs`**  
  Registra informações da aba atual. Recupera a aba ativa, os dados da aula (`lectureLink`) e o usuário atual, monta um payload e envia:
  - Para o `background.js` via `chrome.runtime.sendMessage`  
  - Para a API externa usando `api.callAPI`

- **`getTab`**  
  Retorna a aba ativa na janela atualmente focada usando `chrome.tabs.query`.

- **`buildPayload`**  
  Monta um objeto (`payload`) com informações da aba, aula e usuário para envio à API. Inclui dados como URL, título da aba, status de áudio, timestamps e tipo de evento.

- **`isTitleValid`**  
  Verifica se o título da aba corresponde ao padrão definido por regex (`/^\[[^\]]+\]/`). Retorna `true` se válido, `false` caso contrário.

- **`extractSubject`**  
  Extrai o assunto de uma aula a partir do título da aba, considerando o conteúdo entre colchetes `[ ]`.

- **`standardizeSubject`**  
  Padroniza o assunto extraído, convertendo para letras minúsculas e substituindo espaços por `_`.