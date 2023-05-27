import warnings as warn
from requests import get 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from random import randint
from time import sleep

paginas = np.arange(1, 5, 50)
headers = {'Accept-Language': 'pt-BR,q=0.8'}
titulo = []
years = []
genero = []
runtimes = []
imdb_ratings = []
imb_ratings_standardized = []
votes = []
ratings = []


for pagina in paginas:

    response = get("https://www.imdb.com/search/title?genres=sci-fi&"
                   + "start=" + str(pagina) + "&explore=title_type,generes&ref_=adv_prv", headers=headers)
    
    sleep(randint(8,15))
    if response.status_code != 200:
        warn(f'O pedido: {requests}; Retornou código {response.status_code}')
    #Pegando cada arquivo HTML da aplicação
    page_html = BeautifulSoup(response.text, 'html.parser')

    movie_containers = page_html.find_all('div',class_ = 'lister-item mode-advanced')
    # Separando as informações em container individuais
    for container in movie_containers:
        #Capturar os títulos
        if container.find('div', class_ = 'ratings-metascore') is not None:
            title = container.h3.a.text
            titulo.append(title)
            #capturar anos
            if container.h3.find('span', class_ =  'lister-item-year text-muted unbold') is not None:
                year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
                years.append(year)
            else:
                year.append(None)

            #capturar avaliações
            if container.p.find('span', class_ = 'certificate') is not None:
                rating = container.p.find('span', class_ = 'certificate').text
                ratings.append(rating)
            else:
                ratings.append(None)

            #Capturar gênero genre
            if container.p.find('span', class_ = 'genre') is not None:
                genre = container.p.find('span', class_  = 'genre').text.replace('\n', '').strip().split()
                genero.append(genre)
            else:
                genero.append(None) 

            #captura duração do filme
            if container.p.find('span', class_ = 'runtime') is not None:
                time = int(container.p.find('span', class_ = 'runtime').text.replace('min', ''))
                runtimes.append(time)
            else:
                runtimes.append(None)
            #Capturar a avaliação IMD8 e converter em decimal (strong)
            if container.strong.text is not None:
                imdb = float(container.strong.text.replace(',', '.'))
                imdb_ratings.append(imdb)
            else:
                imdb_ratings.append(None)
            #Capturar os votos dos usuários (span attrs: name 'nav')
            if container.find('span', attrs={'name': 'nv'})['data-value'] is not None:
                voto = int(container.find('span', attrs={'name': 'nv'})['data-value'])
                votes.append(voto)
            else:
                votes.append(None)
df_inicial = pd.DataFrame({
    'ano': years,
    'genero': genero,
    'tempo': runtimes,
    'imdb': imdb_ratings,
    'votos': votes
})

#Separar colunas e corrigir tipagem de dados
df_inicial.loc[:, 'ano'] = df_inicial['ano'].str[-5:-1]
df_inicial['n_imdb'] = df_inicial['imdb']*10
df_final = df_inicial.loc[df_inicial['ano'] != 'Movie']

#Relação da quantidade de filmes por voto
# print(df_final.head())
# sns.heatmap(df_final.corr(), annot=False)
# ax = df_final['imdb'].value_counts().plot(kind='bar', figsize=(14, 8), title='Número de filmes por voto')
# ax.set_xlabel("Votos")
# ax.set_ylabel('Quantidade de Filmes')
# ax.plot()

#Relação entre duração de filme / voto

# plt.scatter(df_final['tempo'], df_final['imdb'])
# plt.xlabel('Duração dos filmes')
# plt.ylabel('Nota IMDM')


sep_genero = df_inicial.explode('genero')

genero_counts = sep_genero['genero'].value_counts()

genero_counts.plot(kind='barh')

plt.show()





# print(response)
    
# https://www.imdb.com/search/title?genres=sci-fi&
# &explore=title_type,genres&ref_=adv_prv