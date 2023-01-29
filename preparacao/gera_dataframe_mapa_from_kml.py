import pandas as pd
import geopandas as gpd
import numpy as np

from shapely.geometry import Polygon  
from xml.etree import ElementTree as ET

arquivokml = '../mapas/ceara.kml'

tree = ET.parse(arquivokml)
root = tree.getroot()

document = root[0]

folder = document[1][1:]

df_cols = ["id", "geometry"]
linhas_setores = []

for child in folder:
    extendeddata = child[1]
    schemaData = extendeddata[0]
    s_id = schemaData[0].text
    multiGeometry = child[2]
    coordinates = multiGeometry[0][0][0][0]
    s_geometry = coordinates.text
    pontos_str = s_geometry.split(' ')
    pontos = []
    for ponto_str in pontos_str:
        pontos.append(ponto_str.split(','))
    
    pontos = list(np.float_(pontos))  
    polygon = Polygon(pontos)
    
    linhas_setores.append({"id": s_id, "geometry": polygon})
    
gdf_setores = gpd.GeoDataFrame(linhas_setores, columns = df_cols)

gdf_setores.to_csv('../saida/mapa.csv',encoding='UTF-8',index=False,sep=';')



    #FORMATO PARA PEGAR OS DADOS DOS OUTROS ARQUIVOS
    # extendeddata = child[1]
    # schemaData = extendeddata[0]
    # s_id = schemaData[4].text
    # polygon = child[2]
    # coordinates = polygon[1][0][1]
    # s_geometry = coordinates.text
