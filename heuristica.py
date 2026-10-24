# Heurística usada quando a busca para antes do fim do jogo. Positivo favorece
# MAX e negativo favorece MIN, sempre bem abaixo da utilidade de vitória (1000).

from regras import DIRECOES, SEQUENCIA, dentro_do_tabuleiro
from tabuleiro import COLUNAS, LINHAS, MAX, MIN, VAZIO

PESO_TRES = 5    # 3 peças + 1 vazia
PESO_DOIS = 2    # 2 peças + 2 vazias
PESO_CENTRO = 3  # por peça na coluna central


# Todas as sequências de 4 casas em linha reta do tabuleiro.
def listar_janelas():
    janelas = []
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            for passo_linha, passo_coluna in DIRECOES:
                janela = []
                for i in range(SEQUENCIA):
                    janela.append((linha + i * passo_linha, coluna + i * passo_coluna))

                # descarta janelas que saem do tabuleiro
                ultima_linha, ultima_coluna = janela[-1]
                if dentro_do_tabuleiro(ultima_linha, ultima_coluna):
                    janelas.append(janela)
    return janelas


# só depende do tamanho do tabuleiro, então é calculado uma vez
JANELAS = listar_janelas()


# Pontos de uma janela a partir dos valores das 4 casas.
def pontuar_janela(casas):
    qtd_max = casas.count(MAX)
    qtd_min = casas.count(MIN)
    qtd_vazias = casas.count(VAZIO)

    # com peças dos dois jogadores ninguém vence por essa janela
    if qtd_max > 0 and qtd_min > 0:
        return 0

    if qtd_max == 3 and qtd_vazias == 1:
        return PESO_TRES
    if qtd_max == 2 and qtd_vazias == 2:
        return PESO_DOIS

    if qtd_min == 3 and qtd_vazias == 1:
        return -PESO_TRES
    if qtd_min == 2 and qtd_vazias == 2:
        return -PESO_DOIS

    return 0


# Bônus por peças na coluna central, que participa de mais alinhamentos.
def pontuar_centro(tabuleiro):
    centro = COLUNAS // 2
    pontos = 0
    for linha in tabuleiro:
        if linha[centro] == MAX:
            pontos += PESO_CENTRO
        elif linha[centro] == MIN:
            pontos -= PESO_CENTRO
    return pontos


# Estima o valor de um tabuleiro que ainda não terminou.
def avaliar(tabuleiro):
    pontos = pontuar_centro(tabuleiro)

    for janela in JANELAS:
        casas = [tabuleiro[linha][coluna] for linha, coluna in janela]
        pontos += pontuar_janela(casas)

    return pontos
