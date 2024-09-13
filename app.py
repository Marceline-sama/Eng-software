from fastapi import FastAPI, HTTPException
from random import shuffle, choice
from typing import List

import uvicorn

import Jogo

app = FastAPI()


jogadores = []
cores_disponiveis = ["vermelho", "azul", "verde", "amarelo", "preto"]
territorios = ["territorio1", "territorio2", "territorio3", "territorio4", "territorio5"]
baralho_de_cartas = ["carta1", "carta2", "carta3", "carta4"]
objetivos = ["Conquistar 24 territórios", "Eliminar o jogador vermelho", "Conquistar 18 territórios com 2 exércitos em cada"]

dados_jogadores = {}

@app.post("/escolher_cor/")
def escolher_cor(nome_jogador: str, cor: str):
    jogo = Jogo.get_instance()

    if cor not in jogo.cores_disponiveis:
        raise HTTPException(status_code=400, detail="Cor indisponível")

    if nome_jogador not in jogo.jogadores:
        jogo.jogadores[nome_jogador] = {"cor": cor, "territorios": [], "cartas": [], "objetivo": None, "exercitos": 0}
    else:
        raise HTTPException(status_code=400, detail="Jogador já escolheu uma cor")

    jogo.cores_disponiveis.remove(cor)
    return {"mensagem": f"{nome_jogador} escolheu a cor {cor}"}


@app.post("/receber_objetivo/")
def receber_objetivo(nome_jogador: str):
    jogo = Jogo.get_instance()

    if nome_jogador not in jogo.jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")

    if jogo.jogadores[nome_jogador]["objetivo"] is None:
        objetivo = choice(jogo.objetivos)
        jogo.jogadores[nome_jogador]["objetivo"] = objetivo
        return {"objetivo": objetivo}
    else:
        raise HTTPException(status_code=400, detail="Objetivo já atribuído")


@app.get("/definir_ordem_jogadores/")
def definir_ordem_jogadores():
    jogo = Jogo.get_instance()
    jogadores_ordenados = list(jogo.jogadores.keys())
    shuffle(jogadores_ordenados)
    return {"ordem": jogadores_ordenados}


@app.post("/distribuir_territorios/")
def distribuir_territorios():
    jogo = Jogo.get_instance()

    if not jogo.jogadores:
        raise HTTPException(status_code=400, detail="Nenhum jogador cadastrado")

    shuffle(jogo.territorios)
    total_jogadores = len(jogo.jogadores)
    index = 0

    for territorio in jogo.territorios:
        jogador_atual = list(jogo.jogadores.keys())[index % total_jogadores]
        jogo.jogadores[jogador_atual]["territorios"].append(territorio)
        index += 1

    return {"territorios_distribuidos": jogo.jogadores}

@app.put("/distribuir_exercitos_inicial/")
def distribuir_exercitos_inicial():
    jogo = Jogo.get_instance()

    if not jogo.jogadores:
        raise HTTPException(status_code=400, detail="Nenhum jogador cadastrado")

    exercitos_iniciais = 30 // len(jogo.jogadores)
    for jogador in jogo.jogadores:
        jogo.jogadores[jogador]["exercitos"] = exercitos_iniciais

    return {"mensagem": f"Cada jogador recebeu {exercitos_iniciais} exércitos"}


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

    if nome_jogador not in jogo.jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")

    if not jogo.baralho_de_cartas:
        raise HTTPException(status_code=400, detail="Sem cartas no baralho")

    carta = choice(jogo.baralho_de_cartas)
    jogo.jogadores[nome_jogador]["cartas"].append(carta)
    jogo.baralho_de_cartas.remove(carta)

    return {"carta_recebida": carta}


@app.put("/mover_exercitos/")
def mover_exercitos(nome_jogador: str, de_territorio: str, para_territorio: str, qtd_exercitos: int):
    jogo = Jogo.get_instance()

    if nome_jogador not in jogo.jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")

    if de_territorio not in jogo.jogadores[nome_jogador]["territorios"]:
        raise HTTPException(status_code=400, detail="Território inválido")

    if qtd_exercitos > jogo.jogadores[nome_jogador]["exercitos"]:
        raise HTTPException(status_code=400, detail="Exércitos insuficientes")

    jogo.jogadores[nome_jogador]["exercitos"] -= qtd_exercitos
    jogo.jogadores[nome_jogador]["territorios"].append(para_territorio)

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
    jogo = Jogo.get_instance()

    if nome_jogador not in jogo.jogadores:
        raise HTTPException(status_code=400, detail="Jogador não encontrado")

    objetivo = jogo.jogadores[nome_jogador]["objetivo"]
    if not objetivo:
        return {"mensagem": "Nenhum objetivo foi atribuído a este jogador"}
    
    return {"objetivo": objetivo, "status": "Não verificado"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
