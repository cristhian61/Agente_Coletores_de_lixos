import random
import copy


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
    for linha in range(20):
        elementos = []

        for coluna in range(20):

            if linha == Agente.linha and coluna == Agente.coluna:
                elementos.append("A")
            else:
                elementos.append(matriz[linha][coluna])

        print(" ".join(elementos))

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

def contar_lixos(matriz):
        quantidade = 0

        for linha in matriz:
            for elemento in linha:
                if elemento == "O" or elemento == "R":
                    quantidade += 1
        return quantidade

def construir_matriz_visitas():
    matriz = []

    for i in range(20):
        linha = []
        for j in range(20):
            linha.append(0)
        matriz.append(linha)
    return matriz

def criar_ambiente(num_ambientes):
    ambientes = []

    for i in range(num_ambientes):

        matriz = construir_matriz()
        matriz[19][19] = "X"
        colocar_lixos(matriz)

        ambientes.append(matriz)

    return ambientes


#================================== Agente ==================================

#Criação e movimentação do agente n matriz
class Agente:
    def __init__(self):
        self.linha = 0
        self.coluna = 0
        self.carga = None
        self.pontuacao = 0
        self.passos = 0
        self.coletados = 0
        self.entregues = 0

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

    def mover_para_direcao(self, direcao):
        if "cima" in direcao:
            self.mover_cima()

        if "baixo" in direcao:
            self.mover_baixo()

        if "esquerda" in direcao:
            self.mover_esquerda()

        if "direita" in direcao:
            self.mover_direita()

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
            self.coletados += 1
            return True

        if matriz[self.linha][self.coluna] == "R":
            self.carga = "R"
            matriz[self.linha][self.coluna] = "."
            self.coletados += 1
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
                self.entregues += 1
                return True  # Lixo solto com sucesso

        return False  # Não é possível soltar lixo fora da posição 

#Função para encontrar os lixos vizinhos do agente na matriz, retornando duas listas: uma com as direções dos lixos recicláveis ("R") e outra com as direções dos lixos orgânicos ("O").
    def encontrar_lixo_vizinho(self, matriz):
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
        if self.carga is None and (posicao == "O" or posicao == "R"):
            return "pegar"

        #Soltar lixo na posição final (19,19) se estiver carregando algum lixo
        if self.carga is not None and self.linha == 19 and self.coluna == 19:
            return "soltar"

        #Mover-se em direção à posição final (19,19) se estiver carregando algum lixo
        if self.carga is not None:
            return self.mover_para_deposito()

        #Procurar Lixos vizinhos e decidir mover-se em direção a eles, se houver algum
        reciclaveis, organicos = self.encontrar_lixo_vizinho(matriz)

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

        elif acao == "mover_para_deposito":
            return self.mover_para_deposito()

        elif acao.startswith("mover_"):
                    direcao = acao.replace("mover_", "")
                    return self.mover_para_direcao(direcao)

#Função para mover o agente em direção à posição final (19,19) na matriz, chamada quando o agente está carregando algum lixo. O agente se move para baixo e para a direita até alcançar a posição final.
    def mover_para_deposito(self):
        if self.linha <19:
            return "mover_baixo"
        if self.coluna <19:
            return "mover_direita"
        return None

#Função para escolher uma direção aleatória para o agente se mover, garantindo que ele não saia dos limites da matriz. A função retorna a ação de movimento escolhida.
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


class AgenteModelo(Agente):

    def __init__(self):
        super().__init__()

        self.visitas = construir_matriz_visitas()

        self.visitas[self.linha][self.coluna] = 1

