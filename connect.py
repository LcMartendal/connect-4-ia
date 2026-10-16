
from estrutura import criar_tabuleiro


class Connect:
    LINHAS = 6
    COLUNAS = 7
    VAZIO = 0
    MAX = 1
    MIN = 2
    SEQUENCIA = 4
    SIMBOLOS = {VAZIO: ".", MAX: "X", MIN: "O"}

    def __init__(self):
        self.tabuleiro = criar_tabuleiro(self)
        self.jogador_atual = self.MAX

    def outro_jogador(self, jogador):
        return self.MIN if jogador == self.MAX else self.MAX

    def acoes(self, tabuleiro=None):
        """Colunas válidas no estado informado (ou no estado atual)."""
        tabuleiro = self.tabuleiro if tabuleiro is None else tabuleiro
        return [c for c in range(self.COLUNAS) if tabuleiro[0][c] == self.VAZIO]

    def resultado(self, tabuleiro, coluna, jogador):
        """Retorna uma cópia do estado após a jogada, sem alterar o argumento."""
        if coluna not in self.acoes(tabuleiro):
            raise ValueError(f"Jogada inválida: coluna {coluna} cheia ou inexistente.")
        novo = [linha[:] for linha in tabuleiro]
        for linha in range(self.LINHAS - 1, -1, -1):
            if novo[linha][coluna] == self.VAZIO:
                novo[linha][coluna] = jogador
                break
        return novo

    def venceu(self, tabuleiro, jogador):
        """Verifica alinhamentos horizontais, verticais e diagonais."""
        for linha in range(self.LINHAS):
            for coluna in range(self.COLUNAS):
                if tabuleiro[linha][coluna] != jogador:
                    continue
                for dl, dc in ((0, 1), (1, 0), (1, 1), (-1, 1)):
                    if all(
                        0 <= linha + passo * dl < self.LINHAS
                        and 0 <= coluna + passo * dc < self.COLUNAS
                        and tabuleiro[linha + passo * dl][coluna + passo * dc] == jogador
                        for passo in range(self.SEQUENCIA)
                    ):
                        return True
        return False

    def tabuleiro_cheio(self, tabuleiro=None):
        return not self.acoes(tabuleiro)

    def fim_jogo(self, tabuleiro=None):
        tabuleiro = self.tabuleiro if tabuleiro is None else tabuleiro
        return (
            self.venceu(tabuleiro, self.MAX)
            or self.venceu(tabuleiro, self.MIN)
            or self.tabuleiro_cheio(tabuleiro)
        )

    def utilidade(self, tabuleiro=None):
        tabuleiro = self.tabuleiro if tabuleiro is None else tabuleiro
        if self.venceu(tabuleiro, self.MAX):
            return 1000
        if self.venceu(tabuleiro, self.MIN):
            return -1000
        return 0

    def imprimir_tabuleiro(self, tabuleiro=None):
        tabuleiro = self.tabuleiro if tabuleiro is None else tabuleiro
        print()
        for linha in tabuleiro:
            print("| " + " ".join(self.SIMBOLOS[casa] for casa in linha) + " |")
        print("+" + "-" * (self.COLUNAS * 2 + 1) + "+")
        print("  " + " ".join(str(c+1) for c in range(self.COLUNAS)))
        print()

    def run(self, agente1, agente2, mostrar=True):
        """Executa uma partida alternando agentes; agentes recebem (estado, jogador) e retornam coluna."""
        agentes = {self.MAX: agente1, self.MIN: agente2}
        rodada = 1
        if mostrar:
            self.imprimir_tabuleiro()

        while not self.fim_jogo():
            jogador = self.jogador_atual
            coluna = agentes[jogador](self.tabuleiro, jogador)
            self.tabuleiro = self.resultado(self.tabuleiro, coluna, jogador)
            if mostrar:
                print(f"Rodada {rodada}: Agente {jogador} ({self.SIMBOLOS[jogador]}) jogou na coluna {coluna}")
                self.imprimir_tabuleiro()
            self.jogador_atual = self.outro_jogador(jogador)
            rodada += 1

        utilidade = self.utilidade()
        vencedor = self.MAX if utilidade > 0 else self.MIN if utilidade < 0 else None
        if mostrar:
            if vencedor is None:
                print("Fim de jogo: EMPATE!")
            else:
                print(f"Fim de jogo: Agente {vencedor} ({self.SIMBOLOS[vencedor]}) VENCEU!")
        return vencedor
