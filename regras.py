# Regras do Lig 4: vitória, fim de jogo e função de utilidade.

from tabuleiro import COLUNAS, LINHAS, MAX, MIN, colunas_validas

SEQUENCIA = 4

# utilidade do ponto de vista de MAX
VITORIA_MAX = 1000
VITORIA_MIN = -1000
EMPATE = 0

# (passo na linha, passo na coluna)
DIRECOES = [
    (0, 1),   # horizontal
    (1, 0),   # vertical
    (1, 1),   # diagonal descendo
    (-1, 1),  # diagonal subindo
]


def dentro_do_tabuleiro(linha, coluna):
    return 0 <= linha < LINHAS and 0 <= coluna < COLUNAS


# Verifica se há 4 peças do jogador a partir de (linha, coluna) na direção dada.
def ha_sequencia(tabuleiro, linha, coluna, direcao, jogador):
    passo_linha, passo_coluna = direcao
    for i in range(SEQUENCIA):
        l = linha + i * passo_linha
        c = coluna + i * passo_coluna
        if not dentro_do_tabuleiro(l, c):
            return False
        if tabuleiro[l][c] != jogador:
            return False
    return True


# Testa cada casa como início de sequência nas 4 direções.
def venceu(tabuleiro, jogador):
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            for direcao in DIRECOES:
                if ha_sequencia(tabuleiro, linha, coluna, direcao, jogador):
                    return True
    return False


def tabuleiro_cheio(tabuleiro):
    return len(colunas_validas(tabuleiro)) == 0


def fim_de_jogo(tabuleiro):
    return venceu(tabuleiro, MAX) or venceu(tabuleiro, MIN) or tabuleiro_cheio(tabuleiro)


# +1000 se MAX venceu, -1000 se MIN venceu, 0 se empatou.
def utilidade(tabuleiro):
    if venceu(tabuleiro, MAX):
        return VITORIA_MAX
    if venceu(tabuleiro, MIN):
        return VITORIA_MIN
    return EMPATE
