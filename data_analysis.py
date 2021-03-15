# importando bibliotecas
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
%matplotlib inline

# Puxa o csv do usuario e trata as colunas
def pushUserData(user_name):
    df = pd.read_csv(f'participantes/dados/total/{user_name}.csv')
    df['data'] = pd.to_datetime(df['data'])
    df['dia'] = df['dia'].astype(str)
    df['seguidores'] = pd.to_numeric(df['seguidores'])
    df['seguindo'] = pd.to_numeric(df['seguindo'])
    df['posts'] = pd.to_numeric(df['posts'])
    return df

# Cria as colunas com as diferenças e a aceleração de seguidores, seguindo e posts
def createAuxCols(data):
    data['dif_seguidores'] = data['seguidores'].diff()
    data['acl_seguidores'] = data['dif_seguidores'].diff()
    data['dif_seguindo'] = data['seguindo'].diff()
    data['acl_seguindo'] = data['dif_seguindo'].diff()
    data['dif_posts'] = data['posts'].diff()
    data['dif_seguidores'] = pd.to_numeric(data['dif_seguidores'])
    data['acl_seguidores'] = pd.to_numeric(data['acl_seguidores'])
    data['dif_seguindo'] = pd.to_numeric(data['dif_seguindo'])
    data['acl_seguindo'] = pd.to_numeric(data['acl_seguindo'])
    data['dif_posts'] = pd.to_numeric(data['dif_posts'])
    n_dia = np.arange(0, data['dia'].shape[0]) + 1
    data['n_dia'] = n_dia
    data = data.fillna(0)
    return data


# Plota um lineplot único
def plot_line(title, data, x, y, xlabel, ylabel):
    sns.set_style('whitegrid')
    ax = sns.lineplot(x = x , y = y, data = data, linewidth = 5 )
    ax.figure.set_size_inches(15,7)
    ax.set_title(title, loc= 'center', fontsize = 18)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax = ax

def compare_plot(data, user):

    plt.figure(figsize = (17, 12))
    ax = plt.subplot(3, 1, 1)
    ax.set_title(f'Análise dos seguidores de @{user}', fontsize = 18, loc = 'center')
    
    sns.set_style('whitegrid')
    g1 = sns.lineplot(x = 'data' , y = 'seguidores', data = data, linewidth = 5)
    g1.figure.set_size_inches(15,17)
    g1.set_xlabel('Tempo', fontsize=14)
    g1.set_ylabel('Seguidores (Milhões)', fontsize=14)

    ax2 = plt.subplot(3, 1, 2)
    
    g2 = sns.lineplot(x = 'data' , y = 'dif_seguidores', data = data, linewidth = 5)
    g2.figure.set_size_inches(15,17)
    g2.set_xlabel('Tempo', fontsize=14)
    g2.set_ylabel('Ganho/Perda Diário', fontsize=14)

    ax3 = plt.subplot(3, 1, 3)
    
    g3 = sns.lineplot(x = 'data' , y = 'acl_seguidores', data = data, linewidth = 5)
    g3.figure.set_size_inches(15,17)
    g3.set_xlabel('Tempo', fontsize=14)
    g3.set_ylabel('Aceleração', fontsize=14)
    
    plt.savefig(f'participantes/graficos/comparacao/comparacao_{user}.png')
    plt.close()


# Gera gráfico da média de perda por dia da semana  
def plot_mean_loss_by_day(data, user):
    aux_col = []
    for item in data['dif_seguidores']:
        if item != 0:
            aux_col.append(item * (-1))
        else:
            aux_col.append(item)
    data['dif_seguidores_aux'] = aux_col
    mean_lost_per_day = data.groupby(['dia']).mean()['dif_seguidores_aux'].astype(int).to_frame()
    mean_lost_per_day['dia'] = mean_lost_per_day.index
    mean_lost_per_day[''] = list(range(mean_lost_per_day.shape[0]))
    mean_lost_per_day = mean_lost_per_day.set_index('')
    re_arange = [mean_lost_per_day.iloc[0],
                 mean_lost_per_day.iloc[4],
                 mean_lost_per_day.iloc[6],
                 mean_lost_per_day.iloc[1],
                 mean_lost_per_day.iloc[2],
                 mean_lost_per_day.iloc[5],
                 mean_lost_per_day.iloc[3]]

    mean_lost_per_day = pd.concat(re_arange, axis = 1).T
    mean_lost_per_day[''] = list(range(mean_lost_per_day.shape[0]))
    mean_lost_per_day = mean_lost_per_day.set_index('')
    
    plt.figure(figsize = (17, 12))
    g1 = sns.barplot(x = 'dia', y = 'dif_seguidores_aux', data = mean_lost_per_day)
    g1.set_title(f'Média de Seguidores Ganhos/Perdidos de @{user} p/ Dia da Semana', fontsize = 18, loc = 'center')
    g1.figure.set_size_inches(15,7)
    g1.set_xlabel('Dia da Semana', fontsize=14)
    g1.set_ylabel('Média de Ganho/Perda', fontsize=14)
    del data['dif_seguidores_aux']
    plt.savefig(f'participantes/graficos/perda_dia_da_semana/dia_da_semana_{user}.png')
    plt.close()
    
    

# Gera um gráfico para cara um nas suas respectivas pastas

def generate_all_compare(file_name):
    file = open('participantes/usuarios/' + file_name + '.txt')
    user_list = file.read().split()
    for user in user_list:
        data = pushUserData(user)
        data = createAuxCols(data)
        compare_plot(data, user)
    file.close()
    
def generate_all_weekday(file_name):
    file = open('participantes/usuarios/' + file_name + '.txt')
    user_list = file.read().split()
    for user in user_list:
        data = pushUserData(user)
        data = createAuxCols(data)
        plot_mean_loss_by_day(data, user)
    file.close()


generate_all_compare('nomes')
generate_all_weekday('nomes')