from fastapi import FastAPI, HTTPException
from random import shuffle, choice
from typing import List

import uvicorn

import Jogo

app = FastAPI()

# Dados iniciais do jogo
jogadores = []
cores_disponiveis = ["vermelho", "azul", "verde", "amarelo", "preto"]
territorios = ["territorio1", "territorio2", "territorio3", "territorio4", "territorio5"]
baralho_de_cartas = ["carta1", "carta2", "carta3", "carta4"]
objetivos = ["Conquistar 24 territórios", "Eliminar o jogador vermelho", "Conquistar 18 territórios com 2 exércitos em cada"]

dados_jogadores = {}

@app.post("/escolher_cor/")
def escolher_cor(nome_jogador: str, cor: str):
    jogo = Jogo()    
    if cor not in jogo.cores_disponiveis:
        raise HTTPException(status_code=400, detail="Cor não disponível")
    if nome_jogador in jogo.dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador já existe")

    jogo.dados_jogadores[nome_jogador] = {"cor": cor, "territorios": [], "cartas": []}
    jogo.cores_disponiveis.remove(cor)
    return {"mensagem": f"{nome_jogador} escolheu {cor}"}

@app.post("/receber_objetivo/")
def receber_objetivo(nome_jogador: str):
    if nome_jogador not in dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")

    if "objetivo" in dados_jogadores[nome_jogador]:
        raise HTTPException(status_code=400, detail="Jogador já tem um objetivo")

    objetivo = choice(objetivos)
    dados_jogadores[nome_jogador]["objetivo"] = objetivo
    return {"mensagem": f"{nome_jogador} recebeu o objetivo: {objetivo}"}

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

@app.put("/distribuir_exercitos_inicial/")
def distribuir_exercitos_inicial():
    if len(dados_jogadores) == 0:
        raise HTTPException(status_code=400, detail="Não há jogadores disponíveis")

    exercitos_por_jogador = 10

    for jogador in dados_jogadores.keys():
        dados_jogadores[jogador]["exercitos"] = exercitos_por_jogador

    return {"mensagem": "Exércitos distribuídos no início", "dados_jogadores": dados_jogadores}

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

@app.put("/mover_exercitos/")
def mover_exercitos(nome_jogador: str, de_territorio: str, para_territorio: str, qtd_exercitos: int):
    if nome_jogador not in dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")
    if de_territorio not in dados_jogadores[nome_jogador]["territorios"]:
        raise HTTPException(status_code=400, detail="Território de origem inválido")

    exercitos_disponiveis = dados_jogadores[nome_jogador].get("exercitos", 0)
    if exercitos_disponiveis < qtd_exercitos:
        raise HTTPException(status_code=400, detail="Exércitos insuficientes")

    dados_jogadores[nome_jogador]["exercitos"] -= qtd_exercitos
    return {"mensagem": f"{qtd_exercitos} exércitos movidos de {de_territorio} para {para_territorio}"}

@app.delete("/realizar_troca_cartas/")
def realizar_troca_cartas(nome_jogador: str, cartas: List[str]):
    if nome_jogador not in dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")

    if set(cartas).issubset(dados_jogadores[nome_jogador]["cartas"]):
        for carta in cartas:
            dados_jogadores[nome_jogador]["cartas"].remove(carta)
        return {"mensagem": "Troca realizada com sucesso"}
    else:
        raise HTTPException(status_code=400, detail="Cartas inválidas para troca")

@app.get("/verificar_objetivo/")
def verificar_objetivo(nome_jogador: str):
    if nome_jogador not in dados_jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")

    objetivo = dados_jogadores[nome_jogador].get("objetivo", None)
    if not objetivo:
        raise HTTPException(status_code=400, detail="Objetivo não encontrado")

    objetivo_completado = False
    if objetivo == "Conquistar 18 territórios com 2 exércitos em cada":
        territorios_com_2_exercitos = sum(
            2 <= dados_jogadores[nome_jogador].get("exercitos_territorio", {}).get(t, 0)
            for t in dados_jogadores[nome_jogador]["territorios"]
        )
        if territorios_com_2_exercitos >= 18:
            objetivo_completado = True
    elif objetivo == "Conquistar 24 territórios":
        if len(dados_jogadores[nome_jogador]["territorios"]) >= 24:
            objetivo_completado = True
    elif objetivo == "Eliminar o jogador vermelho":
        if all(dados_jogadores[jogador].get("cor") != "vermelho" for jogador in dados_jogadores):
            objetivo_completado = True

    return {"objetivo_completado": objetivo_completado}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
