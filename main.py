"""Ponto de entrada executável do Lig 4."""

import random

from connect import Connect

def main():
    jogo = Connect()

    def agente_humano(tabuleiro, jogador):
        while True:
            entrada = input(
                f"Sua vez ({jogo.SIMBOLOS[jogador]}). "
                f"Escolha uma coluna (1-{jogo.COLUNAS}): "
            ).strip()
            try:
                coluna = int(entrada) - 1
            except ValueError:
                print("Digite um número de coluna entre 1 e 7.")
                continue

            if coluna not in jogo.acoes(tabuleiro):
                print("Essa coluna é inválida ou está cheia. Tente outra.")
                continue
            return coluna

    def agente_aleatorio(tabuleiro, jogador):
        return random.choice(jogo.acoes(tabuleiro))

    print("=== LIG 4 ===")
    print("Você joga com X e começa. O computador joga com O.")
    
    jogo.run(agente_humano, agente_aleatorio)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPartida encerrada.")
