import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

from shapely import wkt
from shapely.geometry import Polygon

plt.rc('patch', linewidth=2)
plt.rc('axes', linewidth=2, labelpad=5)
plt.rc('xtick.minor', size=2, width=2)
plt.rc('xtick.major', size=4, width=2, pad=4)
plt.rc('ytick.minor', size=2, width=2)
plt.rc('ytick.major', size=4, width=2, pad=4)
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Computer Modern', size=16)

arquivo_de_saida = '/home/carlos/Downloads/mapa.pdf'

arquivo_coordenadas = '/mnt/68E2710EE270E22C/Insync/mobilidade_covid/DADOS RELATORIO/RESULTADOS/viagens_contato_direto_indireto.csv'

# CARREGA SETORES
arquivoMapa = '../mapas/fortaleza/setores.csv'

df_mapa = pd.read_csv(arquivoMapa, delimiter=';')
gdf_setores = gpd.GeoDataFrame(df_mapa)

gdf_setores['geometry'] = gdf_setores['geometry'].apply(wkt.loads)
gdf_setores = gdf_setores.set_geometry('geometry')  # Definir a coluna de geometria

gdf_setores['centroid'] = gdf_setores['geometry'].centroid
gdf_setores['area'] = gdf_setores['geometry'].area
# CARREGA SETORES

# CARREGA PONTOS
coordenandas = pd.read_csv(arquivo_coordenadas, delimiter=';', encoding='ISO-8859-1', low_memory=False)
coordenandas = coordenandas.filter(['lat', 'lng'])
gdf_viagens = gpd.GeoDataFrame(coordenandas, geometry=gpd.points_from_xy(coordenandas.lng, coordenandas.lat))
# CARREGA PONTOS

gdf_pontos_com_setores = gpd.sjoin(gdf_viagens, gdf_setores, predicate='within')

grouped = gdf_pontos_com_setores.groupby('id').size()
df_setores_count_pontos = grouped.to_frame().reset_index()
df_setores_count_pontos.columns = ['id', 'total_coordenandas']

gdf_setores_processado = gdf_setores.merge(df_setores_count_pontos, on='id', how='outer')
gdf_setores_processado['total_coordenandas'] = gdf_setores_processado['total_coordenandas'].fillna(1)
gdf_setores_processado['total_coordenandas_log'] = np.log10(
gdf_setores_processado['total_coordenandas'] / gdf_setores_processado['area'])

fig, ax = plt.subplots(1, 1)
gdf_setores_processado.plot(column='total_coordenandas_log', ax=ax, legend=True)

plt.savefig(arquivo_de_saida, format="PDF")
