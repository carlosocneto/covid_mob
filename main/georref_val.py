import os
from os import path
import pandas as pd
from datetime import datetime
from multiprocessing import Pool

#PARÂMETROS

num_process = 6

caminho_padrao = '/home/carlos/Insync/carlos.o.c.neto@gmail.com/OneDrive/mobilidade_covid/junho de 2020/'

caminho_hash = caminho_padrao+'veiculos_sindionibus.csv'
caminho_val = caminho_padrao+'validation_to_process/'
caminho_gps = caminho_padrao+'gps_clean/'

caminho_saida = caminho_padrao+'validation_proc/'

tolerancia = 3*60 #3 minutos

#PARÂMETROS

#FUNÇÃO GEORREF

def georreferencia_um_dia(filename):    
    
    strDataValidation = filename.replace('Viagenssigom','')
    strDataValidation = strDataValidation.replace('.csv','')

    diaValidation = datetime.strptime(strDataValidation, '%Y%m%d')

    strDiaGps = diaValidation.strftime("%Y-%m-%d") 
    
    caminho_arquivo_gps_do_dia = caminho_gps+'gps_clean_'+strDiaGps+'.csv'
    
    if(not path.exists(caminho_arquivo_gps_do_dia)):
        print('Arquivo não encontrado:',caminho_arquivo_gps_do_dia)
        return
    
    dfs_gps_veiculos = {}
    
    #HASH TERMINAIS

    terminais = {}
    
    terminais[7] = [-3.772920, -38.607601]
    terminais[10] = [-3.789877, -38.586774]
    terminais[5] = [-3.771688, -38.570013]
    terminais[1] = [-3.737488, -38.584713]
    terminais[3] = [-3.776106, -38.563565]
    terminais[6] = [-3.831225, -38.501589]
    terminais[8] = [-3.738198, -38.485087]
    
    #HASH TERMINAIS
    
    #CARREGA ARQUIVO DE HASH
    df_arquivo_hash = pd.read_csv(caminho_hash, 
                     delimiter=';')
    #CARREGA ARQUIVO DE HASH
    
    print('Inicio:',filename,'-',datetime.now().strftime("%H:%M:%S") )
    
    #CARREGA ARQUIVO DE VALIDATION DO DIA
    df_val = pd.read_csv(caminho_val+filename, 
                         delimiter=';',low_memory=False,header=None,
                     names=["sigon", "linha", "nome_linha","num_veiculo",
                            "data_hora","tipo_validacao","tipo_desc","sentido","integracao","nao_sei"])
    
    df_val['data_hora'] = pd.to_datetime(df_val['data_hora'],format='%d/%m/%Y %H:%M:%S',errors='coerce') 
    df_val['lat'] = 0.0
    df_val['lng'] = 0.0
    df_val['sentido'] = df_val['sentido'].replace('Ida','I')
    df_val['sentido'] = df_val['sentido'].replace('Volta','V')
    #CARREGA ARQUIVO DE VALIDATION DO DIA
    
    #CARREGA ARQUIVO DE GPS DO DIA
           
    df_gps = pd.read_csv(caminho_arquivo_gps_do_dia,delimiter=';')
    
    df_gps['datahora'] = pd.to_datetime(df_gps['datahora'],format='%Y%m%d%H%M%S',errors='coerce')
    df_gps = df_gps.sort_values(by=['datahora'])
    #CARREGA ARQUIVO DE GPS DO DIA
    
    #AGREGA NUM_VEICULO DO GPS na coluna v_gps
    df_val_join = pd.merge(df_val, df_arquivo_hash, left_on='num_veiculo', 
                                  right_on='cod_veiculo',how='left')
    df_val_join = df_val_join.filter(['sigon','linha','num_veiculo',
                                      'data_hora','tipo_validacao','sentido','lat','lng','integracao','id_veiculo'])
    df_val_join = df_val_join.rename(columns={'id_veiculo': 'v_gps'})
    
    df_val_join['v_gps'] = df_val_join['v_gps'].astype('Int64')
    
    df_val_join['v_gps'] = df_val_join['v_gps'].fillna(-1)
    
    #AGREGA NUM_VEICULO DO GPS na coluna v_gps
    
    del df_val
    
    cont = 0
    cont_sucess = 0
    for index, row in df_val_join.iterrows():
        cont = cont + 1
        
        #GEORREF TERMINAIS
        if row['linha'] in terminais:
            df_val_join.at[index,'lat']=terminais[row['linha']][0]
            df_val_join.at[index,'lng']=terminais[row['linha']][1]
            cont_sucess = cont_sucess + 1
        else:
        #GEORREF PELO GPS
            
            veiculoid_str = str(row['num_veiculo'])
            
            #TOPIC NÃO TEM GPS
            if(veiculoid_str[0:2] == '67'):
                continue
            
            if(row['v_gps']==-1):
                continue
            
            if row['v_gps'] in dfs_gps_veiculos:
                df_gps_veiculo = dfs_gps_veiculos[row['v_gps']]   
                df_gps_veiculo_horario = df_gps_veiculo[(df_gps_veiculo['datahora'] >= row['data_hora']) & 
                            (df_gps_veiculo['datahora'] <= row['data_hora']+ pd.to_timedelta(tolerancia, unit='s'))]
                
                if(df_gps_veiculo_horario.size>0):
                    for index_gps,row_gps in df_gps_veiculo_horario.iterrows():
                        df_val_join.at[index,'lat']=row_gps['latitude']
                        df_val_join.at[index,'lng']=row_gps['longitude']
                        break
                    
                    cont_sucess = cont_sucess + 1
                
                del df_gps_veiculo_horario
            else:
                dfs_gps_veiculos[row['v_gps']] = df_gps[df_gps['veiculoid'] == row['v_gps']]
            
        if(cont % 2000 == 0):
            print(filename,'=', cont, 'de', df_val_join['sigon'].size, '-', datetime.now().strftime("%H:%M:%S"), '(',cont_sucess/cont,')')
        
    
    df_val_join = df_val_join.drop(['v_gps'], axis=1)
    
    df_val_join.to_csv(caminho_saida+'validation-'+strDiaGps+'.txt',encoding='UTF-8',index=False,sep=';')
    
    print('Fim:',filename,'-',datetime.now().strftime("%H:%M:%S"))
    
    del df_val_join
    del df_gps
    
    return

#FUNÇÃO GEORREF

if __name__ == '__main__':    
    
    all_files = os.listdir(caminho_val)
    
    filenames = []
    
    for filename in all_files:       
        filenames.append(filename)
#         georreferencia_um_dia(filename)

    with Pool(processes=num_process) as pool:        
        pool.map(georreferencia_um_dia, filenames)
    


    
    
    
    
    
    
    
    
