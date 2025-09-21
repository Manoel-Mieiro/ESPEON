#### Funções

- **`shouldRecord`**  
  Verifica no armazenamento (`storage`) se existe a chave `recording` e qual é o seu valor.

- **`validateTitle(tab)`**  
  Função assíncrona que valida o título da aba atual (`tab.title`) e controla o início do monitoramento e da gravação.

  **Descrição do fluxo:**
  1. Recupera do `storage.session` os valores `regexValidated` e `lectureLink`.
  2. Verifica se o título da aba é válido para gravação:
     - Não está vazio.
     - Não é igual ao último título validado (`lastValidatedTitle`).
     - Regex ainda não validado.
     - Há links de aula disponíveis (`lectureLink`).
  3. Se válido, atualiza o `storage.session` com:
     - `regexValidated: true`  
     - `shouldMonitor: true`  
     - `entrypoint: tab.id` (âncora da extensão)  
     - `recording: true` (inicia a gravação)  
  4. Registra logs para acompanhamento do processo.

### `chrome.runtime.onMessage` Listener

Este trecho do `background.js` escuta mensagens enviadas para a extensão e realiza ações específicas de acordo com o tipo da mensagem.

#### Funcionalidade:

- **Evento de clique (`click_event`)**  
  Captura cliques na página atual e registra no console:
  ```js
  console.log("Click event captured in current webpage");

  ### `chrome.tabs.onActivated` Listener

Este listener é acionado sempre que uma aba é ativada no navegador. Ele valida se a aba atual deve ser monitorada e, caso necessário, envia dados para a API.

#### Fluxo de funcionamento:

1. **Validação do título da aba**  
   - Busca a aba ativa usando `chrome.tabs.get(activeInfo.tabId)`.  
   - Chama a função `validateTitle(tab)` para verificar se o título atende à regex configurada.

2. **Checagem de monitoramento**  
   - Recupera do `storage.session` a flag `shouldMonitor`.  
   - Se `shouldMonitor` for falso, a função retorna e não prossegue.  
   - Também verifica se a gravação deve ocorrer chamando `shouldRecord()`.

3. **Recuperação de dados adicionais**  
   - Busca `lectureLink` e `entrypoint` no `storage.session`.  
   - Obtém o título da aba de referência (`entrypoint`).  
   - Extrai o assunto da aula com `record.extractSubject(title.title)`.  
   - Padroniza o assunto com `record.standardizeSubject(subject)`.  
   - Recupera o usuário atual via `record.retrieveUser()`.

4. **Verificação de saída da aba de Teams**  
   - Se a aba ativada não for a de entrada (`entrypoint`), considera que o aluno saiu da aba do Microsoft Teams.  
   - Monta o payload com `record.buildPayload(...)`.  
   - Envia os dados para a API:
     ```js
     api.callAPI(
       "POST",
       `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
       payload
     );
     ```

5. **Logs para depuração**  
   - ID da aba atual, ID do `entrypoint`, assunto, endpoint e usuário são exibidos no console.

#### Observações
- Esse listener garante que apenas a aba correta (Teams) seja monitorada e que qualquer mudança de aba seja registrada.  
- A função `validateTitle` e o `shouldRecord` controlam se o monitoramento deve iniciar ou não.  

### `chrome.tabs.onUpdated` Listener

Este listener é acionado sempre que uma aba é atualizada (por exemplo, quando a página termina de carregar). Ele verifica se a aba atual deve ser monitorada e envia dados à API quando necessário.

#### Fluxo de funcionamento:

1. **Validação do status da aba**  
   - O listener só age quando `changeInfo.status === "complete"`, ou seja, quando a aba terminou de carregar.

2. **Validação do título da aba**  
   - Chama `validateTitle(tab)` para verificar se o título atende à regex configurada.

3. **Checagem de monitoramento**  
   - Recupera do `storage.session` a flag `shouldMonitor`.  
   - Retorna caso o monitoramento não esteja ativo.  
   - Também verifica se a gravação deve ocorrer chamando `shouldRecord()`.

4. **Recuperação de dados adicionais**  
   - Busca `lectureLink` e `entrypoint` no `storage.session`.  
   - Obtém o título da aba de referência (`entrypoint`).  
   - Recupera o usuário atual via `record.retrieveUser()`.

5. **Verificação de saída da aba de Teams**  
   - Se a aba atual não for a de entrada (`entrypoint`), considera que o aluno deixou a aba do Microsoft Teams.  
   - Monta o payload com `record.buildPayload(...)`.  
   - Envia os dados para a API:
     ```js
     api.callAPI(
       "POST",
       `${CONFIG.API_BASE_URL}${CONFIG.API_ENDPOINT}`,
       payload
     );
     ```

6. **Logs para depuração**  
   - ID da aba atual, ID do `entrypoint` e título da aba são exibidos no console.

#### Observações
- Esse listener complementa o `onActivated` para monitorar mudanças mesmo quando a aba é atualizada, garantindo que qualquer saída da aba de Teams seja registrada.  
- A função `validateTitle` e o `shouldRecord` controlam se o monitoramento deve iniciar ou não.
