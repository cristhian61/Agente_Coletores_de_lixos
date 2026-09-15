import random


#================================== Criação do ambiente ==================================
#Função para construir a matriz 20x20 com todas as posições livres (representadas por ".")
def construir_matriz():
    matriz = []

    for i in range(20):
        linha = []

        for j in range(20):
            linha.append(".")

        matriz.append(linha)

    return matriz

#Função para exibir a matriz formatada no terminal
def mostrar_matriz(matriz):
    for linha in matriz:
        print(" ".join(linha))

#Função para verificar se a célula na matriz está livre (representada por ".")
def posicao_livre(matriz, linha, coluna):
    return matriz[linha][coluna] == "."

#Função para posicionar os lixos de forma aleatódia na matriz
def colocar_lixos(matriz):

    #Organicos (representados por "O")
    for i in range(10):
        while True:
            linha = random.randint(0, 19)
            coluna = random.randint(0, 19)

            if posicao_livre(matriz, linha, coluna):
                break
        matriz[linha][coluna] = "O" #Lixos Organicos

    #Recicláveis (representados por "R")
    for i in range(5):
        while True:
            linha = random.randint(0, 19)
            coluna = random.randint(0, 19)

            if posicao_livre(matriz, linha, coluna):
                break
        matriz[linha][coluna] = "R" #Lixos Recicláveis


#================================== Agente ==================================

#Criação e movimentação do agente n matriz
class Agente:
    def __init__(self):
        self.linha = 0
        self.coluna = 0
        self.carga = None
        self.pontuacao = 0

#Os IFs dentro das funções de movimentação garantem que o agente não saia dos limites da matriz (0 a 19 para linhas e colunas).
    def mover_direita(self):
        if self.coluna < 19:
            self.coluna += 1

    def mover_esquerda(self):
        if self.coluna > 0:
            self.coluna -= 1

    def mover_cima(self):
        if self.linha > 0:
            self.linha -= 1

    def mover_baixo(self):
        if self.linha < 19:
            self.linha += 1

#Função para observar a posição atual do agente na matriz, retornando o valor da célula correspondente.
    def observar_posicao(self, matriz):
        return matriz[self.linha][self.coluna]

#Função para observar as posições vizinhas do agente na matriz, retornando um dicionário com os valores das células correspondentes.
    def observar_posicoes_vizinhas(self, matriz):
        direcoes = {
            "cima_esquerda": (-1,-1),
            "cima": (-1,0),
            "cima_direita": (-1,1),
            "esquerda": (0,-1),
            "direita": (0,1),
            "baixo_esquerda": (1,-1),
            "baixo": (1,0),
            "baixo_direita": (1,1)
        }

        percepcoes = {}

        for nome, (dl, dc) in direcoes.items(): # dl = deslocamento linha, dc = deslocamento coluna
            nova_linha = self.linha + dl
            nova_coluna = self.coluna + dc

            if 0 <= nova_linha < 20 and 0 <= nova_coluna < 20:
                percepcoes[nome] = matriz[nova_linha][nova_coluna]

        return percepcoes

#Função para o agente pegar o lixo na posição atual da matriz, se houver algum. O agente só pode pegar um lixo se não estiver carregando nenhum (carga é None). Se houver lixo orgânico ("O") ou reciclável ("R") na posição atual, o agente pega o lixo, atualiza a carga e remove o lixo da matriz (substituindo por "."). Retorna True se o lixo foi pego com sucesso, caso contrário retorna False.
    def pegar_lixo(self, matriz):

        if self.carga is not None:
            return False  # O agente já está carregando um lixo

        if matriz[self.linha][self.coluna] == "O":
            self.carga = "O"
            matriz[self.linha][self.coluna] = "."
            return True

        if matriz[self.linha][self.coluna] == "R":
            self.carga = "R"
            matriz[self.linha][self.coluna] = "."
            return True

        return False  # Não há lixo para pegar

    def soltar_lixo(self, matriz):

        if self.linha == 19 and self.coluna == 19:
            if self.carga is not None:

                if self.carga == "O":
                    self.pontuacao += 1  # Pontuação para lixo orgânico
                elif self.carga == "R":
                    self.pontuacao += 5  # Pontuação para lixo reciclável

                self.carga = None
                return True  # Lixo solto com sucesso

        return False  # Não é possível soltar lixo fora da posição final

#teste
#Criação da matriz e alocação da posição inicial do robô coletor de lixo (representada por "A") e da posição final (representada por "X")
matriz = construir_matriz()
matriz[0][0] = "A"
matriz[19][19] = "X"

colocar_lixos(matriz)

mostrar_matriz(matriz)