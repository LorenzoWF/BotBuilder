from flask import Flask, jsonify, request, render_template, safe_join, send_from_directory
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os
import json
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/teste', methods=['GET'])
def testeGet():
  print("teste")
  return"Tudo pronto!"

@app.route('/teste', methods=['POST'])
def testePost():
  content = request.json
  #python_obj = json.dumps(request.json)
  #python_obj = python_obj.replace("{", "")
  #python_obj = python_obj.replace("}", "")
  #python_obj = python_obj.replace('\"', "")
  #print(type(content))
  teste = ""
  for key, value in content.items() :
    teste = teste + key + "|"
    #print (key)


  #json_response = {"messages": [
    #                    {"text": "Tu tem " + content['idade'] + " anos"},
    #                    {"text": content['idade'] + " centrimetros de altura"},
    #                    {"text": "e pesa " + content['peso'] + " quilos"}
    #                ]
    #              }

  #json_response = [{"attachment":{
    #                    "type":"template",
    #                    "payload":{
    #                    "template_type":"generic",
    #                        "elements":[{
                                    #"messages": [
                                    #                      {"text": "Tu tem " + content['idade'] + " anos"},
                                    #                      {"text": content['idade'] + " centrimetros de altura"},
                                    #                      {"text": "e pesa " + content['peso'] + " quilos"}
                                    #                  ]

    #                            "title":"TESTE TITULO",
    #                            "subtitle": content
                                #"buttons":[{
                                #    "type":"web_url",
                                #    "url":"https://www.facebook.com/oferta/c2fa78cfdbc21585",
                                #    "title":"Aplicar"
                                #},
                                #{
                                #    "type":"web_url",
                                #    "url":"https://www.facebook.com/oferta/c2fa78cfdbc21585",
                                #    "title":"Mas Informacion"
                                #}]
    #                        }]
    #                    }
    #                }}]


  json_response = {"messages": [
                        {"text": teste}
                    ]
                  }

  return jsonify(json_response)

if __name__ == '__main__':
  #port = int(os.environ.get('PORT', 5000))
  #app.run(host='192.168.9.206', port=port)
  #app.run(host='localhost')
  #app.run(host='192.168.9.206')
  app.run()
