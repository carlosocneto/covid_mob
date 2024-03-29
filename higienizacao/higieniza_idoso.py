import pandas as pd

idosos = pd.read_csv('/home/carlos/Insync/carlos.o.c.neto@gmail.com/OneDrive/mobilidade_covid/Idosos.csv',delimiter=','
                ,encoding='ISO-8859-1',low_memory=False)

idosos['DATA_NASCIMENTO'] = pd.to_datetime(idosos['DATA_NASCIMENTO'],format='%d/%m/%Y',errors='coerce')

idosos = idosos.filter(
    ['CODIGO_USUARIO','NOME','DATA_NASCIMENTO','USU_NOME_MAE','RG','ORGAO_EMISSOR','CPF','ENDERECO','BAIRRO'])

idosos.to_csv('/home/carlos/Downloads/idoso_higienizado.csv',index=False,sep=';')