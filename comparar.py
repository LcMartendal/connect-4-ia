"""Experimentos para a reflexão sobre o algoritmo escolhido.

1. Compara Minimax puro e Minimax com poda Alfa-Beta na mesma posição
   (mesma jogada escolhida, número de estados visitados e tempo).
2. Joga partidas da IA Alfa-Beta contra o agente aleatório.

Uso: python comparar.py
"""

import time

from agentes import AgenteAleatorio, AgenteMinimax
from partida import jogar_partida
from tabuleiro import MAX, MIN, criar_tabuleiro


def comparar_poda(profundidades=(2, 3, 4, 5)):
    """Mede o custo da primeira jogada com e sem poda, para várias profundidades."""
    tabuleiro = criar_tabuleiro()

    print("Primeira jogada (tabuleiro vazio), MAX a jogar")
    print(f"{'prof.':>5} | {'algoritmo':<10} | {'coluna':>6} | {'estados':>9} | {'tempo':>7}")
    print("-" * 50)

    for profundidade in profundidades:
        for usar_poda in (False, True):
            agente = AgenteMinimax(profundidade=profundidade, usar_poda=usar_poda)

            inicio = time.perf_counter()
            coluna = agente.escolher_jogada(tabuleiro, MAX)
            tempo = time.perf_counter() - inicio

            print(
                f"{profundidade:>5} | {agente.nome():<10} | {coluna + 1:>6} | "
                f"{agente.estados_ultima_jogada:>9} | {tempo:>6.2f}s"
            )
    print()


def contra_aleatorio(partidas=10, profundidade=4):
    """Joga partidas da IA (alternando quem começa) contra o agente aleatório."""
    vitorias = 0
    derrotas = 0
    empates = 0

    for i in range(partidas):
        ia = AgenteMinimax(profundidade=profundidade)
        aleatorio = AgenteAleatorio()

        # Em partidas pares a IA começa (joga de MAX); nas ímpares, o aleatório começa.
        if i % 2 == 0:
            vencedor = jogar_partida(ia, aleatorio, mostrar=False)
            lado_da_ia = MAX
        else:
            vencedor = jogar_partida(aleatorio, ia, mostrar=False)
            lado_da_ia = MIN

        if vencedor is None:
            empates += 1
        elif vencedor == lado_da_ia:
            vitorias += 1
        else:
            derrotas += 1

    print(f"IA Alfa-Beta (prof. {profundidade}) x Aleatório em {partidas} partidas:")
    print(f"  vitórias: {vitorias}  derrotas: {derrotas}  empates: {empates}")


if __name__ == "__main__":
    comparar_poda()
    contra_aleatorio()
