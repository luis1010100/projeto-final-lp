from fastapi import FastAPI
from pydantic import BaseModel
import json
from statistics import mean, median, stdev
import os

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
    if not os.path.exists('alunos.txt'): # cria o arquivo se ele não existir
        with open('alunos.txt', 'w') as arquivo:
            pass
    else:
        with open('alunos.txt', 'r') as arquivo:
            for linha in arquivo:
                aluno_dict = json.loads(linha) # converte cada linha do alunos.txt em um dicionário
                aluno_id = aluno_dict["id"]
                notas = Notas(**aluno_dict["notas"])
                aluno = Aluno(id=aluno_id, nome=aluno_dict["nome"], notas=notas)
                alunos[aluno_id] = aluno

carregar_alunos()

@app.post("/")
def adicionar_aluno(aluno: Aluno):
    if aluno.id in alunos:
        return {"message": "Aluno com esse ID já existe"}
    notas = aluno.notas
    notas_dict = notas.__dict__
    for key, value in notas_dict.items():
        if not (0 <= value <= 10):
            return {"message": f"A nota de {key} deve estar entre 0 e 10"}
        notas_dict[key] = round(value, 1)

    alunos[aluno.id] = aluno
    aluno_dict = {
        "id": aluno.id,
        "nome": aluno.nome,
        "notas": notas_dict
    }

    aluno_json = json.dumps(aluno_dict) # salva como json
    with open('alunos.txt', 'a') as file_out:
        file_out.write(aluno_json + "\n")
    return aluno

@app.get("/alunos")
def listar_alunos():
    return list(alunos.values())

@app.get("/alunos/{aluno_id}")
def obter_aluno(aluno_id: str):
    if aluno_id not in alunos:
        return {"message" : "Aluno não encontrado"}
    return alunos[aluno_id]


@app.get("/estatisticas/{disciplina}") #exercicio extra 1 
def estatisticas_disciplina(disciplina: str):
    notas_disciplina = []
    for aluno in alunos.values():
        if disciplina in aluno.notas.__dict__:
            notas_disciplina.append(aluno.notas.__dict__[disciplina])
    
    if not notas_disciplina:
        return {"message": "Disciplina não encontrada"}
    
    media = mean(notas_disciplina)
    mediana = median(notas_disciplina)
    if len(notas_disciplina) > 1:
        desvio_padrao = stdev(notas_disciplina)
    else:
        desvio_padrao = 0.0 # o desvio padrão de apenas um dado sempre é 0
    return {
        "disciplina": disciplina,
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "desvio_padrao": round(desvio_padrao, 2)
    }

@app.get("/desempenho/abaixo-do-esperado") #exercicios extra 2
def desempenho_abaixo(): 
    alunos_abaixo = []
    for aluno in alunos.values():
        notas = aluno.notas.__dict__.values()
        abaixo_do_esperado = False
        for nota in notas:
            if nota < 6.0:
                abaixo_do_esperado = True
                break
        if abaixo_do_esperado:
            alunos_abaixo.append(aluno)
    return alunos_abaixo
