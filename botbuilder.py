#PARTE1
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

#PARTE2
app = Flask(__name__)

#PARTE3
@app.route('/teste', methods=['GET'])
def testeGet():
  #MEU CÓDIGO AQUI
  print("teste")
  return"Tudo pronto!"

@app.route('/teste', methods=['POST'])
def testePost():
  #MEU CÓDIGO AQUI
  content = request.json
  #content = request.args['idade']
  json_response = {"messages": [
                        {"text": "Tu tem " + content['idade'] + " anos"},
                        {"text": content['idade'] + " centrimetros de altura"},
                        {"text": "e pesa " + content['peso'] + " quilos"}
                    ]
                  }

  return jsonify(json_response)
  #return jsonify(content)

#PARTE4
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='localhost', port=port)
