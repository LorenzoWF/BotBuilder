from flask import Flask, jsonify, request, render_template, safe_join, send_from_directory
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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

'''@app.route('/performance', methods=['POST'])
def responderDuvida():
    if request.form.get('performanceTexto') is None:
        return mensagemErro('Houve uma falha no envio dos dados. Tente novamente.')

    performanceTexto = request.form.get('performanceTexto')

    if performanceTexto.find('leve') orperformanceTexto.find('facil')'''


@app.route('/duvida', methods=['POST'])
def responderDuvida():
    if request.form.get('duvidaTexto') is None:
        return mensagemErro('Houve uma falha no envio dos dados. Tente novamente.')

    duvida = request.form.get('duvidaTexto')

    json_response = {"messages": [
                        {"text": 'Boa pergunta!'},
                        {"text": 'Infelizmente no momento eu não sei responder. Assim que eu obtiver a resposta eu te envio :)!'}
                     ]
                   }
    return jsonify(json_response)

'''@app.route('/performance', methods=['POST'])
def receberPerformance():
    return 1'''


@app.route('/img/<path>', methods=['GET'])
def uploaded_file(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)

@app.route('/exercicio', methods=['POST'])
def passarExercicio():

    if request.form.get('exercicio') is None:
        return mensagemErro('Houve um erro durante a coleta dos dados. Tente novamente.')

    exercicio = request.form.get('exercicio')

    if exercicio.find('agachamento') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | AGACHAMENTO LIVRE'
        exercicioDescricao  = 'No Agachamento livre:\nEm pé com a barra apoiada nos ombros e os pés afastados em distância igual à largura dos ombros.\nFlexione lentamente os joelhos até que as coxas fiquem paralelas ao chão.\nEstenda as pernas para retornar à posição inicial (em pé).'
        exercicioImagem     = 'agachamento_livre'

    elif exercicio.find('crucifixo') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | CRUCIFIXO INCLINADO'
        exercicioDescricao  = 'Para executar o Crucifixo Inclinado:\nSentado em um banco inclinado, comece com os halteres diretamente acima do tórax, com as palmas das mãos voltadas para dentro.\nAbaixe os halteres para fora, dobrando ligeiramente os cotovelos enquanto os pesos descem até o nível do tórax.\nLevante os halteres de volta, unindo-os na parte superior do exercício.'
        exercicioImagem     = 'crucifixo_inclinado'

    elif exercicio.find('desenvolvimento') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | DESENVOLVIMENTO COM BARRA'
        exercicioDescricao  = 'Para executar o Desenvolvimento com barra:\nSentado num banco, faça a pegada na barra com afastamento das mãos igual à largura dos ombros; palmas das mãos voltadas para frente.\nAbaixe lentamente o peso (à frente), até que toque a parte superior do tórax.\nImpulsione verticalmente para cima até que ocorra bloqueio dos cotovelos.'
        exercicioImagem     = 'desenvolvimento_barra'

    elif exercicio.find('leg press') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | LEG PRESS'
        exercicioDescricao  = 'Sente-se no aparelho de leg press e coloque os pés com afastamento na plataforma igual à largura dos ombros.\nLentamente, abaixe o peso até que os joelhos estejam com 90 graus de flexão.\nEmpurre o peso de volta à posição inicial; para isso, estenda as pernas.'
        exercicioImagem     = 'leg_press'

    elif exercicio.find('paralela') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | PARALELA'
        exercicioDescricao  = 'Para executar a Paralela:\nAgarre as barras paralelas, sustentando o corpo com os cotovelos estendidos e bloqueados.\nDobre os cotovelos, baixando o torso até que os braços fiquem paralelos ao chão.\nEmpurre o corpo de volta a posição inicial, isto é, até que seus cotovelos fiquem novamente estendidos.'
        exercicioImagem     = 'paralela'

    elif exercicio.find('puxador') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | PUXADOR FRONTAL ABERTO'
        exercicioDescricao  = 'Para executar o Puxador Frontal Aberto:\nFaça uma pegada na barra com o dorso das mãos voltado para cima; as mãos devem ficar a uma distância 15cm maior que a largura dos ombros.\nTracione a barra para baixo, até a parte superior do peito, contraindo os latíssimos.\nRetorne a barra à posição inicial, acima da cabeça.'
        exercicioImagem     = 'puxador_frontal'

    elif exercicio.find('rosca concentrada') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | ROSCA CONCENTRADA'
        exercicioDescricao  = 'Para executar a Rosca Concentrada:\nPosição sentada na extremidade do banco. Segure o halter fixo com o braço estendido; apoie o braço contra a parte interna da coxa.\nFaça o exercício de rosca com halter na direção do ombro, flexionando o cotovelo.\nAbaixe o halter de volta a posição inicial.'
        exercicioImagem     = 'rosca_concentrada'

    elif exercicio.find('rosca') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | ROSCA DIRETA COM BARRA'
        exercicioDescricao  = 'Para executar a Rosca direta com barra:\nSegure a barra com os braços estendidos; pegada com afastamento igual à distância entre os ombros e com o dorso das mãos voltado para baixo.\nLeve a barra até o nível dos ombros; para tanto, flexione os cotovelos.\nAbaixe a barra de volta à posição inicial, com os braços na posição estendida.'
        exercicioImagem     = 'rosca_direta_barra'

    elif exercicio.find('supino') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | SUPINO RETO – BARRA'
        exercicioDescricao  = 'Na posição deitada em um banco plano, faça uma pegada na barra com o dorso das mãos voltado para cima e o afastamento entre elas igual à distância entre os ombros.\nAbaixe lentamente o peso até tocar a parte média do tórax.\nEmpurre a barra diretamente para cima, até que ocorra bloqueio dos cotovelos.'
        exercicioImagem     = 'supino_reto'

    elif exercicio.find('triceps') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | TRICEPS CORDA'
        exercicioDescricao  = 'Para executar o Tríceps puxador:\nFaça a pegada com o dorso das mãos voltado para cima e na largura dos ombros em uma barra curta presa a uma polia alta.\nComece com a barra no nível do peito, cotovelos dobrados um pouco mais do que 90 graus.\nMantendo os braços estendidos, tracione a barra para baixo até que os cotovelos fiquem bloqueados.'
        exercicioImagem     = 'triceps_corda'

    elif exercicio.find('voador') >= 0:
        exercicioTitulo     = 'EXECUÇÃO | VOADOR'
        exercicioDescricao  = 'Segure os pegadores verticais, com os cotovelos ligeiramente dobrados.\nTracione simultaneamente os pegadores até que se toquem à frente de seu tórax.\nDeixe suas mãos retornarem à posição inicial, mantendo os cotovelos elevados.'
        exercicioImagem     = 'voador'

    else:
        return mensagemErro('Exercicio nao encontrado. Tente novamente.')

    json_response = {"messages": [
                        {"text": exercicioTitulo},
                        {"text": exercicioDescricao},
                        {"attachment": {
                                "type": "image",
                                "payload": {
                                  "url": request.base_url.replace('exercicio', '') + 'img/' + exercicioImagem + '.png'
                                }
                            }
                        }
                     ]
                   }

    return jsonify(json_response)

