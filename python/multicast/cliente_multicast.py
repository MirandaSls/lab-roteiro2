import socket
import struct

OFFSET = 54  # MESMO valor do servidor (secao 3.3)

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
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", PORTA))

grupo = socket.inet_aton(GRUPO_MULTICAST)
# Inscreve-se no grupo pela interface de rede local (o mesmo IP que o servidor usa para enviar).
interface = socket.inet_aton(IP)
solicitacao_membro = struct.pack("4s4s", grupo, interface)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, solicitacao_membro)

print(f"[Multicast] Inscrito no grupo {GRUPO_MULTICAST}:{PORTA}. Aguardando avisos...")
while True:
    dados, endereco = sock.recvfrom(1024)
    print(f"[Multicast] Recebido: {dados.decode('utf-8')}")
