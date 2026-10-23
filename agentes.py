"""Agentes que jogam o Lig 4.

Todo agente é "chamável" com a assinatura (tabuleiro, jogador) e retorna o
índice da coluna escolhida (0 a 6), que é o formato esperado por Connect.run.
"""

import math
import random
import time


class AgenteHumano:
    """Pede a jogada pelo teclado e só aceita colunas válidas."""

    def __init__(self, jogo):
        self.jogo = jogo

    def __call__(self, tabuleiro, jogador):
        while True:
            entrada = input(
                f"Sua vez ({self.jogo.SIMBOLOS[jogador]}). "
                f"Escolha uma coluna (1-{self.jogo.COLUNAS}): "
            ).strip()
            try:
                coluna = int(entrada) - 1  # o usuário digita 1-7, internamente usamos 0-6
            except ValueError:
                print(f"Digite um número de coluna entre 1 e {self.jogo.COLUNAS}.")
                continue

            if coluna not in self.jogo.acoes(tabuleiro):
                print("Essa coluna é inválida ou está cheia. Tente outra.")
                continue
            return coluna


class AgenteAleatorio:
    """Escolhe qualquer coluna válida ao acaso (serve de adversário de referência)."""

    def __init__(self, jogo):
        self.jogo = jogo

    def __call__(self, tabuleiro, jogador):
        return random.choice(self.jogo.acoes(tabuleiro))


