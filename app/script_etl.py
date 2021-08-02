#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import datetime
import os
from sqlalchemy import create_engine

def mes_numero(x):
    if(x.MES == 'Jan'):
        return 1
    elif(x.MES == 'Fev'):
        return 2
    elif(x.MES == 'Mar'):
        return 3
    elif(x.MES == 'Abr'):
        return 4
    elif(x.MES == 'Mai'):
        return 5
    elif(x.MES == 'Jun'):
        return 6
    elif(x.MES == 'Jul'):
        return 7
    elif(x.MES == 'Ago'):
        return 8
    elif(x.MES == 'Set'):
        return 9
    elif(x.MES == 'Out'):
        return 10
    elif(x.MES == 'Nov'):
        return 11
    elif(x.MES == 'Dez'):
        return 12


excel = pd.ExcelFile(os.getcwd() + '/app/sales_years.xls')
timestamp_exec = datetime.datetime.now()

df_table_full = pd.DataFrame()
for i in excel.sheet_names:
    if(i != 'Plan1'):
        df_aux = pd.read_excel(excel, i)
        df_aux = df_aux.drop(['TOTAL'], axis=1)
        df_aux = df_aux.melt(id_vars=['COMBUSTÍVEL', 'ANO', 'REGIÃO', 'ESTADO', 'UNIDADE'],
                             var_name='MES', value_name='VALOR')
        frames =[df_table_full, df_aux]
        df_table_full = pd.concat(frames)
    else:
        df_exemplo = pd.read_excel(excel, i)
df_table_full['timestamp_captura'] = timestamp_exec

print('Amostra:')
print(df_table_full.head(20))

df_table_full.to_csv(os.getcwd() + '/app/df_executado.csv')
df_table_full['MES'] = df_table_full.apply(mes_numero, axis=1)

conn = 'postgresql+psycopg2://test:test@db/test'
psql = create_engine(conn)
df_table_full.to_sql(name='sales', con=psql,
                     if_exists='replace', chunksize=1000, schema='public',
                     method='multi', index=False)
print('ETL EXECUTADO COM SUCESSO.')
