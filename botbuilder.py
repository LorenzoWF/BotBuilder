from flask import Flask, jsonify, request, render_template, safe_join, send_from_directory
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

app = Flask(__name__)

@app.route('/')
def index():
    #return render_template("index.html")
    return "teste"

@app.route('/teste', methods=['GET'])
def testeGet():
  print("teste")
  return"Tudo pronto!"

@app.route('/teste', methods=['POST'])
def testePost():
    #content = request.json
    #string = "teste var"
    #python_obj = json.dumps(request.json)
    #print(type(python_obj))

    json_response = {"messages": [
                        {"text": "TESTE 1"},
                        {"text": "TESTE 2"}
                     ]
                   }
    return jsonify(json_response)

if __name__ == '__main__':
  #port = int(os.environ.get('PORT', 5000))
  #app.run(host='192.168.9.206', port=port)
  #app.run(host='localhost')
  #app.run(host='192.168.9.206')
  app.run()
