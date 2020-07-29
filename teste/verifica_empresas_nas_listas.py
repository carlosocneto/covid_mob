import pandas as pd

df_2011 = pd.read_csv('/home/carlos/Downloads/sarah/2011_clean.csv')

df_2012_2014 = pd.read_csv('/home/carlos/Downloads/sarah/2012-2014_clean.csv')

pd.merge(df_2011, df_2012_2014, how='inner', on=['cnpj','regiao']).to_csv('/home/carlos/Downloads/2011_2014.csv',encoding='ISO-8859-1',index=False,sep=',')