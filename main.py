"""Ponto de entrada executável do Lig 4."""

from agentes import AgenteHumano, AgenteMinimax
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
    print("1 - Humano (X) x Humano (O)")
    print("2 - Humano (X) x Agente (O)")
    print("3 - Agente (X) x Agente (O)")
    modo = ler_opcao("Escolha o modo: ", ["1", "2", "3"])

    # Monta os agentes de MAX (X, começa) e MIN (O) conforme o modo escolhido.
    if modo == "1":
        agente_x = AgenteHumano(jogo)
        agente_o = AgenteHumano(jogo)
    elif modo == "2":
        agente_x = AgenteHumano(jogo)
        agente_o = AgenteMinimax(jogo, poda=True, verbose=True)
    else:
        # Instâncias separadas para cada IA ter seu próprio contador de estados.
        agente_x = AgenteMinimax(jogo, poda=True, verbose=True)
        agente_o = AgenteMinimax(jogo, poda=True, verbose=True)

    jogo.run(agente_x, agente_o)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nPartida encerrada.")
