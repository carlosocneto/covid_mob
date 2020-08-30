import os
import numpy as np
import pandas as pd

from datetime import datetime
from shapely.geometry import Point
from shapely.geometry import Polygon
from math import sin, cos, sqrt, atan2, radians

pd.set_option('display.max_columns', None)


def load_gps(path_file, ajust_time=False):

    dict_rename = {0: 'azimute', 1: 'latitude', 2: 'longitude', 3: 'datahora', 4: 'odometro',
                   5: 'routeid', 6: 'velocidade', 7: 'deviceid', 8: 'veiculoid'}

    df_gps = pd.read_csv(path_file, delimiter=',', header=None)

    df_gps.rename(columns=dict_rename, inplace=True)

    df_gps['datahora_dt'] = pd.to_datetime(df_gps['datahora'], format='%Y%m%d%H%M%S', errors='coerce')

    if ajust_time:
        df_gps['datahora_dt'] = df_gps['datahora_dt'] - pd.Timedelta(hours=3)

    df_gps['data'] = df_gps['datahora_dt'].dt.date

    df_gps['datahora'] = df_gps['datahora_dt'].dt.strftime("%Y%m%d%H%M%S")

    return df_gps


def remove_out_fortal(df_gps):
    df_shape = pd.read_csv('../mapas/shapefile_fortaleza_osm.csv')
    df_shape = df_shape.sample(frac=0.2).sort_index()
    polygon = Polygon(df_shape.values)

    def check_inside_fortal(row):
        point = Point(row[1], row[0])
        if polygon.contains(point):
            return True
        return False

    infortal = []
    array_gps = df_gps.values
    for i, gps in enumerate(array_gps):
        if i % 500000 == 0:
            print('\t\t', i, 'de', len(array_gps), 'pontos gps -', datetime.now())
        row = [gps[1], gps[2]]
        infortal.append(check_inside_fortal(row))

    df_gps.insert(len(df_gps.columns), 'in_fortal', infortal)

    df_gps = df_gps[df_gps['in_fortal'] == True]

    return df_gps


def distance(lat1, lon1, lat2, lon2):

    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    dist = R * c

    return dist * 1000


def calc_delta_times(df_gps):
    df_gps.sort_values(by='datahora_dt', inplace=True)
    df_gps['delta_time'] = df_gps['datahora_dt'].diff()
    df_gps['delta_time'] = pd.to_timedelta(df_gps['delta_time'], unit='seconds')
    df_gps['delta_time'] = df_gps['delta_time'].dt.total_seconds()

    return df_gps


def calc_delta_spaces(df_gps):
    delta_s = [float('nan')]

    gps = df_gps.values
    for i in range(len(gps) - 1):
        gps1 = gps[i]
        gps2 = gps[i + 1]

        lat1 = gps1[1]
        lon1 = gps1[2]

        lat2 = gps2[1]
        lon2 = gps2[2]

        space = distance(lat1, lon1, lat2, lon2)
        delta_s.append(space)

    df_gps.insert(len(df_gps.columns), 'delta_space', delta_s)
    df_gps['delta_vel'] = (df_gps['delta_space'] / df_gps['delta_time']) * 3.6

    return df_gps


def remove_velocity_high(df_gps):

    gb_gps = df_gps.groupby('veiculoid')

    list_dataframes = []

    counter = 0
    for veiculoid, df_gps_by_veiculo in gb_gps:

        counter = counter + 1
        if counter % 400 == 0:
            print('\t\t', counter, 'de', len(gb_gps), 'veiculos - veiculoid:', veiculoid, '-', datetime.now())

        x = df_gps_by_veiculo.copy()
        x = calc_delta_times(x)
        x = calc_delta_spaces(x)

        x = x[x['delta_vel'] < 100]

        columns_delta = ['delta_time', 'delta_space', 'delta_vel']
        x = x.replace([np.inf], np.nan)
        x[columns_delta] = x[columns_delta].fillna(value=0.0)

        list_dataframes.append(x)

    df_gps_final = pd.concat(list_dataframes)

    return df_gps_final


if __name__ == '__main__':

    reports = []

    directory = '/home/carlos/Insync/carlos.o.c.neto@gmail.com/OneDrive/mobilidade_covid/agosto de 2020/'
    
    directory_raw = directory+'gps_raw/'
    save_in = directory+'gps_clean/gps_clean_%s.csv'

    report_name = 'relatorio_higienizacao.csv'

    files = os.listdir(directory_raw)
    for i, file in enumerate(files):
        print(i, 'load', file)

        path = os.path.join(directory_raw, file)
        df = load_gps(path, ajust_time=True)

        original_size = len(df)
        print('original', len(df))

        df.drop_duplicates(inplace=True)
        remove_duplicates1 = len(df)
        print('remove duplicates 1:', len(df))

        df.drop_duplicates(subset=['latitude', 'longitude', 'datahora', 'veiculoid'], inplace=True)
        remove_duplicates2 = len(df)
        print('remove duplicates 2:', len(df))

        df = remove_out_fortal(df)
        size_in_fortal = len(df)

        df = remove_velocity_high(df)
        size_vel = len(df)

        data = df['data'].unique()
        print('data', data)
        data = data[0]

        print('\t', size_in_fortal, size_vel)

        total_remove = original_size - size_vel
        report = [data, original_size, remove_duplicates1, remove_duplicates2, size_in_fortal, size_vel, total_remove]
        reports.append(report)

        columns_write = ['azimute', 'latitude', 'longitude', 'datahora', 'odometro',
                         'routeid', 'velocidade', 'deviceid', 'veiculoid']

        name_file = save_in % data

        df[columns_write].to_csv(name_file, index=False, sep=';')

    reports = pd.DataFrame(reports)
    reports.rename(columns={0: 'data', 1: 'original_size', 2: 'duplicates1',
                            3: 'duplicates2', 4: 'in_fortal', 5: 'high_vel',
                            6: 'total_removed'}, inplace=True)

    reports.to_csv(report_name, index=False)
