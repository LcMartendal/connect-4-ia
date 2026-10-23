"""Regras do Lig 4: quem venceu, quando o jogo acaba e a função de utilidade.

Este módulo responde às perguntas da formulação do jogo:
- Teste de estado terminal: fim_de_jogo(tabuleiro)
- Função de utilidade:      utilidade(tabuleiro)
"""

from tabuleiro import COLUNAS, LINHAS, MAX, MIN, colunas_validas

# Quantas peças seguidas são necessárias para vencer.
SEQUENCIA = 4

# Valores da função de utilidade (sempre do ponto de vista de MAX).
VITORIA_MAX = 1000
VITORIA_MIN = -1000
EMPATE = 0

# As quatro direções em que 4 peças podem se alinhar.
# Cada direção é (passo na linha, passo na coluna).
DIRECOES = [
    (0, 1),   # horizontal: anda para a direita
    (1, 0),   # vertical:   anda para baixo
    (1, 1),   # diagonal:   anda para baixo e para a direita
    (-1, 1),  # diagonal:   anda para cima e para a direita
]


def dentro_do_tabuleiro(linha, coluna):
    """Diz se a posição (linha, coluna) existe no tabuleiro."""
    return 0 <= linha < LINHAS and 0 <= coluna < COLUNAS


def ha_sequencia(tabuleiro, linha, coluna, direcao, jogador):
    """Verifica se há 4 peças do jogador começando em (linha, coluna) e
    andando na direção informada.
    """
    passo_linha, passo_coluna = direcao
    for i in range(SEQUENCIA):
        l = linha + i * passo_linha
        c = coluna + i * passo_coluna
        if not dentro_do_tabuleiro(l, c):
            return False  # a sequência "sairia" do tabuleiro
        if tabuleiro[l][c] != jogador:
            return False  # encontrou uma casa que não é do jogador
    return True


def venceu(tabuleiro, jogador):
    """Diz se o jogador tem 4 peças alinhadas em qualquer lugar do tabuleiro.

    Testa cada casa como possível início de sequência, nas 4 direções.
    É mais trabalho do que o necessário, mas é fácil de entender.
    """
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            for direcao in DIRECOES:
                if ha_sequencia(tabuleiro, linha, coluna, direcao, jogador):
                    return True
    return False


def tabuleiro_cheio(tabuleiro):
    """Diz se não há mais nenhuma coluna onde jogar."""
    return len(colunas_validas(tabuleiro)) == 0


def fim_de_jogo(tabuleiro):
    """Teste de estado terminal: alguém venceu ou o tabuleiro encheu."""
    return venceu(tabuleiro, MAX) or venceu(tabuleiro, MIN) or tabuleiro_cheio(tabuleiro)


def utilidade(tabuleiro):
    """Função de utilidade de um estado terminal, do ponto de vista de MAX.

    +1000 se MAX venceu, -1000 se MIN venceu, 0 em caso de empate.
    MAX quer deixar esse valor o maior possível; MIN, o menor possível.
    """
    if venceu(tabuleiro, MAX):
        return VITORIA_MAX
    if venceu(tabuleiro, MIN):
        return VITORIA_MIN
    return EMPATE
