"""Loop de uma partida: alterna os agentes até o jogo acabar.

Este é o "motor" do jogo. Ele não sabe quem são os agentes (humano, aleatório
ou IA); só pede a cada um a sua jogada e aplica as regras.
"""

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


def jogar_partida(agente_max, agente_min, mostrar=True):
    """Executa uma partida completa e devolve o vencedor (MAX, MIN ou None).

    agente_max joga com X e começa; agente_min joga com O.
    mostrar=False deixa a partida silenciosa (útil para experimentos).
    """
    agentes = {MAX: agente_max, MIN: agente_min}

    tabuleiro = criar_tabuleiro()
    jogador = MAX  # MAX sempre começa
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

    # O jogo acabou: a utilidade diz quem venceu.
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
