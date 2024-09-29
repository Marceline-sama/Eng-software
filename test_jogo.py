import pytest
from fastapi import HTTPException
from Jogo import Jogo  # Supondo que a classe Jogo esteja no arquivo jogo.py

# Teste 1: Verificar se o padrão Singleton está funcionando
def test_singleton_instance():
    jogo1 = Jogo()
    jogo2 = Jogo()
    assert jogo1 is jogo2, "A classe Jogo deve ser uma única instância (Singleton)"

# Teste 2: Testar o método escolher_cor()
def test_escolher_cor():
    jogo = Jogo()
    
    # Reiniciar estado para os testes
    jogo.cores_disponiveis = ["vermelho", "azul", "verde", "amarelo", "preto"]
    jogo.dados_jogadores = {}

    # Escolher cor para um jogador novo
    jogo.escolher_cor("Jogador1", "vermelho")
    assert "Jogador1" in jogo.dados_jogadores
    assert jogo.dados_jogadores["Jogador1"]["cor"] == "vermelho"
    assert "vermelho" not in jogo.cores_disponiveis

    # Tentar escolher uma cor já escolhida
    with pytest.raises(HTTPException):
        jogo.escolher_cor("Jogador2", "vermelho")

# Teste 3: Verificar a distribuição de territórios
def test_distribuir_territorios():
    jogo = Jogo()
    
    # Reiniciar estado para os testes
    jogo.cores_disponiveis = ["vermelho", "azul"]
    jogo.dados_jogadores = {
        "Jogador1": {"cor": "vermelho", "territorios": [], "cartas": []},
        "Jogador2": {"cor": "azul", "territorios": [], "cartas": []}
    }
    jogo.territorios = ["territorio1", "territorio2", "territorio3", "territorio4", "territorio5"]
    
    # Distribuir os territórios
    jogo.distribuir_territorios()
    
    # Verificar se todos os territórios foram distribuídos
    num_territorios_total = sum([len(j["territorios"]) for j in jogo.dados_jogadores.values()])
    assert num_territorios_total == len(jogo.territorios)

# Teste 4: Testar o recebimento de objetivos
def test_receber_objetivo():
    jogo = Jogo()

    # Reiniciar estado para os testes
    jogo.dados_jogadores = {
        "Jogador1": {"cor": "vermelho", "territorios": [], "cartas": []}
    }

    # Jogador sem objetivo recebe um
    jogo.receber_objetivo("Jogador1")
    assert "objetivo" in jogo.dados_jogadores["Jogador1"]

    # Jogador já com objetivo tenta receber outro
    with pytest.raises(HTTPException):
        jogo.receber_objetivo("Jogador1")

# Teste 5: Testar movimentação de exércitos
def test_mover_exercitos():
    jogo = Jogo()

    # Reiniciar estado para os testes
    jogo.dados_jogadores = {
        "Jogador1": {
            "cor": "vermelho", 
            "territorios": ["territorio1", "territorio2"], 
            "cartas": [],
            "exercitos": 10
        }
    }

    # Jogador tenta mover exércitos de um território válido
    resultado = jogo.mover_exercitos("Jogador1", "territorio1", "territorio2", 5)
    assert resultado == {"mensagem": "5 exércitos movidos de territorio1 para territorio2"}
    assert jogo.dados_jogadores["Jogador1"]["exercitos"] == 5  # Redução dos exércitos

    # Jogador tenta mover mais exércitos do que possui
    with pytest.raises(HTTPException):
        jogo.mover_exercitos("Jogador1", "territorio1", "territorio2", 10)

def test_singleton():
    jogo1 = Jogo.get_instance()
    jogo2 = Jogo.get_instance()
    assert jogo1 is jogo2, "O padrão Singleton não está funcionando corretamente."

def test_criar_jogador():
    jogo = Jogo.get_instance()
    jogador = jogo.criar_jogador("Jogador1", "vermelho")
    assert jogador.nome == "Jogador1"
    assert jogador.cor == "vermelho"

    # Testar se cor já escolhida não pode ser usada
    with pytest.raises(ValueError):
        jogo.criar_jogador("Jogador2", "vermelho")