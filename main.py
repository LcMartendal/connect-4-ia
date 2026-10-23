"""Ponto de entrada do Lig 4: mostra o menu e inicia a partida.

Uso: python main.py
"""

from agentes import AgenteAleatorio, AgenteHumano, AgenteMinimax
from partida import jogar_partida


def ler_opcao(mensagem, opcoes):
    """Lê do teclado até o usuário digitar uma das opções permitidas."""
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

    # Profundidade da busca: quanto maior, mais forte e mais lenta a IA.
    print("\nDificuldade: 1 - Fácil (prof. 2)  2 - Médio (prof. 4)  3 - Difícil (prof. 6)")
    dificuldade = ler_opcao("Escolha a dificuldade: ", ["1", "2", "3"])
    profundidade = {"1": 2, "2": 4, "3": 6}[dificuldade]

    def nova_ia():
        return AgenteMinimax(profundidade=profundidade, usar_poda=True, verbose=True)

    # Monta quem joga de MAX (X, começa) e quem joga de MIN (O).
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
