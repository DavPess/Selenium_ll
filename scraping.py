import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd

options = Options()
#options.add_argument('--headless')
options.add_argument('window-size=400, 800')

navegador = webdriver.Chrome(options=options)

navegador.get('https://www.airbnb.com.br/')

sleep(2)

input_place = navegador.find_element_by_tag_name('input')
input_place.send_keys('São Paulo')
input_place.submit()

sleep(0.5)

button_stay = navegador.find_element_by_css_selector('button > img')
button_stay.click()

nextButton = navegador.find_elements_by_tag_name('button')[-1]
nextButton.click()

adultButton = navegador.find_elements_by_css_selector('button > span > svg > path [d="m2 16h25m-14-14v28"]')[0]
adultButton.click()
sleep(1)
adultButton.click()
sleep(1)

searchButton = navegador.find_elements_by_tag_name('button')[-1]
searchButton.click()

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')

dados_hospedagens = []

hospedagens = site.findAll('div', attrs={'itemprop': 'itemListElement'})
    
for hospedagem in hospedagens:

    #print(hospedagem.prettify())

    hospedagem_descricao = hospedagem('meta', attrs={'itemprop': 'name'})
    hospedagem_url= hospedagem('meta', attrs={'itemprop': 'url'})
    
    hospedagem_descricao = hospedagem_descricao['content']
    hospedagem_url = hospedagem_url['content']

    print('Descrição: ', hospedagem_descricao)
    print('URL: ', hospedagem_url)

    hospedagem_detalhes = hospedagem.find('div', attrs={'style': 'margin-bottom: 2px;'}).findAll('li')

    #hospedagem_detalhes = hospedagem_detalhes[0].text + hospedagem_detalhes[1].text
    hospedagem_detalhes = ''.join([detalhe.text for detalhe in hospedagem_detalhes])
    print(hospedagem_detalhes)

    preco = hospedagem.findAll('span')[-1].text

    print('Preço da hospedagem:', preco)
    
    print()
    
    dados_hospedagens.append([hospedagem_descricao, hospedagem_url, hospedagem_detalhes, preco])

dados = pd.DataFrame(dados_hospedagens, columns=['Descrição', 'URL', 'Detalhes', 'Preço'])

dados.to_csv('hospedagens.csv', index=False)