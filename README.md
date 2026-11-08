# Algoritmo de Berkeley

## O sistema simula até 5 processos independentes (1 Coordenador e 4 Participantes), cada qual rodando com um relógio inicial dessincronizado (com offset próprio em relação ao tempo real) e comunicando-se exclusivamente via rede TCP. 
- Cada processo deve ser executado em um terminal diferente.

# Passo a Passo para Execução
- Para testar cada processo, abra um terminal separado na mesma máquina (ou em máquinas diferentes na mesma rede, ajustando os IPs).
- Atribua relógios iniciais com diferentes desvios (offsets) para evidenciar a dessincronização e a correção posterior.

## Para inicializar o "coordenador"
```python coordenador.py --offset 15.0```
- O valor representa o desvio do horário atual em segundos, podendo ser pra mais ou para menos

## Para inicializar o(s) participante(s)
```python participante.py --id 1 --offset -25.0```
- Para adicionar um outro participante, basta alterar o valor do "id" e selecionar o desvio.

## Observação
- Após cada participante se conectar, aparecerá a confirmação no terminal do coordenador que ele foi conectado por TCP;
- O coordenador pode pode sincronizar o relógio a partir da conexão do primeiro participante;
- Algumas informações serão apresentadas nos processos: O estado inicial dos relógios divergentes; A troca de mensagens via sockets TCP encapsuladas em JSON; O cálculo da média feito pelo coordenador; O estado final devidamente sincronizado;
- Para um melhor efeito didático, o coordenador aceita qualquer horário que os participantes se conectarem.