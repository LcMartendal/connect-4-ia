"""Agentes que jogam o Lig 4.

Todo agente tem um método escolher_jogada(tabuleiro, jogador) que devolve
o índice da coluna escolhida (0 a 6). É isso que partida.py espera.

Existem três agentes:
- AgenteHumano:    pergunta a jogada pelo teclado.
- AgenteAleatorio: escolhe uma coluna válida ao acaso (adversário de referência).
- AgenteMinimax:   usa a busca de busca.py (Minimax puro ou com poda Alfa-Beta).
"""

import random
import time

from busca import Contador, escolher_melhor_coluna
from tabuleiro import COLUNAS, SIMBOLOS, colunas_validas


class AgenteHumano:
    """Pede a jogada pelo teclado e só aceita colunas válidas."""

    def escolher_jogada(self, tabuleiro, jogador):
        while True:
            entrada = input(
                f"Sua vez ({SIMBOLOS[jogador]}). Escolha uma coluna (1-{COLUNAS}): "
            ).strip()

            try:
                coluna = int(entrada) - 1  # o usuário digita 1-7, internamente usamos 0-6
            except ValueError:
                print(f"Digite um número de coluna entre 1 e {COLUNAS}.")
                continue

            if coluna not in colunas_validas(tabuleiro):
                print("Essa coluna é inválida ou está cheia. Tente outra.")
                continue

            return coluna


class AgenteAleatorio:
    """Escolhe qualquer coluna válida ao acaso."""

    def escolher_jogada(self, tabuleiro, jogador):
        return random.choice(colunas_validas(tabuleiro))


class AgenteMinimax:
    """Agente de busca competitiva com profundidade limitada.

    - usar_poda=True  -> Minimax com poda Alfa-Beta (algoritmo escolhido pelo grupo).
    - usar_poda=False -> Minimax puro (usado só para comparar o custo).
    """

    def __init__(self, profundidade=4, usar_poda=True, verbose=False):
        self.profundidade = profundidade
        self.usar_poda = usar_poda
        self.verbose = verbose  # se True, mostra estatísticas a cada jogada
        self.estados_ultima_jogada = 0
        self.estados_partida = 0

    def nome(self):
        if self.usar_poda:
            return "Alfa-Beta"
        return "Minimax"

    def escolher_jogada(self, tabuleiro, jogador):
        contador = Contador()
        inicio = time.perf_counter()

        coluna, valor = escolher_melhor_coluna(
            tabuleiro, jogador, self.profundidade, self.usar_poda, contador
        )

        tempo = time.perf_counter() - inicio
        self.estados_ultima_jogada = contador.estados
        self.estados_partida += contador.estados

        if self.verbose:
            print(
                f"[{self.nome()}] {contador.estados} estados avaliados em {tempo:.2f}s "
                f"(valor estimado: {valor})"
            )

        return coluna
