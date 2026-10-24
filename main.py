"""
# Lig 4 (Connect 4)

## Participantes

- Cauã Fernando Bertolini
- Eduarda Dagnoni Mazureck
- Fabian Formento
- Lucas Visconti
- Luiz Carlos Martendal

## Como executar

```bash
python main.py
```

No menu é possível escolher o modo de jogo (humano x IA, IA x humano, IA x IA ou IA x aleatório) e a dificuldade (profundidade 2, 4 ou 6 da busca).

## Estrutura do código

Cada módulo corresponde a um conceito da formulação do jogo. A ordem abaixo é uma boa ordem de leitura:

| Módulo | O que faz |
|---|---|
| `tabuleiro.py` | Representação do estado (matriz 6x7), estado inicial, ações válidas e função de transição (`jogar`). |
| `regras.py` | Teste de estado terminal (`fim_de_jogo`), verificação de vitória e função de utilidade (+1000 / −1000 / 0). |
| `heuristica.py` | Função de avaliação usada quando a busca chega no limite de profundidade. |
| `busca.py` | Os algoritmos: `minimax` (puro) e `alfa_beta` (com poda). A IA usa o Alfa-Beta. |
| `agentes.py` | Quem joga: humano, aleatório e IA (que chama a busca). |
| `partida.py` | Loop da partida: alterna os agentes até o fim do jogo. |
| `main.py` | Menu de modo e dificuldade. |

## Parte 1: Definição e formulação do jogo

**Jogo escolhido:** Lig 4. O tabuleiro tem 6 linhas e 7 colunas. Na sua vez, o jogador solta uma peça em uma coluna e ela cai até a posição livre mais baixa. Vence quem alinhar 4 peças na horizontal, na vertical ou na diagonal.

**Estado inicial:** o jogo começa com o tabuleiro vazio. Ele é representado por uma matriz 6x7, onde `0` = vazio, `1` = peça de MAX e `2` = peça de MIN.

**Jogadores:** 2 jogadores. MAX joga com `X` e começa; MIN joga com `O`. No modo padrão, MAX é o humano e MIN é o computador.

**Ações possíveis:** escolher uma coluna de 1 a 7. Não é possível jogar em uma coluna cheia.

**Função de transição:** a peça vai para a linha vazia mais baixa da coluna escolhida, e a vez passa para o outro jogador.

**Estado terminal:** o jogo termina quando um jogador alinha 4 peças (vitória dele, derrota do outro) ou quando o tabuleiro enche sem vencedor (empate).

**Função de utilidade:** vitória de MAX = +1000, vitória de MIN = −1000, empate = 0.

**Tipo de jogo:** determinístico, porque não existe sorte. A mesma jogada sempre gera o mesmo resultado.
"""


# Menu do Lig 4.
# Uso: python main.py

from agentes import AgenteAleatorio, AgenteHumano, AgenteMinimax
from partida import jogar_partida


# Repete a pergunta até receber uma opção válida.
def ler_opcao(mensagem, opcoes):
    while True:
        entrada = input(mensagem).strip()
        if entrada in opcoes:
            return entrada
        print(f"Opção inválida. Escolha entre: {', '.join(opcoes)}.")


def main():
    print("=== LIG 4 ===")
    print("1 - Humano (X) x IA Alfa-Beta (O)")
    print("2 - IA Alfa-Beta (X) x Humano (O)")
    print("3 - IA Alfa-Beta (X) x IA Alfa-Beta (O)")
    print("4 - IA Alfa-Beta (X) x Aleatório (O)")
    modo = ler_opcao("Escolha o modo: ", ["1", "2", "3", "4"])

    print("\nDificuldade: 1 - Fácil (prof. 2)  2 - Médio (prof. 4)  3 - Difícil (prof. 6)")
    dificuldade = ler_opcao("Escolha a dificuldade: ", ["1", "2", "3"])
    profundidade = {"1": 2, "2": 4, "3": 6}[dificuldade]

    def nova_ia():
        return AgenteMinimax(profundidade=profundidade, usar_poda=True, verbose=True)

    # MAX joga com X e começa
    if modo == "1":
        agente_max = AgenteHumano()
        agente_min = nova_ia()
    elif modo == "2":
        agente_max = nova_ia()
        agente_min = AgenteHumano()
    elif modo == "3":
        agente_max = nova_ia()
        agente_min = nova_ia()
    else:
        agente_max = nova_ia()
        agente_min = AgenteAleatorio()

    jogar_partida(agente_max, agente_min)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPartida encerrada.")
