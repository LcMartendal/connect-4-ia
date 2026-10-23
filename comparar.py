"""Experimentos para a reflexão sobre o algoritmo escolhido.

1. Compara Minimax puro e Minimax com poda Alfa-Beta na mesma posição
   (mesma jogada escolhida, número de estados visitados e tempo).
2. Joga partidas da IA Alfa-Beta contra o agente aleatório.

Uso: python comparar.py
"""

import time

from agentes import AgenteAleatorio, AgenteMinimax
from connect import Connect


def comparar_poda(profundidades=(2, 3, 4, 5)):
    """Mede o custo da primeira jogada com e sem poda, para várias profundidades."""
    jogo = Connect()
    print("Primeira jogada (tabuleiro vazio), MAX a jogar")
    print(f"{'prof.':>5} | {'algoritmo':<10} | {'coluna':>6} | {'estados':>9} | {'tempo':>7}")
    print("-" * 50)
    for profundidade in profundidades:
        for poda in (False, True):
            agente = AgenteMinimax(jogo, profundidade=profundidade, poda=poda)
            inicio = time.perf_counter()
            coluna = agente(jogo.tabuleiro, jogo.MAX)
            tempo = time.perf_counter() - inicio
            nome = "Alfa-Beta" if poda else "Minimax"
            print(
                f"{profundidade:>5} | {nome:<10} | {coluna + 1:>6} | "
                f"{agente.nos_visitados:>9} | {tempo:>6.2f}s"
            )
    print()


def contra_aleatorio(partidas=10, profundidade=4):
    """Joga partidas da IA (alternando quem começa) contra o agente aleatório."""
    vitorias = derrotas = empates = 0
    for i in range(partidas):
        jogo = Connect()
        ia = AgenteMinimax(jogo, profundidade=profundidade)
        aleatorio = AgenteAleatorio(jogo)
        ia_comeca = i % 2 == 0
        if ia_comeca:
            vencedor = jogo.run(ia, aleatorio, mostrar=False)
            simbolo_ia = jogo.MAX
        else:
            vencedor = jogo.run(aleatorio, ia, mostrar=False)
            simbolo_ia = jogo.MIN

        if vencedor is None:
            empates += 1
        elif vencedor == simbolo_ia:
            vitorias += 1
        else:
            derrotas += 1
    print(f"IA Alfa-Beta (prof. {profundidade}) x Aleatório em {partidas} partidas:")
    print(f"  vitórias: {vitorias}  derrotas: {derrotas}  empates: {empates}")


if __name__ == "__main__":
    comparar_poda()
    contra_aleatorio()
