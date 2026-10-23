"""Ponto de entrada executável do Lig 4."""

from agentes import AgenteAleatorio, AgenteHumano, AgenteMinimax
from connect import Connect


def ler_opcao(mensagem, opcoes):
    """Lê do teclado até o usuário digitar uma das opções permitidas."""
    while True:
        entrada = input(mensagem).strip()
        if entrada in opcoes:
            return entrada
        print(f"Opção inválida. Escolha entre: {', '.join(opcoes)}.")


def main():
    jogo = Connect()

    print("=== LIG 4 ===")
    print("1 - Humano (X) x IA Alfa-Beta (O)")
    print("2 - IA Alfa-Beta (X) x Humano (O)")
    print("3 - IA Alfa-Beta (X) x IA Alfa-Beta (O)")
    print("4 - IA Alfa-Beta (X) x Aleatório (O)")
    modo = ler_opcao("Escolha o modo: ", ["1", "2", "3", "4"])

    # Profundidade da busca: quanto maior, mais forte e mais lenta a IA.
    print("\nDificuldade: 1 - Fácil (prof. 2)  2 - Médio (prof. 4)  3 - Difícil (prof. 6)")
    dificuldade = ler_opcao("Escolha a dificuldade: ", ["1", "2", "3"])
    profundidade = {"1": 2, "2": 4, "3": 6}[dificuldade]

    humano = AgenteHumano(jogo)
    ia = AgenteMinimax(jogo, profundidade=profundidade, poda=True, verbose=True)

    # Monta os agentes de MAX (X, começa) e MIN (O) conforme o modo escolhido.
    if modo == "1":
        agente_x, agente_o = humano, ia
    elif modo == "2":
        agente_x, agente_o = ia, humano
    elif modo == "3":
        # Instâncias separadas para cada IA ter seu próprio contador de estados.
        agente_x = ia
        agente_o = AgenteMinimax(jogo, profundidade=profundidade, poda=True, verbose=True)
    else:
        agente_x, agente_o = ia, AgenteAleatorio(jogo)

    jogo.run(agente_x, agente_o)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPartida encerrada.")
