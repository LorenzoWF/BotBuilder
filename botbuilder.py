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


@app.route('/verificarInformacoes', methods=['POST'])
def testePost():
    json_response = {"messages": [
                        {"text": "Tu tem " + str(request.form.get('idade')) + " anos"},
                        {"text": "Tu pesa " + str(request.form.get('peso')) + " quilos"},
                        {"text": "Tu mede " + str(request.form.get('altura')) + " centimetros de altura"}
                     ]
                   }
    return jsonify(json_response)

if __name__ == '__main__':
  #port = int(os.environ.get('PORT', 5000))
  #app.run(host='192.168.9.206', port=port)
  app.run()
