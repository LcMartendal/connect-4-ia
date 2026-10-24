# Agentes do Lig 4. Todos implementam escolher_jogada(tabuleiro, jogador),
# que devolve a coluna escolhida (0 a 6).

import random
import time

from busca import Contador, escolher_melhor_coluna
from tabuleiro import COLUNAS, SIMBOLOS, colunas_validas


# Lê a jogada do teclado.
class AgenteHumano:
    def escolher_jogada(self, tabuleiro, jogador):
        while True:
            entrada = input(
                f"Sua vez ({SIMBOLOS[jogador]}). Escolha uma coluna (1-{COLUNAS}): "
            ).strip()

            try:
                coluna = int(entrada) - 1  # usuário digita de 1 a 7
            except ValueError:
                print(f"Digite um número de coluna entre 1 e {COLUNAS}.")
                continue

            if coluna not in colunas_validas(tabuleiro):
                print("Essa coluna é inválida ou está cheia. Tente outra.")
                continue

            return coluna


# Joga em qualquer coluna válida.
class AgenteAleatorio:
    def escolher_jogada(self, tabuleiro, jogador):
        return random.choice(colunas_validas(tabuleiro))


# Minimax com profundidade limitada; usar_poda liga o Alfa-Beta.
class AgenteMinimax:
    def __init__(self, profundidade=4, usar_poda=True, verbose=False):
        self.profundidade = profundidade
        self.usar_poda = usar_poda
        self.verbose = verbose  # imprime estatísticas a cada jogada
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
