from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class Notas(BaseModel):
    linguagem_de_programacao: float
    engenharia_de_software: float
    algoritmos: float
    estrutura_de_dados: float

class Aluno(BaseModel):
    id: str
    nome: str
    notas: Notas

alunos = {}

@app.get("/")
def mensagem():
    return {"message": "Trabalho final de Python"}


def carregar_alunos():
    arquivo = open('alunos.txt', 'r') 
    for linha in arquivo:
        aluno_dict = json.loads(linha) #converte cada linha do alunos.txt em um dicionario
        aluno_id = aluno_dict["id"]
        alunos[aluno_id] = aluno_dict
    arquivo.close()
    return alunos

carregar_alunos()

@app.post("/")
def adicionar_aluno(aluno: Aluno):
    if aluno.id in alunos:
        return {"message": "Aluno com esse ID ja existe"}
    notas = aluno.notas
    notas_dict = notas.__dict__
    for key, value in notas_dict.items():
        if not (0 <= value <= 10):
           return {"message": "A nota de {key} deve estar entre 0 e 10"}
        notas_dict[key] = round(value, 1)

    alunos[aluno.id] = aluno
    aluno_dict = {
        "id": aluno.id,
        "nome": aluno.nome,
        "notas": notas_dict
    }

    aluno_json = json.dumps(aluno_dict) #salva como json 
    with open('alunos.txt', 'a') as file_out:
        file_out.write(aluno_json + "\n")
    return aluno

@app.get("/alunos")
def listar_alunos():
    return list(alunos.values())

@app.get("/alunos/{aluno_id}")
def obter_aluno(aluno_id: str):
    if aluno_id not in alunos:
        return {"message" : "Aluno nao encontrado"}
    return alunos[aluno_id]