import argparse
import json
import socket
import time

def main():
    parser = argparse.ArgumentParser(description="Processo Participante do Algoritmo de Berkeley")
    parser.add_argument("--id", type=int, required=True, help="ID único do participante (1 a 4)")
    parser.add_argument("--host", default="127.0.0.1", help="Endereço IP do coordenador")
    parser.add_argument("--port", type=int, default=5000, help="Porta TCP do coordenador")
    parser.add_argument("--offset", type=float, required=True, help="Desvio inicial do relógio (ex: -30.0, 25.5)")
    args = parser.parse_args()

    # Relógio inicial do participante com dessincronização customizada
    tempo_inicial = time.time() + args.offset
    print(f"[PARTICIPANTE {args.id}] Iniciado. Relógio inicial: {time.strftime('%H:%M:%S', time.localtime(tempo_inicial))} (Offset: {args.offset}s)")

    # Conexão TCP com o Coordenador
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[PARTICIPANTE {args.id}] Conectando ao Coordenador em {args.host}:{args.port}...")
    
    while True:
        try:
            client_socket.connect((args.host, args.port))
            break
        except ConnectionRefusedError:
            print(f"[PARTICIPANTE {args.id}] Coordenador não disponível. Tentando novamente em 2 segundos...")
            time.sleep(2)

    print(f"[PARTICIPANTE {args.id}] Conectado com sucesso! Aguardando instruções do Coordenador...")

    ajuste_aplicado = 0.0
    tempo_antes = tempo_inicial

    try:
        # Loop para receber mensagens do coordenador
        while True:
            dados = client_socket.recv(1024)
            if not dados:
                break
            
            mensagem = json.loads(dados.decode('utf-8'))
            acao = mensagem.get("acao")

            if acao == "SOLICITAR_TEMPO":
                # Simula o relógio local atualizado com o offset no momento da resposta
                tempo_atual = time.time() + args.offset
                tempo_antes = tempo_atual
                print(f"[PARTICIPANTE {args.id}] Solicitação recebida. Enviando tempo local: {time.strftime('%H:%M:%S', time.localtime(tempo_atual))}")
                
                resposta = json.dumps({"tempo": tempo_atual})
                client_socket.sendall(resposta.encode('utf-8'))

            elif acao == "APLICAR_AJUSTE":
                ajuste_aplicado = mensagem.get("ajuste", 0.0)
                # Passo 4: Aplicação do ajuste ao relógio local
                args.offset += ajuste_aplicado # Modifica o offset simulado do relógio
                tempo_final = time.time() + args.offset

                # Passo 5: Exibição de Resultados no Participante
                print("\n==================================================")
                print(f"             RESULTADO DA SINCRONIZAÇÃO           ")
                print("==================================================")
                print(f"Processo: PARTICIPANTE (ID {args.id})")
                print(f"  - Relógio Antes:  {time.strftime('%H:%M:%S', time.localtime(tempo_antes))}")
                print(f"  - Ajuste Aplicado: {ajuste_aplicado:+.2f}s")
                print(f"  - Relógio Depois: {time.strftime('%H:%M:%S', time.localtime(tempo_final))}")
                print("==================================================")
                break

    except Exception as e:
        print(f"[PARTICIPANTE {args.id}] Erro na comunicação: {e}")
    finally:
        client_socket.close()
        print(f"[PARTICIPANTE {args.id}] Conexão encerrada.")

if __name__ == "__main__":
    main()