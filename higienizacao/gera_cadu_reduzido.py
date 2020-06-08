'''
Created on 20 de jun de 2019

@author: carlos
'''
import pandas as pd

cadu = pd.read_csv('/home/carlos/Downloads/mobilidade/gerado/cadu-unif-higienizado.csv',
                   delimiter=';',encoding='ISO-8859-1',low_memory=False) #usecols=[0,1,2,9,10,14,17]

cadu_reduzido = cadu.filter(['CHV-NATURAL-PREFEITURA-FAM','COD-FAMILIAR-FAM','NUM-MEMBRO-FMLA',
             'NOM-PESSOA','COD-SEXO-PESSOA','DTA-NASC-PESSOA',
             'COD-PARENTESCO-RF-PESSOA','COD-RACA-COR-PESSOA','NOM-COMPLETO-MAE-PESSOA',
             'NOM-COMPLETO-PAI-PESSOA'])

cadu_reduzido['DTA-NASC-PESSOA'] = pd.to_datetime(cadu_reduzido['DTA-NASC-PESSOA'],format='%d%m%Y',errors='coerce').dt.date

cadu_reduzido.to_csv('/home/carlos/Downloads/mobilidade/gerado/cadu-reduzido.csv',encoding='ISO-8859-1',index=False,sep=';')