import random

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


#Criação da matriz e alocação da posição inicial do robô coletor de lixo (representada por "A") e da posição final (representada por "X")
matriz = construir_matriz()
matriz[0][0] = "A"
matriz[19][19] = "X"

colocar_lixos(matriz)

mostrar_matriz(matriz)