import pandas as pd
import glob

#PARAMETROS

path_geral = '/home/carlos/Insync/carlos.o.c.neto@gmail.com/OneDrive/mobilidade_covid/'

arquivo_bu = path_geral+'DADOS RELATORIO/bu_higienizado.csv'

arquivo_estudantes = path_geral+'DADOS RELATORIO/estudantes.csv'

arquivo_idosos = path_geral+'Idosos.csv'

pasta_validations = path_geral+'/DADOS RELATORIO/validations' # diretorio validation

all_files = glob.glob(pasta_validations + "/*.txt")

li = []

for filename in all_files:
    df = pd.read_csv(filename, delimiter=';',  index_col=None, header=0)
    li.append(df)

validation = pd.concat(li, axis=0, ignore_index=True)

validation['data_hora'] = pd.to_datetime(validation['data_hora'])

data_sem_hora = validation['data_hora'].dt.date

#PRECISAREI DA DATA LÁ NA FRENTE
validation['data'] = data_sem_hora

validation = validation[validation['sigon']!=0]

bu = pd.read_csv(arquivo_bu,
                   delimiter=';',encoding='UTF-8',low_memory=False)

bu = bu[bu['sigon'].isin(validation['sigon'].unique())]

bu = bu.filter(['sigon','nome','dt_nasc','mae','endereco','bairro'])

bu['tipo'] = 'bu'

idosos = pd.read_csv(arquivo_idosos,delimiter=','
                 ,encoding='ISO-8859-1',low_memory=False)

idosos['DATA_NASCIMENTO'] = pd.to_datetime(idosos['DATA_NASCIMENTO'],format='%d/%m/%Y',errors='coerce').dt.date

idosos = idosos.filter(
     ['CODIGO_USUARIO','NOME','DATA_NASCIMENTO','USU_NOME_MAE'])

idosos = idosos[idosos['CODIGO_USUARIO'].isin(validation['sigon'].unique())]

idosos = idosos.rename(
    columns={'CODIGO_USUARIO': 'sigon','NOME':'nome','DATA_NASCIMENTO':'dt_nasc','USU_NOME_MAE':'mae','ENDERECO':'endereco','BAIRRO':'bairro'})

idosos['tipo'] = 'idoso'

estudantes = pd.read_csv(arquivo_estudantes,
                   delimiter=';',encoding='ISO-8859-1',low_memory=False)

estudantes['endereco'] = estudantes['rua']+','+estudantes['numero']

estudantes = estudantes.filter(['matricula','nome','dt_nasc','mae','endereco','bairro'])

estudantes = estudantes[estudantes['matricula'].isin(validation['sigon'].unique())]

estudantes = estudantes.rename(
    columns={'matricula': 'sigon'})

estudantes['tipo'] = 'estudante'

frames = [estudantes, idosos, bu]

dados_integrados_sigon = pd.concat(frames)

dados_integrados_sigon.to_csv('/home/carlos/Downloads/bu-integrado-pandemia.csv',encoding='UTF-8',index=False,sep=';')





