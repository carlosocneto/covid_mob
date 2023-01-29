import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

from shapely import wkt
from shapely.geometry import Polygon
from _codecs import encode

plt.rc('patch',linewidth=2)
plt.rc('axes', linewidth=2, labelpad=5)
plt.rc('xtick.minor', size=2, width=2)
plt.rc('xtick.major', size=4, width=2, pad=4)
plt.rc('ytick.minor', size=2, width=2)
plt.rc('ytick.major', size=4, width=2, pad=4)
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Computer Modern', size=16)

arquivo_quantidades = '/home/carlos/Downloads/DESP_REC.csv'

#CARREGA SETORES

arquivoMapa = '../mapas/ceara.csv'

df_mapa = pd.read_csv(arquivoMapa, delimiter = ';')

gdf_setores = gpd.GeoDataFrame(df_mapa)

gdf_setores['geometry'] = gdf_setores['geometry'].apply(wkt.loads)

gdf_setores['centroid'] = gdf_setores['geometry'].centroid

gdf_setores['area'] = gdf_setores['geometry'].area


#CARREGA SETORES

#CARREGA PONTOS

dados_quantidades = pd.read_csv(arquivo_quantidades,
                      delimiter=';',encoding='ISO-8859-1' ,low_memory=False)

print(dados_quantidades)
 

gdf_setores_processado = gdf_setores.merge(dados_quantidades, on='id', how='inner')

coluna = 'DESPESA_RECEITA'

gdf_setores_processado[coluna] = gdf_setores_processado[coluna].fillna(1)

gdf_setores_processado[coluna+'_log'] = gdf_setores_processado[coluna]#np.log10(gdf_setores_processado[coluna])

fig, ax = plt.subplots(1, 1)

gdf_setores_processado.plot(column=coluna+'_log', ax=ax, cmap='YlOrRd', legend=True)

arquivo_de_saida = '/home/carlos/Downloads/'+coluna+'.pdf'

plt.savefig(arquivo_de_saida, format="PDF")