@app.route('/passarTreino', methods=['POST'])
def passarTreino():

    #FAZER LIKE PRA PEGAR O SEXO
    if request.form.get('sexoTexto') is None:
        return mensagemErro('Houve um erro durante a coleta dos dados. Tente novamente.')

    sexoTexto = request.form.get('sexoTexto')

    if sexoTexto.find('Masc') >= 0 or sexoTexto.find('masc') >= 0 or sexoTexto == 'M' or sexoTexto == 'm':
        sexo = 1
    elif sexoTexto.find('Fem') >= 0 or sexoTexto.find('fem') >= 0 or sexoTexto == 'F' or sexoTexto == 'f':
        sexo = 2
    else:
        return mensagemErro('Houve um erro durante a coleta dos dados. Tente novamente.')

    if request.form.get('peso') is None:
        return mensagemErro('O peso não pode ser menor que zero. Tente novamente.')
    elif int(request.form.get('peso')) <= 0:
        return mensagemErro('O peso não pode ser menor que zero. Tente novamente.')

    if request.form.get('idade') is None:
        return mensagemErro('A idade não pode ser menor que zero. Tente novamente.')
    elif int(request.form.get('idade')) <= 0:
        return mensagemErro('O idade não pode ser menor que zero. Tente novamente.')

    if request.form.get('altura') is None:
        return mensagemErro('A altura não pode ser menor que zero. Tente novamente.')
    elif int(request.form.get('altura')) <= 0:
        return mensagemErro('O altura não pode ser menor que zero. Tente novamente.')

    if request.form.get('vezesTreino') is None:
        return mensagemErro('O numero de dias para treino não pode ser igual ou menor que zero. Tente novamente.')
    elif int(request.form.get('vezesTreino')) < 3 or int(request.form.get('vezesTreino')) > 6:
        return mensagemErro('O numero de dias para treino não pode ser menor que 3 ou maior que 6. Tente novamente.')

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

    if sexo == 1: #MASCULINO
        if objetivo == 1: #HIPERTROFIA
            if vezesTreino == 3:
                mensagemVezesTreino = "Treino ABC (Masculino + Hipertrofia) > 4 séries de 8 a 12 repetições para cada exercício."
                mensagemExercicio   = "Primeiro dia: costas, bíceps." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Costas: Puxada frente, Puxada Triangulo, Remada Baixa, Remada curvada.' + '\n' + 'Bíceps: Rosca Direta, Rosca Alternada, Rosca Scott, Rosca Inversa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Peito: Supino reto, Crucifixo reto, Crucifixo inclinado, Voador.' + '\n' + 'Ombro: Desenvolvimento com halter, Elevação frontal com halter, Remada Invertida no pulley.'  + '\n' 'Triceps: Triceps Pulley, Triceps Pulley inverso, Rosca testa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Perna, Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Perna: Leg Press na máquina, Agachamento com Barra, Flexor, Extensor, abdutor e adutor.' + '\n' + 'Abdômen: prancha lateral (30 segundos de cada lado), abdominal lateral, Jackniff.' + '\n'

            elif vezesTreino == 4:
                mensagemVezesTreino = "Treino ABCD (Masculino + Hipertrofia)"
                mensagemExercicio   = "Primeiro dia: ombro, tríceps e abdominal." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento com halteres pela frente: 15,12,10,8 e 8 repetições.' + '\n' + 'Elevação lateral sentado: 8, 8, 8 e 6 repetições.' + '\n' + 'Encolhimento com halteres: 3 séries de 15 repetições.' + '\n' + 'Crucifixo inverso na máquina: 10, 8, 8 e 6 repetições' + '\n' + 'Tríceps testa com barra EZ ou W: 12, 10, 10 e 8 repetições.' + '\n' + 'Paralelas com peso: 4 repetições até a falha.' + '\n' + 'Elevação de pernas com peso: 4 séries de 20 repetições.'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Pernas.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento livre: 15, 12, 10, 10 e 8 repetições.' + '\n' + 'Leg press 45º: 20, 15, 10 e 8 repetições'  + '\n' 'Extensora: 15, 10, 10 e 8 repetições.' + '\n' + 'Gêmeos sentado (burrinho): 4 séries de 15 repetições.' + '\n' + 'Flexora: 10, 8, 8 e 8 repetições.' + '\n' + 'Gêmeos em pé unilateral: 12, 10, 10 e 10 repetições.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Peito e abdominal.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino reto com halteres: 15, 12, 10, 8 e 6 repetições.' + '\n' + 'Supino inclinado com barra: 10, 8, 8 e 6 repetições' + '\n' + 'Crossover: 4 séries de 8 repetições.' + '\n' + 'Crucifixo reto: 10, 8, 6 e 4 repetições.' + '\n' + 'Deck FST-7: 7 séries de 8 a 12 repetições com a maior carga possível e descanso de, no máximo, 20 segundos entre uma série e outra.' + '\n' + 'Abdominais na máquina ou cadeira: 30, 20, 20 e 15 repetições.'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: Costa, bíceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Pulley nuca: 12, 10, 8, 8 e 6 repetições.' + '\n' + 'Remada cavalinho: 10, 8, 8 e 6 repetiçõesself.' + '\n' + 'Pulley frente: 10, 8, 8 e 6 repetições.' + '\n' + 'Levantamento terra: 3 séries de 10 repetições.' + '\n' + 'Rosca direta com barra reta: 12, 10, 10 e 8 repetições.' + '\n' + 'Rosca martelo sentado alternado: 3 séries de 10 repetições.' + '\n'

            elif vezesTreino == 5:
                mensagemVezesTreino = "ABCDE (Masculino + Hipertrofia)"
                mensagemExercicio   = "Primeiro dia: Tríceps, bíceps e abdômen." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino fechado – 4 séries de 6 a 8 repetições.' + '\n' + 'Rosca francesa com halter – 4 séries de 10 a 12 repetições.' + '\n' + 'Pulley corda – 4 séries de 10 a 12 repetições.' + '\n' + 'Rosca direta – 4 séries de 6 a 8 repetições.' + '\n' + 'Rosca alternada – 4 séries de 10 a 12 repetições.' + '\n' + 'Rosca martelo – 4 séries de 10 a 12 repetições.' + '\n' + 'Abdominal no pulley – 3 séries de 10 repetições.' + '\n' + 'Abdominal com carga (ou uma variação da sua escolha, mas que use carga) – 3 séries de 10 repetições.'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Pernas e Panturrilhas.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento – 4 x 6 a 8.' + '\n' + 'Legpress – 4 x 10.'  + '\n' 'Stiff – 3×10.' + '\n' + 'Extensora 3 x 12.' + '\n' + 'Flexora 3 x 12.' + '\n' + 'Elevação de gêmeos sentada – 4 x 10 a 15.' + '\n' + 'Elevação de gêmeos no legpress – 4 x 10 a 15.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Ombros, Trapézio e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento com barra sentado – 4 x 6 a 8.' + '\n' + 'Elevação lateral – 4 x 10.' + '\n' + 'Crucifixo inverso – 4 x 10.' + '\n' + 'Encolhimento com barra – 4 x 6 a 8.' + '\n' + 'Encolhimento com halteres – 4 x 10 a 12.' + '\n' + 'Abdominal no pulley – 3 séries de 10 repetições.' + '\n' + 'Abdominal com carga (ou uma variação da sua escolha, mas que use carga) – 3 séries de 10 repetições' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: Costas e panturrilhas.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Barra-fixa 4 x falha.' + '\n' + 'Remada curvada 4 x 10' + '\n' + 'Puxada no pulley usando o pegador neutro 4 x 10×12.' + '\n' + 'Levantamento terra 4 x 8 a 10.' + '\n' + 'Barra-fixa 4 x falha.' + '\n' + 'Remada curvada 4 x 10.' + '\n' + 'Puxada no pulley usando o pegador neutro 4 x 10×12' + '\n' + 'Levantamento terra 4 x 8 a 10' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quinto dia: Peitoral e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino reto – 4 x 6 a 8.' + '\n' + 'Supino inclinado – 4 x 10.' + '\n' + 'Paralelas – 4 x falha.' + '\n' + 'Crucifixo ou crossover – 4 x 10 a 12.' + '\n' + 'Abdominal no pulley – 3 séries de 10 repetições.' + '\n' + 'Abdominal com carga (ou uma variação da sua escolha, mas que use carga) – 3 séries de 10 repetições' + '\n'

            elif vezesTreino == 6:
                mensagemVezesTreino = "Treino ABCABC (Masculino + Hipertrofia) > 4 séries de 8 a 12 repetições para cada exercício."
                mensagemExercicio   = "Primeiro dia: costas, bíceps." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Costas: Puxada frente, Puxada Triangulo, Remada Baixa, Remada curvada.' + '\n' + 'Bíceps: Rosca Direta, Rosca Alternada, Rosca Scott, Rosca Inversa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Peito: Supino reto, Crucifixo reto, Crucifixo inclinado, Voador.' + '\n' + 'Ombro: Desenvolvimento com halter, Elevação frontal com halter, Remada Invertida no pulley.' + '\n' + 'Triceps: Triceps Pulley, Triceps Pulley inverso, Rosca testa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Perna, Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Perna: Leg Press na máquina, Agachamento com Barra, Flexor, Extensor, abdutor e adutor.' + '\n' + 'Abdômen: prancha lateral (30 segundos de cada lado), abdominal lateral, Jackniff.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: costas, bíceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Costas: Puxada frente, Puxada Triangulo, Remada Baixa, Remada curvada.' + '\n' + 'Bíceps: Rosca Direta, Rosca Alternada, Rosca Scott, Rosca Inversa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quinto dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Peito: Supino reto, Crucifixo reto, Crucifixo inclinado, Voador.' + '\n' + 'Ombro: Desenvolvimento com halter, Elevação frontal com halter, Remada Invertida no pulley.' + '\n' + 'Triceps: Triceps Pulley, Triceps Pulley inverso, Rosca testa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Sexto dia: Perna, Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Perna: Leg Press na máquina, Agachamento com Barra, Flexor, Extensor, abdutor e adutor.' + '\n' + 'Abdômen: prancha lateral (30 segundos de cada lado), abdominal lateral, Jackniff.' + '\n'

        elif objetivo == 2: #EMAGRECIMENTO
            if vezesTreino == 3:
                mensagemVezesTreino = "Treino ABC (Masculino + Emagrecimento) > 3 séries de 8 a 12 repetições para cada exercício e após 30 minutos de aeróbio, na esteira ou bicicleta."
                mensagemExercicio   = "Primeiro dia: costas, bíceps." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Costas: Puxada frente, Puxada Triangulo, Remada Baixa, Remada curvada.' + '\n' + 'Bíceps: Rosca Direta, Rosca Alternada, Rosca Scott, Rosca Inversa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Peito: Supino reto, Crucifixo reto, Crucifixo inclinado, Voador.' + '\n' + 'Ombro: Desenvolvimento com halter, Elevação frontal com halter, Remada Invertida no pulley.'  + '\n' 'Triceps: Triceps Pulley, Triceps Pulley inverso, Rosca testa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Perna, Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Perna: Leg Press na máquina, Agachamento com Barra, Flexor, Extensor, abdutor e adutor.' + '\n' + 'Abdômen: prancha lateral (30 segundos de cada lado), abdominal lateral, Jackniff.' + '\n'

            elif vezesTreino == 4:
                mensagemVezesTreino = "Treino ABCD (Masculino + emagrecimento) > 3 séries de 8 a 12 repetições para cada exercício e após 30 minutos de aeróbio, na esteira ou bicicleta."
                mensagemExercicio   = "Primeiro dia: ombro, tríceps e abdominal." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento com halteres pela frente: 15,12,10,8 e 8 repetições.' + '\n' + 'Elevação lateral sentado: 8, 8, 8 e 6 repetições.' + '\n' + 'Encolhimento com halteres: 3 séries de 15 repetições.' + '\n' + 'Crucifixo inverso na máquina: 10, 8, 8 e 6 repetições' + '\n' + 'Tríceps testa com barra EZ ou W: 12, 10, 10 e 8 repetições.' + '\n' + 'Paralelas com peso: 4 repetições até a falha.' + '\n' + 'Elevação de pernas com peso: 4 séries de 20 repetições.'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Pernas.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento livre: 15, 12, 10, 10 e 8 repetições.' + '\n' + 'Leg press 45º: 20, 15, 10 e 8 repetições'  + '\n' 'Extensora: 15, 10, 10 e 8 repetições.' + '\n' + 'Gêmeos sentado (burrinho): 4 séries de 15 repetições.' + '\n' + 'Flexora: 10, 8, 8 e 8 repetições.' + '\n' + 'Gêmeos em pé unilateral: 12, 10, 10 e 10 repetições.'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Peito e abdominal.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino reto com halteres: 15, 12, 10, 8 e 6 repetições.' + '\n' + 'Supino inclinado com barra: 10, 8, 8 e 6 repetições' + '\n' + 'Crossover: 4 séries de 8 repetições.' + '\n' + 'Crucifixo reto: 10, 8, 6 e 4 repetições.' + '\n' + 'Deck FST-7: 7 séries de 8 a 12 repetições com a maior carga possível e descanso de, no máximo, 20 segundos entre uma série e outra.' + '\n' + 'Abdominais na máquina ou cadeira: 30, 20, 20 e 15 repetições.'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: Costa, bíceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Pulley nuca: 12, 10, 8, 8 e 6 repetições.' + '\n' + 'Remada cavalinho: 10, 8, 8 e 6 repetiçõesself.' + '\n' + 'Pulley frente: 10, 8, 8 e 6 repetições.' + '\n' + 'Levantamento terra: 3 séries de 10 repetições.' + '\n' + 'Rosca direta com barra reta: 12, 10, 10 e 8 repetições.' + '\n' + 'Rosca martelo sentado alternado: 3 séries de 10 repetições.'

            elif vezesTreino == 5:
                mensagemVezesTreino = "Treino ABCDE (Masculino + emagrecimento) > 3 séries de 8 a 12 repetições para cada exercício e após 30 minutos de aeróbio, na esteira ou bicicleta."
                mensagemExercicio   = "Primeiro dia: Tríceps, bíceps e abdômen." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino fechado – 4 séries de 6 a 8 repetições.' + '\n' + 'Rosca francesa com halter – 4 séries de 10 a 12 repetições.' + '\n' + 'Pulley corda – 4 séries de 10 a 12 repetições.' + '\n' + 'Rosca direta – 4 séries de 6 a 8 repetições.' + '\n' + 'Rosca alternada – 4 séries de 10 a 12 repetições.' + '\n' + 'Rosca martelo – 4 séries de 10 a 12 repetições.' + '\n' + 'Abdominal no pulley – 3 séries de 10 repetições.' + '\n' + 'Abdominal com carga (ou uma variação da sua escolha, mas que use carga) – 3 séries de 10 repetições.'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Pernas e Panturrilhas.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento – 4 x 6 a 8.' + '\n' + 'Legpress – 4 x 10.'  + '\n' 'Stiff – 3×10.' + '\n' + 'Extensora 3 x 12.' + '\n' + 'Flexora 3 x 12.' + '\n' + 'Elevação de gêmeos sentada – 4 x 10 a 15.' + '\n' + 'Elevação de gêmeos no legpress – 4 x 10 a 15.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Ombros, Trapézio e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento com barra sentado – 4 x 6 a 8.' + '\n' + 'Elevação lateral – 4 x 10.' + '\n' + 'Crucifixo inverso – 4 x 10.' + '\n' + 'Encolhimento com barra – 4 x 6 a 8.' + '\n' + 'Encolhimento com halteres – 4 x 10 a 12.' + '\n' + 'Abdominal no pulley – 3 séries de 10 repetições.' + '\n' + 'Abdominal com carga (ou uma variação da sua escolha, mas que use carga) – 3 séries de 10 repetições' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: Costas e panturrilhas.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Barra-fixa 4 x falha.' + '\n' + 'Remada curvada 4 x 10' + '\n' + 'Puxada no pulley usando o pegador neutro 4 x 10×12.' + '\n' + 'Levantamento terra 4 x 8 a 10.' + '\n' + 'Barra-fixa 4 x falha.' + '\n' + 'Remada curvada 4 x 10.' + '\n' + 'Puxada no pulley usando o pegador neutro 4 x 10×12' + '\n' + 'Levantamento terra 4 x 8 a 10' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quinto dia: Peitoral e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino reto – 4 x 6 a 8.' + '\n' + 'Supino inclinado – 4 x 10.' + '\n' + 'Paralelas – 4 x falha.' + '\n' + 'Crucifixo ou crossover – 4 x 10 a 12.' + '\n' + 'Abdominal no pulley – 3 séries de 10 repetições.' + '\n' + 'Abdominal com carga (ou uma variação da sua escolha, mas que use carga) – 3 séries de 10 repetições' + '\n'

            elif vezesTreino == 6:
                mensagemVezesTreino = "Treino ABCABC (Masculino + Emagrecimento) > 3 séries de 8 a 12 repetições para cada exercício e após 30 minutos de aeróbio, na esteira ou bicicleta."
                mensagemExercicio   = "Primeiro dia: costas, bíceps." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Costas: Puxada frente, Puxada Triangulo, Remada Baixa, Remada curvada.' + '\n' + 'Bíceps: Rosca Direta, Rosca Alternada, Rosca Scott, Rosca Inversa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Peito: Supino reto, Crucifixo reto, Crucifixo inclinado, Voador.' + '\n' + 'Ombro: Desenvolvimento com halter, Elevação frontal com halter, Remada Invertida no pulley.' + '\n' + 'Triceps: Triceps Pulley, Triceps Pulley inverso, Rosca testa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Perna, Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Perna: Leg Press na máquina, Agachamento com Barra, Flexor, Extensor, abdutor e adutor.' + '\n' + 'Abdômen: prancha lateral (30 segundos de cada lado), abdominal lateral, Jackniff.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: costas, bíceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Costas: Puxada frente, Puxada Triangulo, Remada Baixa, Remada curvada.' + '\n' + 'Bíceps: Rosca Direta, Rosca Alternada, Rosca Scott, Rosca Inversa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quinto dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Peito: Supino reto, Crucifixo reto, Crucifixo inclinado, Voador.' + '\n' + 'Ombro: Desenvolvimento com halter, Elevação frontal com halter, Remada Invertida no pulley.' + '\n' + 'Triceps: Triceps Pulley, Triceps Pulley inverso, Rosca testa.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Sexto dia: Perna, Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Perna: Leg Press na máquina, Agachamento com Barra, Flexor, Extensor, abdutor e adutor.' + '\n' + 'Abdômen: prancha lateral (30 segundos de cada lado), abdominal lateral, Jackniff.' + '\n'

    elif sexo == 2: #FEMININO
        if objetivo == 1: #HIPERTROFIA
            if vezesTreino == 3:
                mensagemVezesTreino = "Treino ABC (Feminino + Hipertrofia)"
                mensagemExercicio   = "Primeiro dia: Peito e costas." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino inclinado com barra (12 – 10 – 8 – 6 séries), Barra fixa ( 12 – 10 – 8), Crucifixo Reto (8 – 8 – 6 – 6), Remada Cavalinho (8 – 8 – 6 – 4), Cross Over (3x8), Serrote Unilateral (3x10).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Pernas, Panturrilha e Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento Livre (15 – 12 – 10 – 8 – 6 – 4), Leg Press 45º (15 – 12 – 10 – 8), Flexora (8 – 8 – 6 – 6), Extensora (12 – 10 – 8 – 6), Levantamento terra (10 – 10 – 8 – 8), Gêmeos Sentado (15 – 12 – 10 – 8 – 6), abdominal com corda (12 – 10 – 8), Elevação de pernas declinado (3x25).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Ombro, Bíceps, Tríceps e trapézio.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento militar com halteres (12 – 10 – 8 – 6), Elevação lateral sentado (8 – 8 – 6), Elevação frontal (10 – 8 – 8), Rosca direta com barra reta (10 – 8 – 6), Rosca concentrada (2x8), Extensão de tríceps francês (4x8), Tríceps pulley com barra reta (10 – 8 – 6 – 4), Encolhimento com barra por trás ( 12 – 8 – 6 – 4).' + '\n'

            elif vezesTreino == 4:
                mensagemVezesTreino = "Treino ABCD (Feminino + Hipertrofia)"
                mensagemExercicio   = "Primeiro dia: quadríceps, panturrilhas e abdômen." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento Livre 3 x 8.' + '\n' + 'Leg Press 45º 3 x 8.' + '\n' + 'Flexora 3 x 8.' + '\n' + 'Extensora 3 x 8.' + '\n' + 'Levantamento terra 3 x 8.' + '\n' + 'Gêmeos Sentado 3 x 8.' + '\n' + 'Abdominal com corda 3 x 8.' + '\n' + 'Elevação de pernas declinado 3x25.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Crucifixo 3 x 8.' + '\n' + 'Supino 3 x 8.' + '\n' 'Voador 3 x 8.' + '\n' + 'Tríceps Cross Over pegada inversa 3 x 8.' + '\n' + 'Tríceps Corda 3 x 8.' + '\n' + 'Tríceps Frances 3 x 8.' + '\n' + 'Arnold Press 3 x 8.' + '\n' + 'Elevação lateral de ombro no banco (posterior) 3 x 8.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: glúteos, panturrilha e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Flexora deitada 3 x 10.' + '\n' + 'Meio levantamento terra 3 x 10.' + '\n' + 'Bom dia 3 x 10.' + '\n' + 'Glúteo Cross Over 3 x 10.' + '\n' + 'Panturrilha Sentada 3 x 8.' + '\n' + 'Panturrilha Leg 45 º 3 x 8.' + '\n' + 'Abdominais colchonete Circuito' + '\n' + 'Abdominais Cross Over Carga máxima.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: costas e bíceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Remada baixa 3x10.' + '\n' + 'Puxador alta frente 3x10.' + '\n' + 'Voador Inverso 3x10.' + '\n' + 'Cavalinho 3x10.' + '\n' + 'Rosca direta halteres 3x10.' + '\n' + 'Rosca concentrada barra W 3x10.' + '\n' + 'Rosca direta na barra H 3x10.' + '\n'

            elif vezesTreino == 5:
                mensagemVezesTreino = "Treino ABCDE (Feminino + hipertrofia)"
                mensagemExercicio   = "Primeiro dia: anterior da coxa, panturrilhas e abdômen" + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Extensora 3 x Até a exaustão.' + '\n' + '45º 3 x Até a exaustão.' + '\n' + 'Agachamento Livre 4 x 10.' + '\n' + 'Agachamento Hack 3 x 10.' + '\n' + 'Avanço com barra 3 x 10.' + '\n' + 'Elevação gêmeos hack 3 x 10.' + '\n' + 'Panturrilha sentada. 3 x 10.' + '\n' + 'Abdominais Cross Over Carga máxima.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Crucifixo 3 x 8.' + '\n' + 'Supino 3 x 8.'  + '\n' 'Voador 3 x 8.' + '\n' + 'Tríceps Cross Over pegada inversa 3 x 8.' + '\n' + 'Tríceps Corda 3 x 8.' + '\n' + 'Tríceps Frances 3 x 8.' + '\n' + 'Arnold Press 3 x 8.' + '\n' + 'Elevação lateral de ombro no banco (posterior) 3 x 8' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: glúteos, panturrilha e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Flexora Deitada 3 x 10.' + '\n' + 'Meio levantamento terra 3 x 10.' + '\n' + 'Bom dia 3 x 10.' + '\n' + 'Glúteo Cross Over 3 x 10.' + '\n' + 'Panturrilha Sentada 3 x 8.' + '\n' + 'Panturilha Leg 45 º 3 x 8.' + '\n' + 'Abdominais colchonete Circuito.' + '\n' + 'Abdominais Cross Over Carga máxima' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: costa e bíceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Remada baixa 3x10.' + '\n' + 'Puxador alta frente 3x10' + '\n' + 'Voador Inverso 3x10.' + '\n' + 'Cavalinho 3x10.' + '\n' + 'Rosca direta halteres 3x10.' + '\n' + 'Rosca concentrada barra W 3x10.' + '\n' + 'Rosca direta na barra H 3x10.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quinto dia: posterior da coxa, panturrilha e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Stiff 3 x 10.' + '\n' + 'Afundo no Step 3 x 10.' + '\n' + 'Agachamento com bola 3 x 10.' + '\n' + 'Adução 3 x 10.' + '\n' + 'Abdução 3 x 10.' + '\n' + 'Panturrilha sentada 3 x 10.' + '\n' + 'Elevação gêmeos step Até exaustão' + '\n' + 'Abdominais prancha' + '\n'

            elif vezesTreino == 6:
                mensagemVezesTreino = "Treino ABCABC (Feminino + Hipertrofia)"
                mensagemExercicio   = "Primeiro dia: Peito e costas." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino inclinado com barra (12 – 10 – 8 – 6 séries), Barra fixa ( 12 – 10 – 8), Crucifixo Reto (8 – 8 – 6 – 6), Remada Cavalinho (8 – 8 – 6 – 4), Cross Over (3x8), Serrote Unilateral (3x10).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Pernas, Panturrilha e Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento Livre (15 – 12 – 10 – 8 – 6 – 4), Leg Press 45º (15 – 12 – 10 – 8), Flexora (8 – 8 – 6 – 6), Extensora (12 – 10 – 8 – 6), Levantamento terra (10 – 10 – 8 – 8), Gêmeos Sentado (15 – 12 – 10 – 8 – 6), abdominal com corda (12 – 10 – 8), Elevação de pernas declinado (3x25).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Ombro, Bíceps, Tríceps e trapézio.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento militar com halteres (12 – 10 – 8 – 6), Elevação lateral sentado (8 – 8 – 6), Elevação frontal (10 – 8 – 8), Rosca direta com barra reta (10 – 8 – 6), Rosca concentrada (2x8), Extensão de tríceps francês (4x8), Tríceps pulley com barra reta (10 – 8 – 6 – 4), Encolhimento com barra por trás ( 12 – 8 – 6 – 4).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: Peito e costas.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino inclinado com barra (12 – 10 – 8 – 6 séries), Barra fixa ( 12 – 10 – 8), Crucifixo Reto (8 – 8 – 6 – 6), Remada Cavalinho (8 – 8 – 6 – 4), Cross Over (3x8), Serrote Unilateral (3x10).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quinto dia: Pernas, Panturrilha e Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento Livre (15 – 12 – 10 – 8 – 6 – 4), Leg Press 45º (15 – 12 – 10 – 8), Flexora (8 – 8 – 6 – 6), Extensora (12 – 10 – 8 – 6), Levantamento terra (10 – 10 – 8 – 8), Gêmeos Sentado (15 – 12 – 10 – 8 – 6), abdominal com corda (12 – 10 – 8), Elevação de pernas declinado (3x25).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Sexto dia: Ombro, Bíceps, Tríceps e trapézio.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento militar com halteres (12 – 10 – 8 – 6), Elevação lateral sentado (8 – 8 – 6), Elevação frontal (10 – 8 – 8), Rosca direta com barra reta (10 – 8 – 6), Rosca concentrada (2x8), Extensão de tríceps francês (4x8), Tríceps pulley com barra reta (10 – 8 – 6 – 4), Encolhimento com barra por trás ( 12 – 8 – 6 – 4).' + '\n'

        elif objetivo == 2: #EMAGRECIMENTO
            if vezesTreino == 3:
                mensagemVezesTreino = "Treino ABC (Feminino + Emagrecimento) + redução das séries pela metade e 30 minutos de aeróbio após o treino podendo ser esteira ou bicicleta."
                mensagemExercicio   = "Primeiro dia: Peito e costas." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino inclinado com barra (12 – 10 – 8 – 6 séries), Barra fixa ( 12 – 10 – 8), Crucifixo Reto (8 – 8 – 6 – 6), Remada Cavalinho (8 – 8 – 6 – 4), Cross Over (3x8), Serrote Unilateral (3x10).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Pernas, Panturrilha e Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento Livre (15 – 12 – 10 – 8 – 6 – 4), Leg Press 45º (15 – 12 – 10 – 8), Flexora (8 – 8 – 6 – 6), Extensora (12 – 10 – 8 – 6), Levantamento terra (10 – 10 – 8 – 8), Gêmeos Sentado (15 – 12 – 10 – 8 – 6), abdominal com corda (12 – 10 – 8), Elevação de pernas declinado (3x25).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Ombro, Bíceps, Tríceps e trapézio.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento militar com halteres (12 – 10 – 8 – 6), Elevação lateral sentado (8 – 8 – 6), Elevação frontal (10 – 8 – 8), Rosca direta com barra reta (10 – 8 – 6), Rosca concentrada (2x8), Extensão de tríceps francês (4x8), Tríceps pulley com barra reta (10 – 8 – 6 – 4), Encolhimento com barra por trás ( 12 – 8 – 6 – 4).' + '\n'

            elif vezesTreino == 4:
                mensagemVezesTreino = "Treino ABCD (Feminino + Emagrecimento) > séries de 8 a 12 repetições para cada exercício e após 30 minutos de aeróbio, na esteira ou bicicleta."
                mensagemExercicio   = "Primeiro dia: quadríceps, panturrilhas e abdômen." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento Livre 3 x 8.' + '\n' + 'Leg Press 45º 3 x 8.' + '\n' + 'Flexora 3 x 8.' + '\n' + 'Extensora 3 x 8.' + '\n' + 'Levantamento terra 3 x 8.' + '\n' + 'Gêmeos Sentado 3 x 8.' + '\n' + 'Abdominal com corda 3 x 8.' + '\n' + 'Elevação de pernas declinado 3x25.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Crucifixo 3 x 8.' + '\n' + 'Supino 3 x 8.' + '\n' 'Voador 3 x 8.' + '\n' + 'Tríceps Cross Over pegada inversa 3 x 8.' + '\n' + 'Tríceps Corda 3 x 8.' + '\n' + 'Tríceps Frances 3 x 8.' + '\n' + 'Arnold Press 3 x 8.' + '\n' + 'Elevação lateral de ombro no banco (posterior) 3 x 8.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: glúteos, panturrilha e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Flexora deitada 3 x 10.' + '\n' + 'Meio levantamento terra 3 x 10.' + '\n' + 'Bom dia 3 x 10.' + '\n' + 'Glúteo Cross Over 3 x 10.' + '\n' + 'Panturrilha Sentada 3 x 8.' + '\n' + 'Panturrilha Leg 45 º 3 x 8.' + '\n' + 'Abdominais colchonete Circuito' + '\n' + 'Abdominais Cross Over Carga máxima.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: costas e bíceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Remada baixa 3x10.' + '\n' + 'Puxador alta frente 3x10.' + '\n' + 'Voador Inverso 3x10.' + '\n' + 'Cavalinho 3x10.' + '\n' + 'Rosca direta halteres 3x10.' + '\n' + 'Rosca concentrada barra W 3x10.' + '\n' + 'Rosca direta na barra H 3x10.' + '\n'

            elif vezesTreino == 5:
                mensagemVezesTreino = "Treino ABCDE (Feminino + emagrecimento) > 2 séries de 8 a 12 repetições para cada exercício e após 30 minutos de aeróbio, na esteira ou bicicleta."
                mensagemExercicio   = "Primeiro dia: anterior da coxa, panturrilhas e abdômen" + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Extensora 3 x Até a exaustão.' + '\n' + '45º 3 x Até a exaustão.' + '\n' + 'Agachamento Livre 4 x 10.' + '\n' + 'Agachamento Hack 3 x 10.' + '\n' + 'Avanço com barra 3 x 10.' + '\n' + 'Elevação gêmeos hack 3 x 10.' + '\n' + 'Panturrilha sentada. 3 x 10.' + '\n' + 'Abdominais Cross Over Carga máxima.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Peito, ombro e tríceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Crucifixo 3 x 8.' + '\n' + 'Supino 3 x 8.'  + '\n' 'Voador 3 x 8.' + '\n' + 'Tríceps Cross Over pegada inversa 3 x 8.' + '\n' + 'Tríceps Corda 3 x 8.' + '\n' + 'Tríceps Frances 3 x 8.' + '\n' + 'Arnold Press 3 x 8.' + '\n' + 'Elevação lateral de ombro no banco (posterior) 3 x 8' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: glúteos, panturrilha e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Flexora Deitada 3 x 10.' + '\n' + 'Meio levantamento terra 3 x 10.' + '\n' + 'Bom dia 3 x 10.' + '\n' + 'Glúteo Cross Over 3 x 10.' + '\n' + 'Panturrilha Sentada 3 x 8.' + '\n' + 'Panturilha Leg 45 º 3 x 8.' + '\n' + 'Abdominais colchonete Circuito.' + '\n' + 'Abdominais Cross Over Carga máxima' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: costa e bíceps.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Remada baixa 3x10.' + '\n' + 'Puxador alta frente 3x10' + '\n' + 'Voador Inverso 3x10.' + '\n' + 'Cavalinho 3x10.' + '\n' + 'Rosca direta halteres 3x10.' + '\n' + 'Rosca concentrada barra W 3x10.' + '\n' + 'Rosca direta na barra H 3x10.' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quinto dia: posterior da coxa, panturrilha e abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Stiff 3 x 10.' + '\n' + 'Afundo no Step 3 x 10.' + '\n' + 'Agachamento com bola 3 x 10.' + '\n' + 'Adução 3 x 10.' + '\n' + 'Abdução 3 x 10.' + '\n' + 'Panturrilha sentada 3 x 10.' + '\n' + 'Elevação gêmeos step Até exaustão' + '\n' + 'Abdominais prancha' + '\n'

            elif vezesTreino == 6:
                mensagemVezesTreino = "Treino ABCABC (Feminino + Emagrecimento) > que redução das séries pela metade e 30 minutos de aeróbio após o treino, podendo ser esteira ou bicicleta."
                mensagemExercicio   = "Primeiro dia: Peito e costas." + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino inclinado com barra (12 – 10 – 8 – 6 séries), Barra fixa ( 12 – 10 – 8), Crucifixo Reto (8 – 8 – 6 – 6), Remada Cavalinho (8 – 8 – 6 – 4), Cross Over (3x8), Serrote Unilateral (3x10).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Segundo dia: Pernas, Panturrilha e Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento Livre (15 – 12 – 10 – 8 – 6 – 4), Leg Press 45º (15 – 12 – 10 – 8), Flexora (8 – 8 – 6 – 6), Extensora (12 – 10 – 8 – 6), Levantamento terra (10 – 10 – 8 – 8), Gêmeos Sentado (15 – 12 – 10 – 8 – 6), abdominal com corda (12 – 10 – 8), Elevação de pernas declinado (3x25).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Terceiro dia: Ombro, Bíceps, Tríceps e trapézio.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento militar com halteres (12 – 10 – 8 – 6), Elevação lateral sentado (8 – 8 – 6), Elevação frontal (10 – 8 – 8), Rosca direta com barra reta (10 – 8 – 6), Rosca concentrada (2x8), Extensão de tríceps francês (4x8), Tríceps pulley com barra reta (10 – 8 – 6 – 4), Encolhimento com barra por trás ( 12 – 8 – 6 – 4).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quarto dia: Peito e costas.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Supino inclinado com barra (12 – 10 – 8 – 6 séries), Barra fixa ( 12 – 10 – 8), Crucifixo Reto (8 – 8 – 6 – 6), Remada Cavalinho (8 – 8 – 6 – 4), Cross Over (3x8), Serrote Unilateral (3x10).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Quinto dia: Pernas, Panturrilha e Abdômen.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Agachamento Livre (15 – 12 – 10 – 8 – 6 – 4), Leg Press 45º (15 – 12 – 10 – 8), Flexora (8 – 8 – 6 – 6), Extensora (12 – 10 – 8 – 6), Levantamento terra (10 – 10 – 8 – 8), Gêmeos Sentado (15 – 12 – 10 – 8 – 6), abdominal com corda (12 – 10 – 8), Elevação de pernas declinado (3x25).' + '\n'

                mensagemExercicio += '\n'
                mensagemExercicio += 'Sexto dia: Ombro, Bíceps, Tríceps e trapézio.' + '\n'

                if local == 2: #NA ACADEMIA
                    mensagemExercicio += 'Desenvolvimento militar com halteres (12 – 10 – 8 – 6), Elevação lateral sentado (8 – 8 – 6), Elevação frontal (10 – 8 – 8), Rosca direta com barra reta (10 – 8 – 6), Rosca concentrada (2x8), Extensão de tríceps francês (4x8), Tríceps pulley com barra reta (10 – 8 – 6 – 4), Encolhimento com barra por trás ( 12 – 8 – 6 – 4).' + '\n'

    mensagemMotivacional = "Agora é HORA DO SHOW! BIIIIRRLLL!"

    json_response = {
                    "set_attributes":
                    {
                      "mensagemVezesTreino": mensagemVezesTreino,
                      "mensagemExercicio": mensagemExercicio
                    },
                    "messages": [
                        {"text": mensagemInicial},
                        {"text": mensagemVezesTreino},
                        {"text": mensagemExercicio},
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
