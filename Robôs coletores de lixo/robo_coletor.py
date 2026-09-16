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
        self.passos = 0

#Os IFs dentro das funções de movimentação garantem que o agente não saia dos limites da matriz (0 a 19 para linhas e colunas).
    def mover_direita(self):
        if self.coluna < 19:
            self.coluna += 1
            self.passos += 1

    def mover_esquerda(self):
        if self.coluna > 0:
            self.coluna -= 1
            self.passos += 1

    def mover_cima(self):
        if self.linha > 0:
            self.linha -= 1
            self.passos += 1
    
    def mover_baixo(self):
        if self.linha < 19:
            self.linha += 1
            self.passos += 1

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

        return False  # Não é possível soltar lixo fora da posição 

#Função para encontrar os lixos vizinhos do agente na matriz, retornando duas listas: uma com as direções dos lixos recicláveis ("R") e outra com as direções dos lixos orgânicos ("O").
    def encontar_lixo_vizinho(self, matriz):
        vizinhos = self.observar_posicoes_vizinhas(matriz)

        reciclaveis = []
        organicos = []

        for direcao, objeto in vizinhos.items():
            if objeto == "R":
                reciclaveis.append(direcao)
            elif objeto == "O":
                organicos.append(direcao)

        return reciclaveis, organicos

#Função para decidir a ação do agente com base na posição atual e nos lixos vizinhos. Se o agente não estiver carregando nenhum lixo e estiver em uma posição com lixo orgânico ("O") ou reciclável ("R"), ele decide pegar o lixo. Caso contrário, ele verifica os lixos vizinhos e escolhe aleatoriamente uma direção para se mover em direção a um lixo reciclável ou orgânico, se houver algum.
    def decidir_acao(self, matriz):
        posicao = self.observar_posicao(matriz)

        #Pegar lixo se estiver em uma posição com lixo orgânico ("O") ou reciclável ("R") e não estiver carregando nenhum lixo
        if self.carga is None and (posicao == "0" or posicao == "R"):
            return "pegar"

        #Soltar lixo na posição final (19,19) se estiver carregando algum lixo
        if self.carga is not None and self.linha == 19 and self.coluna == 19:
            return "soltar"

        #Mover-se em direção à posição final (19,19) se estiver carregando algum lixo
        if self.carga is not None:
            return "mover_para_deposito"

        #Procurar Lixos vizinhos e decidir mover-se em direção a eles, se houver algum
        reciclaveis, organicos = self.encontar_lixo_vizinho(matriz)

        if reciclaveis:
            direcao = random.choice(reciclaveis)
            return f"mover_{direcao}"
        if organicos:
            direcao = random.choice(organicos)
            return f"mover_{direcao}"

        #Se não houver lixos vizinhos, mover-se aleatoriamente
        return self.movimento_aleatorio()

#Função para executar a ação decidida pelo agente, chamando a função correspondente com base na ação escolhida. Se a ação for "pegar", chama a função pegar_lixo; se for "soltar", chama a função soltar_lixo; se for uma das direções de movimento, chama a função de movimento correspondente.
    def executar_acao(self, acao, matriz):
        if acao == "pegar":
            return self.pegar_lixo(matriz)
        elif acao == "soltar":
            return self.soltar_lixo(matriz)
        elif acao == "mover_cima":
            self.mover_cima()
        elif acao == "mover_baixo":
            self.mover_baixo()
        elif acao == "mover_esquerda":
            self.mover_esquerda()
        elif acao == "mover_direita":
            self.mover_direita()

    def mover_para_deposito(self):
        if self.linha <19:
            self.mover_baixo()
        if self.coluna <19:
            self.mover_direita()
        return None

    def movimento_aleatorio(self):
        direcoes = []

        if self.linha > 0:
            direcoes.append("cima")
        if self.linha < 19:
            direcoes.append("baixo")
        if self.coluna > 0:
            direcoes.append("esquerda")
        if self.coluna < 19:
            direcoes.append("direita")

        direcao = random.choice(direcoes)

        return f"mover_{direcao}"

'''#teste
#Criação da matriz e alocação da posição inicial do robô coletor de lixo (representada por "A") e da posição final (representada por "X")
matriz = construir_matriz()
matriz[0][0] = "A"
matriz[19][19] = "X"
matriz[0][1] = "O"
matriz[1][0] = "R"

colocar_lixos(matriz)

mostrar_matriz(matriz)

agente = Agente()

print(f"Posição ({agente.linha},{agente.coluna})")
print("Contem: ", agente.observar_posicao(matriz))

reciclaveis, organicos = agente.encontar_lixo_vizinho(matriz)
print("Recicláveis vizinhos:", reciclaveis)
print("Orgânicos vizinhos:", organicos)

print("Ação: ", agente.decidir_acao(matriz))

acao = agente.decidir_acao(matriz)
print("ação escolhida: ", acao)

agente.executar_acao(acao, matriz)
print(f"Posição após ação: ({agente.linha},{agente.coluna})")
print("Contem: ", agente.observar_posicao(matriz))

acao = agente.decidir_acao(matriz)
print("ação escolhida: ", acao)

agente.executar_acao(acao, matriz)
print(f"Posição após ação: ({agente.linha},{agente.coluna})")
print("Contem: ", agente.observar_posicao(matriz))'''