#Função atualiza por onde o agente ja passou
    def atualizar_modelo(self):
        self.visitas[self.linha][self.coluna] += 1

    def executar_acao(self, acao, matriz):
        super().executar_acao(acao, matriz)
        self.atualizar_modelo()

    def encontrar_direcoes_nao_visitadas(self, matriz):
        vizinhos = self.observar_posicoes_vizinhas(matriz)

        direcoes = []

        deslocamento = {
            "cima_esquerda": (-1,-1),
            "cima": (-1,0),
            "cima_direita": (-1,1),
            "esquerda": (0,-1),
            "direita": (0,1),
            "baixo_esquerda": (1,-1),
            "baixo": (1,0),
            "baixo_direita": (1,1)
        }
        for direcao in vizinhos:
            dl, dc = deslocamento[direcao]

            nova_linha = self.linha + dl
            nova_coluna = self.coluna + dc

            if self.visitas[nova_linha][nova_coluna] == 0:
                direcoes.append(direcao)

        return direcoes

    def encontrar_direcao_menos_visitadas(self, matriz):
        vizinhos = self.observar_posicoes_vizinhas(matriz)

        deslocamento = {
                    "cima_esquerda": (-1,-1),
                    "cima": (-1,0),
                    "cima_direita": (-1,1),
                    "esquerda": (0,-1),
                    "direita": (0,1),
                    "baixo_esquerda": (1,-1),
                    "baixo": (1,0),
                    "baixo_direita": (1,1)
        }

        menor_visita = None
        direcoes = []

        for direcao in vizinhos:
            dl, dc = deslocamento[direcao]

            nova_linha = self.linha + dl
            nova_coluna = self.coluna + dc
            visitas = self.visitas[nova_linha][nova_coluna]

            if menor_visita is None or visitas < menor_visita:
                menor_visita = visitas 
                direcoes = [direcao]

            elif visitas == menor_visita:
                direcoes.append(direcao)

        if direcoes:
            return random.choice(direcoes)

        return None

    def decidir_acao(self, matriz):

        posicao = self.observar_posicao(matriz)

        if self.carga is not None and self.linha == 19 and self.coluna == 19:
            return "soltar"

        if self.carga is not None:
            return self.mover_para_deposito()

        if posicao == "O" or posicao == "R":
            return "pegar"

        reciclaveis, organicos = self.encontrar_lixo_vizinho(matriz)

        if reciclaveis:
            direcao = random.choice(reciclaveis)
            return f"mover_{direcao}"
        if organicos:
                    direcao = random.choice(organicos)
                    return f"mover_{direcao}"

        direcoes_nao_visitadas = self.encontrar_direcoes_nao_visitadas(matriz)

        if direcoes_nao_visitadas:
            direcao = random.choice(direcoes_nao_visitadas)
            return f"mover_{direcao}"

        direcao = self.encontrar_direcao_menos_visitadas(matriz)

        if direcao:
            return f"mover_{direcao}"
        
        return self.movimento_aleatorio() 


