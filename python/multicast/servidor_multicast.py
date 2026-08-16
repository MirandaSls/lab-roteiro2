import socket
import time

OFFSET = 54  # dois ultimos digitos da matricula (secao 3.3)

GRUPO_MULTICAST = "230.0.0.1"
# Base 4646 (nao 4446): a porta 4500 e reservada pelo Windows (IPsec NAT-T) e descarta o multicast.
PORTA = 4646 + OFFSET  # 4700


def ip_local():
    # Descobre o IP da interface de rede local (nao envia nada; so resolve a rota de saida).
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


IP = ip_local()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
# Fixa a interface de saida do multicast; sem isso o Windows pode mandar pela interface errada.
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(IP))
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

print(f"[Multicast] Enviando avisos para o grupo {GRUPO_MULTICAST}:{PORTA}")
for contador in range(1, 6):
    mensagem = f"Aviso #{contador}: a aula comeca em {5 - contador} minuto(s)!"
    sock.sendto(mensagem.encode("utf-8"), (GRUPO_MULTICAST, PORTA))
    print(f"[Multicast] Enviado: {mensagem}")
    time.sleep(2)

sock.close()
