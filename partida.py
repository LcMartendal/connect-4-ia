# Loop da partida: pede a jogada de cada agente e aplica no tabuleiro.

from regras import fim_de_jogo, utilidade
from tabuleiro import (
    MAX,
    MIN,
    SIMBOLOS,
    criar_tabuleiro,
    imprimir_tabuleiro,
    jogar,
    outro_jogador,
)


# Joga uma partida e devolve o vencedor (MAX, MIN ou None).
# agente_max joga com X e começa; com mostrar=False nada é impresso.
def jogar_partida(agente_max, agente_min, mostrar=True):
    agentes = {MAX: agente_max, MIN: agente_min}

    tabuleiro = criar_tabuleiro()
    jogador = MAX
    rodada = 1

    if mostrar:
        imprimir_tabuleiro(tabuleiro)

    while not fim_de_jogo(tabuleiro):
        agente = agentes[jogador]
        coluna = agente.escolher_jogada(tabuleiro, jogador)
        tabuleiro = jogar(tabuleiro, coluna, jogador)

        if mostrar:
            print(f"Rodada {rodada}: Agente {jogador} ({SIMBOLOS[jogador]}) jogou na coluna {coluna + 1}")
            imprimir_tabuleiro(tabuleiro)

        jogador = outro_jogador(jogador)
        rodada += 1

    valor = utilidade(tabuleiro)
    if valor > 0:
        vencedor = MAX
    elif valor < 0:
        vencedor = MIN
    else:
        vencedor = None

    if mostrar:
        if vencedor is None:
            print("Fim de jogo: EMPATE!")
        else:
            print(f"Fim de jogo: Agente {vencedor} ({SIMBOLOS[vencedor]}) VENCEU!")

    return vencedor
