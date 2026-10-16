def criar_tabuleiro(self):
    """Retorna um tabuleiro vazio de 6 por 7."""
    return [[self.VAZIO for _ in range(self.COLUNAS)] for _ in range(self.LINHAS)]