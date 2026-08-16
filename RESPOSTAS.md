# Respostas — Lab de Redes (Central de Avisos da Turma)

**Aluno:** MirandaSls · **Modalidade:** individual · **OFFSET (matrícula):** 54

Portas usadas: TCP 5054 · UDP 5055 · Multicast 4700 · WebSocket Java 8941 / Python 8942.

> Nota sobre a porta do multicast: `4446 + OFFSET(54) = 4500`, mas a **4500/UDP é reservada pelo Windows (IPsec NAT-T)** e descarta datagramas multicast silenciosamente. Por isso a base foi ajustada para 4646, resultando na porta **4700**.

> Uso de IA declarado: este texto foi feitos com apoio do Claude, usado para redação e organização; entendo e sei defender cada trecho.

---

## Parte A — TCP

**1. O que acontece se você iniciar o cliente antes do servidor? Por quê (considerando o TCP)?**

O cliente falha imediatamente com um erro de conexão recusada (`ConnectException: Connection refused` em Java, `ConnectionRefusedError` em Python). Isso ocorre porque o TCP é orientado a conexão: antes de trocar qualquer dado ele precisa completar o *handshake* de três vias (SYN → SYN-ACK → ACK). Como não há nenhum processo escutando na porta 5054, o sistema operativo responde ao SYN com um pacote RST (reset), e a tentativa de `connect()` é rejeitada na hora. Sem servidor aceitando, não há com quem estabelecer a conexão.

**2. O TCP garante ordem das mensagens. Qual mecanismo do protocolo é responsável por isso?**

Os **números de sequência** (sequence numbers). Cada byte enviado recebe um número de sequência; o receptor usa esses números para remontar o fluxo na ordem correta, mesmo que os segmentos cheguem fora de ordem pela rede, e para detectar lacunas. Junto com os **ACKs** (confirmações) e a retransmissão de segmentos perdidos, isso garante entrega ordenada e sem duplicatas. No código, por isso, basta usar `readLine()` / `recv()` sequencialmente: o TCP já entrega em ordem.

**3. O que aconteceria se dois clientes tentassem se conectar ao mesmo tempo? O código atual suporta? Justifique observando o código do servidor.**

O código atual **não** suporta dois clientes simultâneos. Tanto em Java (`servidor.accept()` chamado uma única vez) quanto em Python (um único `servidor.accept()`), o servidor aceita **uma** conexão, entra no laço de troca de mensagens com ela e, ao terminar, o `main` encerra — não há laço de `accept()` nem threads. Enquanto o primeiro cliente está conectado, um segundo `connect()` fica retido na fila de espera do socket (backlog do `listen`); ele só seria atendido se o servidor voltasse a chamar `accept()`, o que não acontece. Para suportar vários clientes seria preciso um laço `while (true) accept()` criando uma **thread** (ou processo/async) por cliente.

---

## Parte B — UDP

**1. O que aconteceu ao enviar uma mensagem com o servidor desligado? Compare com o TCP e relacione com "sem conexão".**

O envio em si **não falha**: como o UDP não estabelece conexão, o `send()` apenas entrega o datagrama à rede e retorna com sucesso, sem saber se há alguém do outro lado. O problema aparece depois, quando o cliente tenta receber a resposta. No meu teste, em `localhost` no Windows, o cliente Python **estourou o erro `ConnectionResetError: [WinError 10054]`** ao chamar `recvfrom()` logo após eu derrubar o servidor: o sistema operativo devolve um ICMP "port unreachable" (a porta não tem mais ninguém escutando) e esse ICMP faz o `recvfrom()` falhar em vez de esperar. Vale notar que entre **máquinas diferentes** (rede real), sem esse ICMP de volta, o cliente simplesmente **travaria** esperando uma resposta que nunca chega. Em TCP o comportamento seria diferente já no começo: nem o `connect()` inicial teria sucesso (erro de conexão recusada), pois o handshake exige um servidor ativo. Essa é a essência do "sem conexão": o UDP dispara o datagrama sem garantir que exista um receptor, e a ausência dele só é percebida depois — por erro ou por espera infinita.

**2. Dois exemplos reais que usam UDP e por que a confiabilidade do TCP não é essencial (ou atrapalharia).**

- **DNS:** uma consulta é curta (uma pergunta, uma resposta) e a latência importa muito. Abrir e fechar um handshake TCP para cada resolução seria desperdício; se a resposta se perder, a própria aplicação reenvia. O baixo overhead do UDP é ideal.
- **VoIP / streaming de áudio e vídeo em tempo real (e jogos online):** aqui a pontualidade vale mais que a integridade total. Se um pacote se perde, é melhor descartá-lo e seguir do que esperar uma retransmissão que chegaria atrasada e travaria o áudio/vídeo. A garantia de entrega e ordem do TCP, nesse caso, atrapalharia (causaria *buffering* e atraso).

**3. O servidor UDP não registra "quem está conectado". Seria possível implementar isso? O que mudaria na arquitetura?**

