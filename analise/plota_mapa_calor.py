import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

from shapely.geometry import Polygon  
from xml.etree import ElementTree as ET


plt.rc('patch',linewidth=2)
plt.rc('axes', linewidth=2, labelpad=5)
plt.rc('xtick.minor', size=2, width=2)
plt.rc('xtick.major', size=4, width=2, pad=4)
plt.rc('ytick.minor', size=2, width=2)
plt.rc('ytick.major', size=4, width=2, pad=4)
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Computer Modern', size=16)

arquivo_de_saida = '/home/carlos/Downloads/mapa.pdf'

arquivo_coordenadas = '/home/carlos/Insync/carlos.o.c.neto@gmail.com/OneDrive/mobilidade_covid/DADOS RELATORIO/RESULTADOS/viagens_contato_direto_indireto.csv'

#CARREGA SETORES

arquivokml = '../mapas/fortaleza/setores.kml'

tree = ET.parse(arquivokml)
root = tree.getroot()

document = root[0]

folder = document[1][1:]

df_cols = ["id", "geometry"]
linhas_setores = []

for child in folder:
    extendeddata = child[1]
    schemaData = extendeddata[0]
    s_id = schemaData[4].text
    polygon = child[2]
    coordinates = polygon[1][0][1]
    s_geometry = coordinates.text
    pontos_str = s_geometry.split(' ')
    pontos = []
    for ponto_str in pontos_str:
        pontos.append(ponto_str.split(','))
    
    pontos = list(np.float_(pontos))  
    polygon = Polygon(pontos)
    
    linhas_setores.append({"id": s_id, "geometry": polygon})
    
gdf_setores = gpd.GeoDataFrame(linhas_setores, columns = df_cols)

gdf_setores['centroid'] = gdf_setores['geometry'].centroid

gdf_setores['area'] = gdf_setores['geometry'].area

print(gdf_setores)

#CARREGA SETORES

#CARREGA PONTOS

coordenandas = pd.read_csv(arquivo_coordenadas,
                      delimiter=';',encoding='ISO-8859-1',low_memory=False)
 
coordenandas=coordenandas.filter(['lat','lng'])
 
gdf_viagens=gpd.GeoDataFrame(coordenandas,geometry=gpd.points_from_xy(coordenandas.lng, coordenandas.lat))
 
#CARREGA PONTOS
 
gdf_pontos_com_setores = gpd.sjoin(gdf_viagens, gdf_setores, op='within')

#  
grouped = gdf_pontos_com_setores.groupby('id').size()
df_setores_count_pontos = grouped.to_frame().reset_index()
df_setores_count_pontos.columns = ['id', 'total_coordenandas']
 
gdf_setores_processado = gdf_setores.merge(df_setores_count_pontos, on='id', how='outer')

gdf_setores_processado['total_coordenandas'] = gdf_setores_processado['total_coordenandas'].fillna(1)

gdf_setores_processado['total_coordenandas_log'] = np.log10(gdf_setores_processado['total_coordenandas']/gdf_setores_processado['area'])

fig, ax = plt.subplots(1, 1)

gdf_setores_processado.plot(column='total_coordenandas_log', ax=ax, legend=True)

plt.savefig(arquivo_de_saida, format="PDF")
