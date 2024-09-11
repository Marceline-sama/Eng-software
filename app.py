from fastapi import FastAPI, HTTPException
from random import shuffle, choice

app = FastAPI()

jogadores = []
cores_disponiveis = ["vermelho", "azul", "verde", "amarelo", "preto"]
territorios = ["territorio1", "territorio2", "territorio3", "territorio4", "territorio5"]
baralho_de_cartas = ["carta1", "carta2", "carta3", "carta4"]

dados_jogadores = {}

@app.post("/escolher_cor/")
def escolher_cor(nome_jogador: str, cor: str):
    if cor not in cores_disponiveis:
        raise HTTPException(status_code=400, detail="Cor não disponível")
    if nome_jogador in dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador já existe")
    
    dados_jogadores[nome_jogador] = {"cor": cor, "territorios": [], "cartas": []}
    cores_disponiveis.remove(cor)
    return {"mensagem": f"{nome_jogador} escolheu {cor}"}

@app.get("/definir_ordem_jogadores/")
def definir_ordem_jogadores():
    if len(dados_jogadores) < 2:
        raise HTTPException(status_code=400, detail="Não há jogadores suficientes")
    
    lista_jogadores = list(dados_jogadores.keys())
    shuffle(lista_jogadores)
    return {"ordem": lista_jogadores}

@app.post("/distribuir_territorios/")
def distribuir_territorios():
    if len(dados_jogadores) == 0:
        raise HTTPException(status_code=400, detail="Não há jogadores disponíveis")
    
    shuffle(territorios)
    num_jogadores = len(dados_jogadores)
    for i, territorio in enumerate(territorios):
        jogador = list(dados_jogadores.keys())[i % num_jogadores]
        dados_jogadores[jogador]["territorios"].append(territorio)
    
    return {"territorios_distribuidos": dados_jogadores}

@app.post("/distribuir_exercitos/")
def distribuir_exercitos(nome_jogador: str, exercitos: int):
    if nome_jogador not in dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")
    
    dados_jogadores[nome_jogador]["exercitos"] = exercitos
    return {"mensagem": f"{nome_jogador} recebeu {exercitos} exércitos"}

@app.post("/atacar/")
def atacar(nome_jogador: str, de_territorio: str, para_territorio: str):
    if nome_jogador not in dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")
    if de_territorio not in dados_jogadores[nome_jogador]["territorios"]:
        raise HTTPException(status_code=400, detail="Território de ataque inválido")
    
    resultado = choice(["sucesso", "falha"])
    if resultado == "sucesso":
        dados_jogadores[nome_jogador]["territorios"].append(para_territorio)
    return {"resultado": resultado}

@app.post("/receber_carta/")
def receber_carta(nome_jogador: str):
    if nome_jogador not in dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")
    
    if len(baralho_de_cartas) == 0:
        raise HTTPException(status_code=400, detail="Não há mais cartas disponíveis")
    
    carta = baralho_de_cartas.pop()
    dados_jogadores[nome_jogador]["cartas"].append(carta)
    return {"mensagem": f"{nome_jogador} recebeu {carta}"}
