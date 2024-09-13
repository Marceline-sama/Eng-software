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
    jogo = Jogo.get_instance()
    return jogo.escolher_cor(nome_jogador, cor)


@app.post("/receber_objetivo/")
def receber_objetivo(nome_jogador: str):
    jogo = Jogo.get_instance()
    return jogo.receber_objetivo(nome_jogador)


@app.get("/definir_ordem_jogadores/")
def definir_ordem_jogadores():
    jogo = Jogo.get_instance()
    return jogo.definir_ordem_jogadores()


@app.post("/distribuir_territorios/")
def distribuir_territorios():
    jogo = Jogo.get_instance()
    return jogo.distribuir_territorios()

@app.put("/distribuir_exercitos_inicial/")
def distribuir_exercitos_inicial():
    jogo = Jogo.get_instance()
    return jogo.distribuir_exercitos_inicial()


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
    jogo = Jogo.get_instance()
    return jogo.receber_carta(nome_jogador)


@app.put("/mover_exercitos/")
def mover_exercitos(nome_jogador: str, de_territorio: str, para_territorio: str, qtd_exercitos: int):
    jogo = Jogo.get_instance()
    return jogo.mover_exercitos(nome_jogador, de_territorio, para_territorio, qtd_exercitos)


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
    jogo = Jogo.get_instance()
    return jogo.verificar_objetivo(nome_jogador)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