class AgenteMinimax:
    """Agente de busca competitiva baseado no Minimax com profundidade limitada.

    - poda=True  -> Minimax com poda Alfa-Beta (algoritmo escolhido pelo grupo).
    - poda=False -> Minimax puro (usado para comparar o número de estados visitados).

    MAX tenta deixar a utilidade a maior possível e MIN a menor possível,
    seguindo a função de utilidade definida em Connect.utilidade (+1000 / -1000 / 0).
    """

    # Pesos da função de avaliação heurística (usada quando a busca é cortada).
    PESO_TRES = 5     # 3 peças do mesmo jogador + 1 casa vazia na janela
    PESO_DOIS = 2     # 2 peças do mesmo jogador + 2 casas vazias na janela
    PESO_CENTRO = 3   # cada peça na coluna central

    def __init__(self, jogo, profundidade=5, poda=True, verbose=False):
        self.jogo = jogo
        self.profundidade = profundidade
        self.poda = poda
        self.verbose = verbose
        self.nos_visitados = 0  # estados visitados na última jogada
        self.nos_total = 0      # estados visitados na partida inteira

        # Ordem de teste das colunas: do centro para as bordas.
        # Colunas centrais costumam ser melhores, então a poda corta mais cedo.
        centro = jogo.COLUNAS // 2
        self.ordem_colunas = sorted(range(jogo.COLUNAS), key=lambda c: abs(c - centro))

        # Pré-calcula todas as "janelas" de 4 casas seguidas do tabuleiro
        # (horizontais, verticais e diagonais) para não recalcular a cada avaliação.
        self.janelas = []
        n = jogo.SEQUENCIA
        for linha in range(jogo.LINHAS):
            for coluna in range(jogo.COLUNAS):
                for dl, dc in ((0, 1), (1, 0), (1, 1), (-1, 1)):
                    fim_l = linha + (n - 1) * dl
                    fim_c = coluna + (n - 1) * dc
                    if 0 <= fim_l < jogo.LINHAS and 0 <= fim_c < jogo.COLUNAS:
                        self.janelas.append(
                            [(linha + i * dl, coluna + i * dc) for i in range(n)]
                        )

    def __call__(self, tabuleiro, jogador):
        """Escolhe a melhor coluna para o jogador informado."""
        self.nos_visitados = 0
        inicio = time.perf_counter()

        maximizando = jogador == self.jogo.MAX
        melhor_valor = -math.inf if maximizando else math.inf
        melhor_coluna = None
        alfa, beta = -math.inf, math.inf

        # Testa cada jogada possível e simula a resposta do adversário com o Minimax.
        for coluna in self._acoes_ordenadas(tabuleiro):
            filho = self.jogo.resultado(tabuleiro, coluna, jogador)
            valor = self.minimax(
                filho, self.profundidade - 1, alfa, beta, self.jogo.outro_jogador(jogador)
            )

            if maximizando and valor > melhor_valor:
                melhor_valor, melhor_coluna = valor, coluna
            elif not maximizando and valor < melhor_valor:
                melhor_valor, melhor_coluna = valor, coluna

            # Atualiza a janela alfa-beta também na raiz.
            if self.poda:
                if maximizando:
                    alfa = max(alfa, melhor_valor)
                else:
                    beta = min(beta, melhor_valor)

        self.nos_total += self.nos_visitados
        if self.verbose:
            tempo = time.perf_counter() - inicio
            nome = "Alfa-Beta" if self.poda else "Minimax"
            print(
                f"[{nome}] {self.nos_visitados} estados avaliados em {tempo:.2f}s "
                f"(valor estimado: {melhor_valor})"
            )
        return melhor_coluna

    def minimax(self, tabuleiro, profundidade, alfa, beta, jogador):
        """Retorna o valor do estado considerando que ambos jogam da melhor forma.

        profundidade: quantas jogadas ainda podem ser exploradas.
        alfa: melhor valor já garantido para MAX no caminho até aqui.
        beta: melhor valor já garantido para MIN no caminho até aqui.
        jogador: quem joga neste estado.
        """
        self.nos_visitados += 1

        # Estado terminal: usa a função de utilidade do jogo.
        if self.jogo.fim_jogo(tabuleiro):
            utilidade = self.jogo.utilidade(tabuleiro)
            # Soma a profundidade restante para preferir vitórias mais rápidas
            # (e derrotas mais demoradas, dando mais chance do adversário errar).
            if utilidade > 0:
                return utilidade + profundidade
            if utilidade < 0:
                return utilidade - profundidade
            return 0

        # Limite de profundidade: estima o valor com a heurística.
        if profundidade == 0:
            return self.avaliar(tabuleiro)

        proximo = self.jogo.outro_jogador(jogador)

        if jogador == self.jogo.MAX:
            valor = -math.inf
            for coluna in self._acoes_ordenadas(tabuleiro):
                filho = self.jogo.resultado(tabuleiro, coluna, jogador)
                valor = max(valor, self.minimax(filho, profundidade - 1, alfa, beta, proximo))
                if self.poda:
                    alfa = max(alfa, valor)
                    if alfa >= beta:  # MIN nunca deixaria chegar aqui: corta o resto
                        break
            return valor

        valor = math.inf
        for coluna in self._acoes_ordenadas(tabuleiro):
            filho = self.jogo.resultado(tabuleiro, coluna, jogador)
            valor = min(valor, self.minimax(filho, profundidade - 1, alfa, beta, proximo))
            if self.poda:
                beta = min(beta, valor)
                if alfa >= beta:  # MAX nunca deixaria chegar aqui: corta o resto
                    break
        return valor

    def avaliar(self, tabuleiro):
        """Função de avaliação heurística (ponto de vista de MAX).

        Valores positivos favorecem MAX e negativos favorecem MIN.
        Fica sempre bem abaixo de 1000, para nunca superar uma vitória real.
        """
        pontos = 0

        # Peças no centro participam de mais alinhamentos possíveis.
        centro = self.jogo.COLUNAS // 2
        for linha in tabuleiro:
            if linha[centro] == self.jogo.MAX:
                pontos += self.PESO_CENTRO
            elif linha[centro] == self.jogo.MIN:
                pontos -= self.PESO_CENTRO

        # Pontua cada janela de 4 casas que ainda pode virar uma vitória.
        for janela in self.janelas:
            casas = [tabuleiro[l][c] for l, c in janela]
            pontos += self._pontuar_janela(casas)

        return pontos

    def _pontuar_janela(self, casas):
        """Pontua uma janela de 4 casas."""
        qtd_max = casas.count(self.jogo.MAX)
        qtd_min = casas.count(self.jogo.MIN)
        vazias = casas.count(self.jogo.VAZIO)

        # Janela com peças dos dois jogadores não serve para ninguém.
        if qtd_max and qtd_min:
            return 0
        if qtd_max == 3 and vazias == 1:
            return self.PESO_TRES
        if qtd_max == 2 and vazias == 2:
            return self.PESO_DOIS
        if qtd_min == 3 and vazias == 1:
            return -self.PESO_TRES
        if qtd_min == 2 and vazias == 2:
            return -self.PESO_DOIS
        return 0

    def _acoes_ordenadas(self, tabuleiro):
        """Ações válidas na ordem centro -> bordas."""
        validas = self.jogo.acoes(tabuleiro)
        return [c for c in self.ordem_colunas if c in validas]
