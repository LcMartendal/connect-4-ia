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

## Parte 1: Definição e formulação do jogo

**Jogo escolhido:** Lig 4. O tabuleiro tem 6 linhas e 7 colunas. Na sua vez, o jogador solta uma peça em uma coluna e ela cai até a posição livre mais baixa. Vence quem alinhar 4 peças na horizontal, na vertical ou na diagonal.

**Estado inicial:** o jogo começa com o tabuleiro vazio. Ele é representado por uma matriz 6x7, onde `0` = vazio, `1` = peça de MAX e `2` = peça de MIN.

**Jogadores:** 2 jogadores. MAX é o humano (`X`), que começa. MIN é o computador (`O`).

**Ações possíveis:** escolher uma coluna de 1 a 7. Não é possível jogar em uma coluna cheia.

**Função de transição:** a peça vai para a linha vazia mais baixa da coluna escolhida, e a vez passa para o outro jogador.

**Estado terminal:** o jogo termina quando um jogador alinha 4 peças (vitória dele, derrota do outro) ou quando o tabuleiro enche sem vencedor (empate).

**Função de utilidade:** vitória de MAX = +1000, vitória de MIN = −1000, empate = 0.

**Tipo de jogo:** determinístico, porque não existe sorte. A mesma jogada sempre gera o mesmo resultado.