import pandas as pd

bu = pd.read_csv('/home/carlos/Insync/carlos.o.c.neto@gmail.com/OneDrive/mobilidade_covid/BU.csv',delimiter=';'
                ,encoding='UTF-8',low_memory=False,header=None,
                 names=["0", "nome", "documento","orgao_expedidor",
                        "dt_nasc","endereco","bairro","cidade","estado","cep",
                        "telefone","mae","12","tipo","pis","sigon"])

bu['dt_nasc'] = bu['dt_nasc'].str.replace('00:00:00.000', '', regex=False)

bu['nome'] = bu['nome'].str.replace('^ +| +$', '')

bu['mae'] = bu['mae'].str.replace('^ +| +$', '')

bu['dt_nasc'] = bu['dt_nasc'].str.replace('^ +| +$', '')

bu['bairro'] = bu['bairro'].str.replace('^ +| +$', '')

bu = bu.filter(['sigon','nome','dt_nasc','bairro','cidade','cep','mae','tipo','endereco']);

bu.to_csv('/home/carlos/Downloads/bu_higienizado.csv',index=False,sep=';')
