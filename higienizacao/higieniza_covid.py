import pandas as pd

def popula_data(row):  
    
    if(row['data_pri_sintomas_nova'] is pd.NaT):
        return row['data_solicitacao_exame']
    else:
        return row['data_pri_sintomas_nova']

municipios = ['FORTALEZA','FORTALEZA-CE','FORT, CE - BR','FPORTALEZA, CE - BR','EUSEBIO','EUZEBIO, CE - BR','EUZEBIO','CAUCAIA','MARACANAU','MARANGUAPE']    

covid = pd.read_csv('/home/carlos/Insync/carlos.o.c.neto@gmail.com/OneDrive/mobilidade_covid/covid/base-dados-integrasus-2020-07-23-09-05-50.csv',
                   delimiter=';',encoding='UTF-8',low_memory=False)

covid = covid[covid['resultado_final_exame']=='Positivo']

covid = covid.drop_duplicates()

covid = covid[covid['municipio_paciente'].isin(municipios)]

covid['id'] = covid.index+1

covid = covid.filter(['id','evolucao_caso_esus','nome_paciente',
              'data_nascimento','nome_mae','cpf','bairro_paciente','codigo_paciente',
              'data_inicio_sintomas','data_solicitacao_exame','data_coleta_exame','data_resultado_exame','resultado_final_exame']);

covid = covid.rename(columns={'id': 'ORDEM',
                              'nome_paciente':'NOME',
                              'data_nascimento':'DATA_NASCIMENTO',
                              'nome_mae':'NOME_MAE',
                              'data_inicio_sintomas':'data_pri_sintomas_nova'})

covid['data_pri_sintomas_nova'] = pd.to_datetime(covid['data_pri_sintomas_nova'],errors='coerce').dt.date

covid['DATA_NASCIMENTO'] = pd.to_datetime(covid['DATA_NASCIMENTO'],format='%Y/%m/%d',errors='coerce').dt.date

covid['data_solicitacao_exame'] = pd.to_datetime(covid['data_solicitacao_exame'],errors='coerce').dt.date

covid['data_coleta_exame'] = pd.to_datetime(covid['data_coleta_exame'],errors='coerce').dt.date

covid['data_resultado_exame'] = pd.to_datetime(covid['data_resultado_exame'],errors='coerce').dt.date

# covid['data_pri_sintomas_nova'] = covid.apply(popula_data, axis=1)

covid = covid[(~covid['data_pri_sintomas_nova'].isna())]

covid.to_csv('/home/carlos/Downloads/casos_covid.csv',encoding='UTF-8',index=False,sep=';')




