import java.net.*;
import java.io.IOException;

public class ClienteMulticast {
    static final int OFFSET = 54; // MESMO valor do servidor (secao 3.3)

    public static void main(String[] args) throws IOException {
        String grupoMulticast = "230.0.0.1";
        // Base 4646 (nao 4446): 4500 e reservada pelo Windows (IPsec NAT-T). 4646 + OFFSET(54) = 4700.
        int porta = 4646 + OFFSET; // 4700

        try (MulticastSocket socket = new MulticastSocket(porta)) {
            InetAddress grupo = InetAddress.getByName(grupoMulticast);
            InetSocketAddress endpointGrupo = new InetSocketAddress(grupo, porta);

            // Inscreve-se no grupo pela interface de rede local. Se estiver em Wi-Fi corporativa/VPN
            // que bloqueia multicast, veja a secao 6.5 do roteiro (troubleshooting).
            NetworkInterface interfaceRede = NetworkInterface.getByInetAddress(InetAddress.getLocalHost());

            socket.joinGroup(endpointGrupo, interfaceRede);
            System.out.println("[Multicast] Inscrito no grupo " + grupoMulticast + ":" + porta + ". Aguardando avisos...");

            byte[] buffer = new byte[1024];
            while (true) {
                DatagramPacket pacote = new DatagramPacket(buffer, buffer.length);
                socket.receive(pacote);
                String mensagem = new String(pacote.getData(), 0, pacote.getLength());
                System.out.println("[Multicast] Recebido: " + mensagem);
            }
        }
    }
}
