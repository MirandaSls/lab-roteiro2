# Central de Avisos da Turma — Lab de Redes

Laboratório de Desenvolvimento de Aplicações Móveis e Distribuídas — U0 (Nivelamento de Redes).

Mesmo cenário (central de comunicação da turma) implementado com **4 protocolos** de rede, cada um em **Java** e **Python**:

| Parte | Protocolo | Porta (OFFSET 54) | Cenário |
|---|---|---|---|
| A | TCP | 5054 | Aluno pergunta ao monitor e recebe resposta (confiável, 1-a-1) |
| B | UDP | 5055 | Mesmo pedido, sem garantia de entrega |
| C | Multicast | 4500 | Professor avisa todos os alunos do grupo de uma vez |
| D | WebSocket | 8941 (Java) / 8942 (Python) | Mural de avisos em tempo real |

## Estrutura

```
java/       tcp, udp, multicast (javac direto) + websocket (Maven)
python/     tcp, udp, multicast, websocket
evidencias/ prints de execução por protocolo
RESPOSTAS.md  respostas das 12 perguntas
```

## Como rodar

Cada pasta traz servidor e cliente. Ver instruções em `RESPOSTAS.md` e nos comentários de cada arquivo.
