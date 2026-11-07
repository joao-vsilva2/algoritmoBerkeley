import argparse
import json
import socket
import time
import random

def calcular_media_berkeley(tempos_coletados, tempo_coordenador, tolerancia=10.0):
    """
    Calcula a média de Berkeley, descartando valores discrepantes (outliers)
    se ultrapassarem a tolerância definida.
    """
    todos_tempos = [(0, tempo_coordenador)] # (id_participante, tempo) -> id 0 é o coordenador
    for p_id, t in tempos_coletados.items():
        todos_tempos.append((p_id, t))
    
    print(f"\n[COORDENADOR] Tempos brutos coletados: {todos_tempos}")
    
    # Filtragem de discrepantes em relação ao coordenador (opcional, mas recomendado no algoritmo)
    tempos_validos = []
    for p_id, t in todos_tempos:
        diff = abs(t - tempo_coordenador)
        if diff <= tolerancia:
            tempos_validos.append((p_id, t))
        else:
            print(f"[COORDENADOR] Aviso: Participante {p_id} descartado por discrepância (diferença de {diff:.2f}s).")

    # Calcula a média dos relógios válidos
    soma = sum(t for _, t in tempos_validos)
    media = soma / len(tempos_validos)
    
    print(f"[COORDENADOR] Tempo médio calculado: {media:.2f}")
    
    # Calcula os ajustes necessários para cada processo
    ajustes = {}
    for p_id, t in tempos_validos:
        ajustes[p_id] = media - t
        
    return ajustes, media

def main():
    parser = argparse.ArgumentParser(description="Coordenador do Algoritmo de Berkeley")
    parser.add_argument("--host", default="127.0.0.1", help="Endereço IP do coordenador")
    parser.add_argument("--port", type=int, default=5000, help="Porta TCP do coordenador")
    parser.add_argument("--participantes", type=int, default=4, help="Número de participantes esperados")
    parser.add_argument("--offset", type=float, default=15.0, help="Desvio inicial do relógio do coordenador (em segundos)")
    args = parser.parse_args()

    # Relógio inicial do coordenador (Tempo real + offset simulado)
    tempo_local_inicial = time.time() + args.offset
    print(f"[COORDENADOR] Iniciando... Relógio inicial: {time.strftime('%H:%M:%S', time.localtime(tempo_local_inicial))} (Offset: {args.offset}s)")

    # Configuração do socket TCP do Coordenador
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((args.host, args.port))
    server_socket.listen(args.participantes)
    
    print(f"[COORDENADOR] Escutando conexões em {args.host}:{args.port}...")

    conexoes = []
    enderecos = []

    # Passo 1: Estabelecer conexões com os 4 participantes
    while len(conexoes) < args.participantes:
        conn, addr = server_socket.accept()
        conexoes.append(conn)
        enderecos.append(addr)
        print(f"[COORDENADOR] Participante conectado de {addr} (Total: {len(conexoes)}/{args.participantes})")

    input("\n[COORDENADOR] Pressione ENTER para iniciar a sincronização de relógios...")

    # Simula o avanço do relógio local do coordenador no momento da consulta
    tempo_coordenador_consulta = time.time() + args.offset
    
    # Passo 1 (Cont.): O Coordenador solicita os valores atuais dos relógios
    tempos_coletados = {}
    print("\n--- PASSO 1: Coordenador solicitando horários aos participantes ---")
    
    for i, conn in enumerate(conexoes):
        p_id = i + 1
        mensagem_requisicao = json.dumps({"acao": "SOLICITAR_TEMPO"})
        conn.sendall(mensagem_requisicao.encode('utf-8'))
        
        # Recebe o tempo do participante
        dados = conn.recv(1024).decode('utf-8')
        resposta = json.loads(dados)
        tempo_participante = resposta["tempo"]
        tempos_coletados[p_id] = tempo_participante
        print(f"[COORDENADOR] Hora recebida do Participante {p_id}: {time.strftime('%H:%M:%S', time.localtime(tempo_participante))}")

    # Passo 2: Cálculo de ajustes
    print("\n--- PASSO 2: Calculando ajustes de tempo ---")
    ajustes, tempo_medio = calcular_media_berkeley(tempos_coletados, tempo_coordenador_consulta)

    # Aplicação do ajuste do próprio coordenador
    ajuste_coordenador = ajustes.get(0, tempo_medio - tempo_coordenador_consulta)
    tempo_coordenador_final = tempo_coordenador_consulta + ajuste_coordenador

    # Passo 3: Envio de ajustes
    print("\n--- PASSO 3: Enviando ajustes calculados aos participantes ---")
    for i, conn in enumerate(conexoes):
        p_id = i + 1
        ajuste_p = ajustes.get(p_id, 0.0) # Se foi descartado, ajuste é 0
        mensagem_ajuste = json.dumps({"acao": "APLICAR_AJUSTE", "ajuste": ajuste_p})
        conn.sendall(mensagem_ajuste.encode('utf-8'))
        print(f"[COORDENADOR] Ajuste enviado para Participante {p_id}: {ajuste_p:+.2f} segundos")

    # Passo 5: Exibição de Resultados no Coordenador
    print("\n==================================================")
    print("             RESULTADO DA SINCRONIZAÇÃO           ")
    print("==================================================")
    print(f"Processo: COORDENADOR (ID 0)")
    print(f"  - Relógio Antes:  {time.strftime('%H:%M:%S', time.localtime(tempo_coordenador_consulta))}")
    print(f"  - Ajuste Aplicado: {ajuste_coordenador:+.2f}s")
    print(f"  - Relógio Depois: {time.strftime('%H:%M:%S', time.localtime(tempo_coordenador_final))}")
    print("==================================================")

    # Fechamento das conexões
    for conn in conexoes:
        conn.close()
    server_socket.close()
    print("[COORDENADOR] Sincronização concluída e conexões encerradas.")

if __name__ == "__main__":
    main()