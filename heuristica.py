"""Função de avaliação heurística.

A busca Minimax tem um limite de profundidade: ela não consegue explorar o
jogo até o fim. Quando chega nesse limite em um estado que ainda não acabou,
ela precisa "chutar" quão bom é aquele tabuleiro. Esse chute é a heurística.

A avaliação é sempre do ponto de vista de MAX:
- valor positivo  -> o tabuleiro é bom para MAX
- valor negativo  -> o tabuleiro é bom para MIN
- zero            -> equilibrado

Os valores ficam bem abaixo de 1000 (a utilidade de uma vitória real), para
que a busca nunca prefira uma "boa posição" a uma vitória de verdade.
"""

from regras import DIRECOES, SEQUENCIA, dentro_do_tabuleiro
from tabuleiro import COLUNAS, LINHAS, MAX, MIN, VAZIO

# Pesos da heurística. Mudar esses números muda o "estilo" da IA.
PESO_TRES = 5    # 3 peças do mesmo jogador + 1 casa vazia na janela
PESO_DOIS = 2    # 2 peças do mesmo jogador + 2 casas vazias na janela
PESO_CENTRO = 3  # cada peça na coluna do meio


def listar_janelas():
    """Lista todas as "janelas" de 4 casas seguidas do tabuleiro.

    Uma janela é uma lista de 4 posições (linha, coluna) em linha reta.
    Se as 4 forem preenchidas pelo mesmo jogador, ele vence. Por isso,
    contar quantas peças cada jogador já tem em cada janela é uma boa
    medida de quem está mais perto de ganhar.
    """
    janelas = []
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            for passo_linha, passo_coluna in DIRECOES:
                janela = []
                for i in range(SEQUENCIA):
                    janela.append((linha + i * passo_linha, coluna + i * passo_coluna))

                # A janela só vale se a última casa ainda está dentro do tabuleiro.
                ultima_linha, ultima_coluna = janela[-1]
                if dentro_do_tabuleiro(ultima_linha, ultima_coluna):
                    janelas.append(janela)
    return janelas


# As janelas são sempre as mesmas (dependem só do tamanho do tabuleiro),
# então calculamos a lista uma única vez quando o módulo é carregado.
JANELAS = listar_janelas()


def pontuar_janela(casas):
    """Pontua uma janela a partir dos 4 valores das suas casas."""
    qtd_max = casas.count(MAX)
    qtd_min = casas.count(MIN)
    qtd_vazias = casas.count(VAZIO)

    # Se os dois jogadores têm peças na janela, ninguém pode mais vencer por ela.
    if qtd_max > 0 and qtd_min > 0:
        return 0

    # Janelas boas para MAX (pontos positivos).
    if qtd_max == 3 and qtd_vazias == 1:
        return PESO_TRES
    if qtd_max == 2 and qtd_vazias == 2:
        return PESO_DOIS

    # Janelas boas para MIN (pontos negativos).
    if qtd_min == 3 and qtd_vazias == 1:
        return -PESO_TRES
    if qtd_min == 2 and qtd_vazias == 2:
        return -PESO_DOIS

    return 0


def pontuar_centro(tabuleiro):
    """Peças na coluna central participam de mais alinhamentos possíveis."""
    centro = COLUNAS // 2  # coluna de índice 3
    pontos = 0
    for linha in tabuleiro:
        if linha[centro] == MAX:
            pontos += PESO_CENTRO
        elif linha[centro] == MIN:
            pontos -= PESO_CENTRO
    return pontos


def avaliar(tabuleiro):
    """Estima o valor de um tabuleiro que ainda não terminou."""
    pontos = pontuar_centro(tabuleiro)

    for janela in JANELAS:
        casas = [tabuleiro[linha][coluna] for linha, coluna in janela]
        pontos += pontuar_janela(casas)

    return pontos
