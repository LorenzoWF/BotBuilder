from flask import Flask, jsonify, request, render_template, safe_join, send_from_directory
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "teste"

@app.route('/teste', methods=['GET'])
def testeGet():
  print("teste")
  return"Tudo pronto!"

@app.route('/calculaImc', methods=['POST'])
def calculaImc():
    if not request.form.get('peso') is None and not request.form.get('altura') is None:
        peso    = int(request.form.get('peso'))
        altura  = int(request.form.get('altura'))

    if request.form.get('peso') is None or request.form.get('altura') is None:
        json_response = {"messages": [
                            {"text": "Houve um problema no recebimento dos dados, tente novamente!"}
                         ]
                       }
    else:
        altura          = altura / 100
        alturaQuadrado  = altura * altura
        imc             = int(peso / alturaQuadrado)
        #FAZER ELE DIZER SE ESTA BOM OU RUIM COM SWITCH

        if imc < 17:
            comentario = "Você está muito abaixo do peso"
        elif imc >= 17 and imc <= 18.49:
            comentario = "Você está abaixo do peso"
        elif imc >= 18.5 and imc <= 24.99:
            comentario = "Você está com o peso normal"
        elif imc >= 25 and imc <= 29.99:
            comentario = "Você está acima do peso"
        elif imc >= 30 and imc <= 34.99:
            comentario = "Você está com obesidade I"
        elif imc >= 35 and imc <= 39.99:
            comentario = "Você está com obesidade II"
        elif imc >= 40:
            comentario = "Você está com obesidade III"
        else:
            comentario = "SEM COMENTARIOS"

        json_response = {"messages": [
                            {"text": "O seu IMC atual é " + str(round(imc,2))},
                            {"text": comentario}
                         ]
                       }

    return jsonify(json_response)


@app.route('/passarTreino', methods=['POST'])
def testePost():

    if request.form.get('peso') is None:
        return mensagemErro('O peso não pode ser menor que zero. Tente novamente.')
    elif int(request.form.get('peso')) <= 0:
        return mensagemErro('O peso não pode ser menor que zero. Tente novamente.')

    if request.form.get('idade') is None:
        return mensagemErro('A idade não pode ser menor que zero. Tente novamente.')
    elif int(request.form.get('idade')) <= 0:
        return mensagemErro('O peso não pode ser menor que zero. Tente novamente.')

    if request.form.get('altura') is None:
        return mensagemErro('A altura não pode ser menor que zero. Tente novamente.')
    elif int(request.form.get('altura')) <= 0:
        return mensagemErro('O peso não pode ser menor que zero. Tente novamente.')

    if request.form.get('vezesTreino') is None:
        return mensagemErro('O numero de dias para treino não pode ser igual ou menor que zero. Tente novamente.')
    elif int(request.form.get('vezesTreino')) <= 0:
        return mensagemErro('O peso não pode ser menor que zero. Tente novamente.')

    if request.form.get('problemaSaude') is None:
        return mensagemErro('Houve um erro durante a coleta dos dados. Tente novamente.')

    if request.form.get('objetivo') is None:
        return mensagemErro('Houve um erro durante a coleta dos dados. Tente novamente.')

    if request.form.get('local') is None:
        return mensagemErro('Houve um erro durante a coleta dos dados. Tente novamente.')

    peso            = int(request.form.get('peso'))
    idade           = int(request.form.get('idade'))
    altura          = int(request.form.get('altura'))
    problemaSaude   = int(request.form.get('problemaSaude'))
    objetivo        = int(request.form.get('objetivo'))
    local           = int(request.form.get('local'))
    vezesTreino     = int(request.form.get('vezesTreino'))

    mensagemInicial = "De acordo com o que você me passou vou lhe passar o seguinte treino:"

    '''tiposTreino = []
    tiposTreino.append(tipoTreino(1, 'costas'))
    tiposTreino.append(tipoTreino(2, 'peito'))
    tiposTreino.append(tipoTreino(3, 'tricpes'))
    tiposTreino.append(tipoTreino(4, 'biceps'))
    tiposTreino.append(tipoTreino(5, 'pernas'))'''

    if vezesTreino >= 5:
        mensagemVezesTreino = "Você irá treinar " + str(vezesTreino) + " vezes por semana, de segunda a sexta"
        mensagemExercicio   = "Segunda, quarta e sexta você irá fazer exercicios para costas, pernas e triceps. Nas terças e quintas você irá fazer bicpes e peito."
    elif vezesTreino == 4:
        mensagemVezesTreino = "Você irá treinar " + str(vezesTreino) + " vezes por semana, de segunda a quarta mais toda sexta"
        mensagemExercicio   = "Segunda e quarta você irá fazer exercicios para costas, pernas e triceps. Nas terças e sextas você irá fazer bicpes e peito."
    elif vezesTreino == 3:
        mensagemVezesTreino = "Você irá treinar " + str(vezesTreino) + " vezes por semana, de segunda, quarta e sexta"
        mensagemExercicio   = "Segunda e sexta você irá fazer exercicios para costas, pernas e triceps. Na quarta você irá fazer bicpes e peito."
    elif vezesTreino == 2:
        mensagemVezesTreino = "Você irá treinar " + str(vezesTreino) + " vezes por semana, nas terças e quintas"
        mensagemExercicio   = "Terça você irá fazer exercicios para costas, pernas e triceps. Na quinta você irá fazer bicpes e peito."
    elif vezesTreino == 1:
        mensagemVezesTreino = "Você irá treinar uma vez por semana, nas terças"
        mensagemExercicio   = "Em uma semana você irá fazer exercicios para costas, pernas e triceps, e na outra semana você irá fazer bicpes e peito."

    mensagemCarga = "Por enquanto a carga vou deixar a seu critério, caso queria mais detalhes basta informar a palavra treino + dia da semana que eu lhe passo. Exemplo: Treino Segunda."
    mensagemMotivacional = "Agora é HORA DO SHOW! BIIIIRRLLL!"

    json_response = {"messages": [
                        {"text": mensagemInicial},
                        {"text": mensagemVezesTreino},
                        {"text": mensagemExercicio},
                        {"text": mensagemCarga},
                        {"text": mensagemMotivacional}
                     ]
                   }
    return jsonify(json_response)

def mensagemErro(mensagemErro):
    json_response = {"messages": [
                        {"text": mensagemErro}
                     ]
                   }
    return jsonify(json_response)

if __name__ == '__main__':
  #port = int(os.environ.get('PORT', 5000))
  #app.run(host='192.168.9.206', port=port)
  app.run()


class tipoTreino:
    numero = 0
    descricao = ""

    def __init__(self, numero, dsecricao):
        self.numero = numero
        self.descricao = descricao
