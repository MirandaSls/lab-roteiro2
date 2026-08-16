# Respostas — Lab de Redes (Central de Avisos da Turma)

**Aluno:** MirandaSls · **Modalidade:** individual · **OFFSET (matrícula):** 54

Portas usadas: TCP 5054 · UDP 5055 · Multicast 4500 · WebSocket Java 8941 / Python 8942.

---

## Parte A — TCP

**1. O que acontece se você iniciar o cliente antes do servidor? Por quê (considerando o TCP)?**

_(a preencher após implementar e testar)_

**2. O TCP garante ordem das mensagens. Qual mecanismo do protocolo é responsável por isso?**

_(a preencher)_

**3. O que aconteceria se dois clientes tentassem se conectar ao mesmo tempo? O código atual suporta? Justifique observando o código do servidor.**

_(a preencher)_

---

## Parte B — UDP

**1. O que aconteceu ao enviar uma mensagem com o servidor desligado? Compare com o TCP e relacione com "sem conexão".**

_(a preencher)_

**2. Dois exemplos reais de aplicações que usam UDP e por que a confiabilidade do TCP não é essencial (ou atrapalharia) em cada uma.**

_(a preencher)_

**3. O servidor UDP não registra "quem está conectado". Seria possível implementar isso? O que mudaria na arquitetura?**

_(a preencher)_

---

## Parte C — Multicast

**1. Diferença entre unicast repetido 3x e multicast único, em termos de tráfego de rede.**

_(a preencher)_

**2. O que é o TTL configurado no socket multicast e por que importa para o alcance dos pacotes?**

_(a preencher)_

**3. Se um cliente ficar offline e voltar, ele recebe os avisos que perdeu? Por quê? Relacione com a arquitetura de grupo.**

_(a preencher)_

---

## Parte D — WebSocket

**1. Depois do handshake HTTP com `Upgrade: websocket`, o que exatamente muda na conexão?**

_(a preencher)_

**2. Compare o mural (WebSocket) com o aviso (Multicast): como cada um descobre e alcança os destinatários?**

_(a preencher)_

**3. Por que o WebSocket é mais adequado que TCP "cru" (Parte A) para o mural em tempo real, mesmo ambos sendo TCP?**

_(a preencher)_
