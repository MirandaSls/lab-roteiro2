import java.net.*;
import java.io.IOException;

public class ServidorMulticast {
    static final int OFFSET = 54; // dois ultimos digitos da matricula (secao 3.3)

    public static void main(String[] args) throws IOException, InterruptedException {
        String grupoMulticast = "230.0.0.1";
        // Base 4646 (nao 4446): a porta 4500 e reservada pelo Windows (IPsec NAT-T) e o multicast
        // e silenciosamente descartado nela. 4646 + OFFSET(54) = 4700.
        int porta = 4646 + OFFSET; // 4700

        InetAddress grupo = InetAddress.getByName(grupoMulticast);
        try (DatagramSocket socket = new DatagramSocket()) {
            // Fixa a interface de saida do multicast na rede local desta maquina. Sem isso, no
            // Windows o SO pode escolher outra interface e o cliente local nao recebe nada.
            NetworkInterface interfaceRede = NetworkInterface.getByInetAddress(InetAddress.getLocalHost());
            socket.setOption(StandardSocketOptions.IP_MULTICAST_IF, interfaceRede);

            int contador = 1;
            System.out.println("[Multicast] Enviando avisos para o grupo " + grupoMulticast + ":" + porta);
            while (contador <= 5) {
                String mensagem = "Aviso #" + contador + ": a aula comeca em " + (5 - contador) + " minuto(s)!";
                byte[] dados = mensagem.getBytes();
                DatagramPacket pacote = new DatagramPacket(dados, dados.length, grupo, porta);
                socket.send(pacote);
                System.out.println("[Multicast] Enviado: " + mensagem);
                contador++;
                Thread.sleep(2000);
            }
        }
    }
}
