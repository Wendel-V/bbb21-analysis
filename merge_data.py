# Importando bibliotecas
import pandas as pd
from datetime import datetime
from datetime import timedelta

# Adiciona nova linha no DataFrame principal
def addRow(base_df, df):
    new_row = {'data' : str(df.iloc[-1][0]),
       'dia' : str(df.iloc[-1][1]),
       'seguidores' : str(df.iloc[-1][2]), 
       'seguindo' : str(df.iloc[-1][3]) , 
       'posts' : str(df.iloc[-1][4]) }
    return base_df.append(new_row, ignore_index = True)  

# Junta as linhas de todos os DataFrames das pastas presentes de um usuario
def joinAllDays(user):
    initial_day = '19-02-2021'
    day = (datetime.strptime(initial_day, "%d-%m-%Y") + timedelta(days = 0)).strftime("%d-%m-%Y")
    df_base = pd.read_csv(f'participantes/dados/{day}/{user}.csv')
    i = 1
    exists = True
    while exists:
        try:
            day = (datetime.strptime(initial_day, "%d-%m-%Y") + timedelta(days = i)).strftime("%d-%m-%Y")
            new_df = pd.read_csv(f'participantes/dados/{day}/{user}.csv')
            df_base = addRow(df_base, new_df)
            i += 1
        except:
            exists = False
            print(f'Tabela de {user} completamente atualizada!')
    return df_base

# Unifica os dados de todos os usuarios e cria um .csv para cada um na pasta 'total'
def updateAll(file_name):
    file = open('participantes/usuarios/' + file_name + '.txt')
    user_list = file.read().split()
    for user in user_list:
        df = joinAllDays(user)
        df.to_csv(f'participantes/dados/total/{user}.csv', index = False)
    file.close()
    
# Executa a função
updateAll('nomes')