class AgenteBDI(Agente):
    def __init__(self):
        super().__init__()

        self.crencas = {
            "posicao": (self.linha, self.coluna),
            "carga": self.carga,
            "deposito": (19,19)
        }

        self.desejos = [
            "coletar_reciclavel",
            "coletar_organico",
            "ir_ao_deposito",
            "minimizar_passos"
        ]

        self.intenceos = None

    def atualizar_crenca(self):
        self.crencas["posicao"] = (self.linha, self.coluna)
        self.crencas["carga"] = self.carga

    def gerar_opcoes(self, matriz):
        opcoes = []

        if self.carga is not None:
            opcoes.append("ir_ao_deposito")
            return opcoes
        posicao = self.observar_posicao(matriz)

        if posicao == "R":
            opcoes.append("coletar_reciclavel")
        elif posicao == "O":
            opcoes.append("coletar_organico")

        reciclaveis, organicos = self.encontrar_lixo_vizinho(matriz)

        if reciclaveis and "coletar_reciclavel" not in opcoes:
            opcoes.append("coletar_reciclavel")
        if organicos and "coletar_organico" not in opcoes:
            opcoes.append("coletar_organico")

        opcoes.append("explorar")

        return opcoes

    def selecionar_intencao(self, opcoes):
        if "coletar_reciclavel" in opcoes:
            self.intenceos = "coletar_reciclavel"

        elif "coletar_organico" in opcoes:
            self.intenceos = "coletar_organico"

        elif "ir_ao_deposito" in opcoes:
            self.intenceos = "ir_ao_deposito"

        elif "explorar" in opcoes:
            self.intenceos = "explorar"

        else:
            self.intenceos = None

    def selecionar_acao(self, matriz):

        #Intenção: ir ao deposito
        if self.intenceos == "ir_ao_deposito":
            if self.linha == 19 and self.coluna == 19:
                return "soltar"
            return self.mover_para_deposito()

        #Intenção: coletar reciclavel
        if self.intenceos == "coletar_reciclavel":
            posicao = self.observar_posicao(matriz)
            if posicao == "R":
                return "pegar"

            reciclaveis, organicos = self.encontrar_lixo_vizinho(matriz)

            if reciclaveis:
                direcao = random.choice(reciclaveis)
                return f"mover_{direcao}"

        #Intenção: coletar organico
        if self.intenceos == "coletar_organico":
            posicao = self.observar_posicao(matriz)
            if posicao == "O":
                return "pegar"

            reciclaveis, organicos = self.encontrar_lixo_vizinho(matriz)

            if organicos:
                direcao = random.choice(organicos)
                return f"mover_{direcao}"

        #Intenção: explorar
        if self.intenceos == "explorar":
            return self.movimento_aleatorio()

        return self.movimento_aleatorio()

    def ciclo_bdi(self, matriz):
        self.atualizar_crenca()

        opcoes = self.gerar_opcoes(matriz)
        self.selecionar_intencao(opcoes)
        return self.selecionar_acao(matriz)



#================================== Execução Agentes ==================================
#Função implementar o Agente Reativo Simples
def simular_reativo_simples(ambientes):
    NUM_EXECUCOES = len(ambientes)
    LIMITE_SEGURACA = 8000

    total_coletados = 0
    total_entregues = 0
    total_pontuacao = 0
    total_passos = 0
    sucesso = 0
    taxa_sucesso = 0

    for ambiente in ambientes:

        matriz = copy.deepcopy(ambiente)

        agente = Agente()

        while agente.entregues <15 and agente.passos < LIMITE_SEGURACA:
            acao = agente.decidir_acao(matriz)

            agente.executar_acao(acao, matriz)

        if agente.entregues == 15:
            sucesso += 1
        total_coletados += agente.coletados
        total_entregues += agente.entregues
        total_pontuacao += agente.pontuacao
        total_passos += agente.passos 

    media_coletados = total_coletados / NUM_EXECUCOES
    media_entregues = total_entregues / NUM_EXECUCOES
    media_pontuacao = total_pontuacao / NUM_EXECUCOES
    media_passos = total_passos / NUM_EXECUCOES

    taxa_sucesso = (sucesso/NUM_EXECUCOES)*100

    return(
        media_coletados,
        media_entregues,
        media_pontuacao,
        media_passos,
        sucesso,
        taxa_sucesso,
        NUM_EXECUCOES
    )

def simular_baseado_modelo(ambientes):
    NUM_EXECUCOES = len(ambientes)
    LIMITE_SEGURACA = 8000

    total_coletados = 0
    total_entregues = 0
    total_pontuacao = 0
    total_passos = 0
    sucesso = 0
    taxa_sucesso = 0

    for ambiente in ambientes:

        matriz = copy.deepcopy(ambiente)

        agente = AgenteModelo()

        while agente.entregues <15 and agente.passos < LIMITE_SEGURACA:
            acao = agente.decidir_acao(matriz)

            agente.executar_acao(acao, matriz)

        if agente.entregues == 15:
            sucesso += 1
        total_coletados += agente.coletados
        total_entregues += agente.entregues
        total_pontuacao += agente.pontuacao
        total_passos += agente.passos 

    media_coletados = total_coletados / NUM_EXECUCOES
    media_entregues = total_entregues / NUM_EXECUCOES
    media_pontuacao = total_pontuacao / NUM_EXECUCOES
    media_passos = total_passos / NUM_EXECUCOES

    taxa_sucesso = (sucesso/NUM_EXECUCOES)*100

    return(
        media_coletados,
        media_entregues,
        media_pontuacao,
        media_passos,
        sucesso,
        taxa_sucesso,
        NUM_EXECUCOES
    )

