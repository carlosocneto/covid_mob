import pandas as pd

path_contaminados = '/home/carlos/Insync/carlos.o.c.neto@gmail.com/OneDrive/mobilidade_covid/covid/tanta/'
path_contaminados += 'base_dados_integrasus_fortaleza_final(recebi dia 15 de setembro).csv'
df_contaminados = pd.read_csv(path_contaminados)

df_contaminados = df_contaminados.drop_duplicates()

df_contaminados['data_inicio_sintomas_nova'] =  pd.to_datetime(df_contaminados['data_inicio_sintomas_nova'],
                                                       format='%d/%m/%Y',errors='coerce')

df_contaminados['data_coleta_exame'] =  pd.to_datetime(df_contaminados['data_coleta_exame'],
                                                       format='%d/%m/%Y',errors='coerce')

df_contaminados['data_nascimento'] =  pd.to_datetime(df_contaminados['data_nascimento'],
                                                       format='%d/%m/%Y',errors='coerce')

df_contaminados['latitude_endereco_paciente'] = df_contaminados['latitude_endereco_paciente'].str.replace(',','.').astype(float)

df_contaminados['longitude_endereco_paciente'] = df_contaminados['longitude_endereco_paciente'].str.replace(',','.').astype(float)

df_contaminados.drop_duplicates({'codigo_paciente'},inplace=True)

df_contaminados = df_contaminados.filter(['id','obito_confirmado','nome_paciente',
              'data_nascimento','nome_mae','bairro_ajustado','codigo_paciente','sexo_paciente',
              'data_inicio_sintomas_nova','data_coleta_exame','tipo_teste_exame',
              'latitude_endereco_paciente','longitude_endereco_paciente']);

df_contaminados = df_contaminados.rename(columns={'id': 'ORDEM',
                              'nome_paciente':'NOME',
                              'data_nascimento':'DATA_NASCIMENTO',
                              'nome_mae':'NOME_MAE',
                              'data_inicio_sintomas_nova':'data_pri_sintomas_nova'})


df_contaminados = df_contaminados[(~df_contaminados['data_pri_sintomas_nova'].isna())]

df_contaminados.to_csv('/home/carlos/Downloads/casos_covid_tanta.csv',encoding='UTF-8',index=False,sep=';')




