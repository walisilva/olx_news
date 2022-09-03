url = 'https://pb.olx.com.br/paraiba/joao-pessoa/imoveis/aluguel/casas?pe=1000&ros=2&sd=4834&sd=4833&sd=4827&sd=4842&sd=4847&sd=4843' # url de exemplo, modifique para a sua url
tg_destino = 'seu_id' # aqui o id do seu usuario, canal ou grupo

from time import sleep
import requests
from bs4 import BeautifulSoup

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import telebot

CHAVE_API="sua_chave_aqui" # Chave do seu bot criado no telegram (bot father)
bot = telebot.TeleBot(CHAVE_API)

ct = 1 # contador, não modificar

ultimo = '' # armazenar ultima informaçao, nao modificar
send = False # armazenar informacao de envio ou nao de mensagem telegram

tm = 5 # padrao de tempo de atualizacao em minutos

while(True):
    
    hdr = {'User-Agent': 'Mozilla/5.0'} # simular navegador mozila
    response = requests.get(url, verify=False, headers=hdr)
    doc = BeautifulSoup(response.text, 'html.parser')

    titles = doc.select('span[color="grayscale.darker"]')  # seletor para o caminho dos resultados na pagina

    if not titles:
        print('\nErro ao obter dados da página.')
        tm = 1
    else:
        tm = 5
        resultados = str(titles[0].text).split(' de ')
        res = resultados[1]+':'

        if ultimo == '':
            ultimo = resultados[1]
            send = False
        else:
            if ultimo != resultados[1]:
                ultimo = resultados[1]
                send = True

        titles = doc.select('#column-main-content > div.h3us20-6.iLWqoT > div > div > div > div.sc-gPWkxV.sc-1ncgzjx-0.uvMTU > div > div.sc-gPWkxV.sc-1a202fr-0.dpPMei > div') # seletor para os detalhes do resultado da consulta - Atualizado em 2022-09-03
        resultados = titles[0].contents

        for r in resultados:
            res += '\n- '+r.text.upper()
        
        print()
        print('Tentativa Num... ' + str(ct))
        print()
        print(res)

        # send = True
        
        if send: 
            bot.send_message(tg_destino, res)
            print('\n>> Telegram enviado.')
        else:
            print('\n>> Telegram NãO enviado')

    ct += 1
    send = False

    sleep(60 * tm)