def simular_bdi(ambientes):
    NUM_EXECUCOES = len(ambientes)
    LIMITE_SEGURACA = 8000

    total_coletados = 0
    total_entregues = 0
    total_pontuacao = 0
    total_passos = 0
    sucesso = 0
    taxa_sucesso = 0

    for ambiente in ambientes:

        matriz = copy.deepcopy(ambiente)

        agente = AgenteBDI()

        while agente.entregues <15 and agente.passos < LIMITE_SEGURACA:
            acao = agente.ciclo_bdi(matriz)

            agente.executar_acao(acao, matriz)

        if agente.entregues == 15:
            sucesso += 1
        
        total_coletados += agente.coletados
        total_entregues += agente.entregues
        total_pontuacao += agente.pontuacao
        total_passos += agente.passos 

    media_coletados = total_coletados / NUM_EXECUCOES
    media_entregues = total_entregues / NUM_EXECUCOES
    media_pontuacao = total_pontuacao / NUM_EXECUCOES
    media_passos = total_passos / NUM_EXECUCOES

    taxa_sucesso = (sucesso/NUM_EXECUCOES)*100

    return(
        media_coletados,
        media_entregues,
        media_pontuacao,
        media_passos,
        sucesso,
        taxa_sucesso,
        NUM_EXECUCOES
    )


#================================== Execução Resultados ==================================

ambientes = criar_ambiente(100) #o numero no argumento é a quantidade de execuções que o programa irá executar 

coletados, entregues, pontuacao, passos, sucessos, taxa_conc, NUM_EXEC = simular_reativo_simples(ambientes)

print("\n======== AGENTE REATIVO SIMPLES ========")

print(f"\nExeculçoes: {NUM_EXEC}\n")

print(f"Média de coletados: {coletados:.2f}")
print(f"Média de entregues: {entregues:.2f}")
print(f"Média de pontuação: {pontuacao:.2f}")
print(f"Média de passos: {passos:.2f}")

print(f"\nExecuçoes concluídas: {sucessos}/{NUM_EXEC}")
print(f"Taxa de conclusão: {taxa_conc:.2f}%\n")


coletados, entregues, pontuacao, passos, sucessos, taxa_conc, NUM_EXEC = simular_baseado_modelo(ambientes)

print("\n======= AGENTE BASEADO EM MODELO =======")

print(f"\nExeculçoes: {NUM_EXEC}\n")

print(f"Média de coletados: {coletados:.2f}")
print(f"Média de entregues: {entregues:.2f}")
print(f"Média de pontuação: {pontuacao:.2f}")
print(f"Média de passos: {passos:.2f}")

print(f"\nExecuçoes concluídas: {sucessos}/{NUM_EXEC}")
print(f"Taxa de conclusão: {taxa_conc:.2f}%\n")


coletados, entregues, pontuacao, passos, sucessos, taxa_conc, NUM_EXEC = simular_bdi(ambientes)

print("\n============== AGENTE BDI ==============")

print(f"\nExeculçoes: {NUM_EXEC}\n")

print(f"Média de coletados: {coletados:.2f}")
print(f"Média de entregues: {entregues:.2f}")
print(f"Média de pontuação: {pontuacao:.2f}")
print(f"Média de passos: {passos:.2f}")

print(f"\nExecuçoes concluídas: {sucessos}/{NUM_EXEC}")
print(f"Taxa de conclusão: {taxa_conc:.2f}%\n")
