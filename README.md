# Algoritmo de Berkeley

## O sistema simula 5 processos independentes (1 Coordenador e 4 Participantes), cada qual rodando com um relógio inicial dessincronizado (com offset próprio em relação ao tempo real) e comunicando-se exclusivamente via rede TCP. 
- Cada processo deve ser executado em um terminal diferente.

# Passo a Passo para Execução
- Para testar o sistema com 5 processos independentes, abra 5 terminais separados na mesma máquina (ou em máquinas diferentes na mesma rede, ajustando os IPs).
- Atribua relógios iniciais com diferentes desvios (offsets) para evidenciar a dessincronização e a correção posterior.

## Para inicializar o "coordenado"
python coordenador.py --offset 15.0 
- O valor representa o tempo do offset, podendo ser um valor positivo ou negativo

## Para inicializar o(s) participante(s)
python participante.py --id 1 --offset -25.0
- Para adicionar um outro participante, basta alterar o valor do "id"

## Observação
- Após cada participante se conectar, aparecerá a confirmação no terminal do coordenado que ele foi conectado por TCP.
- Depois que todos os participantes forem conectados: pressione ENTER no Terminal do Coordenador para disparar a solicitação de horários.
- Algumas informações serão apresentadas nos processos: O estado inicial dos relógios divergentes; A troca de mensagens via sockets TCP encapsuladas em JSON; O cálculo da média e tolerância de Berkeley feito pelo coordenador; O estado final devidamente sincronizado.