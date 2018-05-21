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

    json_response = {"messages": [
                        {"text": "Tu tem " + request.form.get('idade') + " anos"},
                        {"text": "Tu pesa " + request.form.get('pesa') + " quilos"},
                        {"text": "Tu mede " + request.form.get('altura') + " centimetros de altura"}
                     ]
                   }
    return jsonify(json_response)

if __name__ == '__main__':
  #port = int(os.environ.get('PORT', 5000))
  #app.run(host='192.168.9.206', port=port)
  app.run()
