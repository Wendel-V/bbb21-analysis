from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import pandas as pd
from datetime import date
import os

def instaData(user, today):
    # Puxando a página:
    
    url = 'https://socialblade.com/instagram/user/' + user
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}

    try:
        req = Request(url, headers = headers)
        response = urlopen(req)
        html = response.read()

    except HTTPError as e:
        print(e.status, e.reason)

    except URLError as e:
        print(e.reason)

    # Tratando a pagina
    html = html.decode('utf-8')

    # Invocando o BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Puxando o a tabela que será utilizada

    social_blade_container = soup.find('div', {'id' : 'socialblade-user-content'})
    style1 = {'style' : 'width: 860px; height: 30px; line-height: 30px; background: #f8f8f8;; border-bottom: 1px solid #ddd; padding: 0px 20px; color:#444; font-size: 9pt;'}
    style2 = {'style' : 'width: 860px; height: 30px; line-height: 30px; background: #fafafa; border-bottom: 1px solid #ddd; padding: 0px 20px; color:#444; font-size: 9pt;'}
    data = social_blade_container.find('div', style = "width: 880px; background: #fff; padding: 0px; color:#444; font-size: 10pt;")
    rows1 = data.findAll('div', style1)
    rows2 = data.findAll('div', style2)
    rows = []
    for row in range(len(rows1)):
        rows.append(rows1[row])
        rows.append(rows2[row])

    n_rows = len(rows)

    # Declarando variáveis para alimentar o dataframe:

    dates = []
    days = []
    followers = []
    following = []
    posts = []


    # Puxando lista de datas
    for item in range(n_rows):
        date = rows[item].findAll('div')[1].get_text()
        dates.append(date)

    # Puxando lista de dias da semana
    for item in range(n_rows):
        day = rows[item].findAll('div')[2].get_text()
        days.append(day)

    # Puxando lista do numero de seguidores
    for item in range(n_rows):
        follower = rows[item].findAll('div')[5].get_text().split()[0]
        follower = follower.replace(',','')
        followers.append(follower)

    # Puxando lista do número de pessoas que está seguindo
    for item in range(n_rows):
        follow = rows[item].findAll('div')[8].get_text()
        follow = follow.replace(',','')
        following.append(follow)

    # Puxando lista do número de posts realizados
    for item in range(n_rows):
        post = rows[item].findAll('div')[11].get_text()
        post = post.replace(',','')
        posts.append(post)

    # Criando o dataframe:

    # Criando o dataframe de cada coluna
    df_date = pd.DataFrame(dates, columns = ['data'])
    df_days = pd.DataFrame(days, columns = ['days'])
    df_followers = pd.DataFrame(followers, columns = ['followers'])
    df_following = pd.DataFrame(following, columns = ['following'])
    df_posts = pd.DataFrame(posts, columns = ['posts'])

    # Concatenando tudo em um só dataframe
    insta_data = pd.concat([df_date, df_days, df_followers, df_following, df_posts], axis = 1)


    # Tratando os dados do dataframe:

    # Convertendo a coluna date para o tipo 'datetime'
    #insta_data['data'] = pd.to_datetime(insta_data['data'])

    # Traduzindo os dados da coluna 'days'
    weekdays = {'Thu' : 'Qui'
                , 'Fri' : 'Sex'
                , 'Sat' : 'Sab'
                , 'Sun' : 'Dom'
                , 'Mon' : 'Seg'
                , 'Wed' : 'Qua'
                , 'Tue' : 'Ter'}

    insta_data['days'] = insta_data.days.map(weekdays)

    # Traduzindo os nomes das colunas
    columns = {'data' : 'data'
               , 'days' : 'dia'
               , 'followers' :'seguidores'
               , 'following' :'seguindo'
               , 'posts' : 'posts'}

    insta_data = insta_data.rename(columns = columns)


    # Gerando arquivo .csv
    insta_data.to_csv('participantes/dados/' + today + '/' + user + '.csv', sep = ',', index = False)

# Função que abre o arquivo com nomes dos usuarios e gerando um csv para cada um dentro da pasta /participantes/dados
def geraPastaDados(nome_arquivo):
    file = open('participantes/usuarios/' + nome_arquivo + '.txt')
    lista_usuarios = file.read().split()
    today = date.today().strftime("%d-%m-%Y")
    path = 'participantes/dados/' + today
    try: 
        os.mkdir(path)
    except:
        print('Dados já coletados hoje!')
    for usuario in lista_usuarios:
        instaData(usuario, today)
    file.close()

        
# Chamando a função
geraPastaDados('nomes')