Sim, é possível — mas seria uma abstração criada **pela aplicação**, não pelo protocolo. O servidor guardaria uma estrutura (lista/dicionário) com os endereços `IP:porta` vistos nos `recvfrom`, tratando cada um como uma "sessão", com *heartbeats* periódicos e um *timeout* para expirar quem parou de responder. Isso transforma o servidor de **sem estado** (stateless) em **com estado** (stateful): ele passa a gastar memória por cliente e a gerir ciclo de vida de sessões, aproximando-se do que o TCP já faz nativamente — só que reinventado por cima do UDP.

---

## Parte C — Multicast

**1. Diferença entre unicast repetido 3x e multicast único, em termos de tráfego de rede.**

No unicast repetido, a origem envia **três cópias** independentes (uma para cada destinatário), precisa conhecer o endereço de cada um, e o tráfego que sai da origem cresce linearmente com o número de destinos. No multicast, a origem envia **um único** datagrama para o endereço de grupo (230.0.0.1); a **rede** (roteadores/switches) é que replica o pacote apenas nos pontos onde há membros inscritos, o mais perto possível deles. Resultado: muito menos tráfego no enlace da origem, escala melhor com N destinatários, e a origem nem precisa saber quem são os destinatários.

**2. O que é o TTL configurado no socket multicast e por que importa para o alcance dos pacotes?**

O **TTL (time-to-live)** é um contador no cabeçalho IP. Cada roteador que encaminha o pacote decrementa esse valor em 1; quando chega a 0, o pacote é descartado. Em multicast ele define o **escopo/alcance**: TTL 1 restringe o tráfego à sub-rede local; valores maiores permitem atravessar mais roteadores. Importa porque evita que avisos multicast "vazem" para além da rede pretendida, contendo o raio de propagação. No nosso servidor Python isso está explícito (`IP_MULTICAST_TTL = 2`).

**3. Se um cliente ficar offline e voltar depois, ele recebe os avisos que perdeu? Por quê? Relacione com a arquitetura de grupo.**

Não recebe. O multicast é *best-effort* e **sem estado/histórico**, como o UDP: a entrega acontece em tempo real apenas para quem está inscrito no grupo **no momento do envio**. Não existe buffer, retransmissão ou um servidor guardando mensagens por membro — o emissor sequer conhece os destinatários. Quem estava offline (ou ainda não tinha feito o *join* no grupo) simplesmente não vê aquele aviso. Na arquitetura de grupo, "publicar" é um evento instantâneo; recuperar histórico exigiria outra camada (ex.: um servidor de mensagens persistente).

---

## Parte D — WebSocket

**1. Depois do handshake HTTP com `Upgrade: websocket`, o que exatamente muda na conexão?**

A conexão deixa de seguir o modelo requisição/resposta do HTTP e passa a ser um **canal TCP persistente e full-duplex** de mensagens (frames) WebSocket. Sobre o **mesmo** socket TCP, os dois lados podem enviar dados a qualquer momento, de forma independente, sem reabrir conexão nem repetir cabeçalhos HTTP a cada mensagem. Em resumo: o protocolo de aplicação muda de *stateless request/response* para uma comunicação **bidirecional orientada a mensagens**, com baixo overhead por mensagem.

**2. Compare o mural (WebSocket) com o aviso (Multicast): como cada um descobre e alcança os destinatários?**

- **WebSocket (mural):** o **servidor** mantém explicitamente a lista de conexões (`getConnections()` em Java, o `set` `clientes_conectados` em Python) e faz o *fan-out* em software — envia uma cópia da mensagem por cada conexão TCP aberta. Ele conhece individualmente cada cliente; a replicação acontece num ponto central (o servidor).
- **Multicast:** o emissor **não** conhece os destinatários; envia para um endereço de grupo e é a **rede** que entrega aos inscritos. A "descoberta" se dá por IGMP (o cliente faz *join* no grupo), não por uma lista mantida no servidor.

Ou seja: WebSocket faz *fan-out* na **aplicação**, endereçando por conexão; multicast faz *fan-out* na **rede**, endereçando por grupo.

**3. Por que o WebSocket é mais adequado que TCP "cru" (Parte A) para o mural em tempo real, mesmo ambos sendo TCP?**

O TCP cru entrega um **fluxo de bytes sem fronteiras de mensagem**: para um mural, você teria que inventar seu próprio enquadramento (delimitadores/tamanho), protocolo de controle e lógica de broadcast do zero. O WebSocket já oferece, de forma padronizada sobre esse mesmo TCP: **enquadramento por mensagens**, handshake sobre HTTP (o que o torna compatível com navegadores e amigável a proxies/portas web), controle de conexão (ping/pong, fechamento limpo) e uma API de eventos (`onOpen`/`onMessage`/`onClose`) que torna natural repassar uma mensagem a todos os clientes. Ambos são TCP por baixo, mas o WebSocket adiciona exatamente a camada de mensagens bidirecionais que o cenário de mural em tempo real precisa — sobretudo para clientes web.
