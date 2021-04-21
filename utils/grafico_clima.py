
import datetime
import pandas as pd
from plotly.offline import plot
import plotly.figure_factory as ff


def gerando_grafico (arq_cor, tipo_dado, data_inicial, data_final):
    if tipo_dado:
        arq_cor_del = arq_cor.loc[0::, ["Data Medicao", str(tipo_dado)]]
    else:
        arq_cor_del = arq_cor.iloc[0::, [0, 7]]


    arq_cor_del["TEMPERATURA DO AR"] = arq_cor_del.iloc[0::, [1]]

    df_gantt = arq_cor_del.copy()

    arq_cor_del.dropna(inplace=True)
    arq_cor_del.reset_index(inplace=True)
    del arq_cor_del["index"]
    coluna = arq_cor_del.columns[1]
    diagrama = False

    del arq_cor_del[arq_cor_del.columns[1]]

    arq_cor_del.replace({',': '.'}, regex=True, inplace=True)

    arq_cor_del["Data"] = arq_cor_del["Data Medicao"]
    del arq_cor_del["Data Medicao"]


    arq_cor_del["TEMPERATURA DO AR"] = pd.to_numeric(arq_cor_del["TEMPERATURA DO AR"])

    agrupando2_maximo = arq_cor_del.iloc[0::, [0, 1]].groupby("Data").max()
    agrupando2_minimo = arq_cor_del.iloc[0::, [0, 1]].groupby("Data").min()
    agrupando2_media = arq_cor_del.iloc[0::, [0, 1]].groupby("Data").mean()

    agrupando2_data = agrupando2_maximo.reset_index()
    agrupando2_data["TEMPERATURA DO AR"] = agrupando2_data["Data"]
    agrupando2_data.set_index("Data", inplace=True)


    agrupando2_data["TEMPERATURA DO AR"] = pd.DataFrame(agrupando2_data["TEMPERATURA DO AR"].apply(
        lambda Mes: int(datetime.datetime(
            *datetime.date(int(Mes[0:4]), int(Mes[5:7]), int(Mes[8::])).timetuple()[:3]).timestamp() * 1000)
    )
    )

    concatenando = pd.concat([agrupando2_data, agrupando2_minimo, agrupando2_maximo])
    concatenando.reset_index(inplace=True)

    agrupando_max_min = concatenando[["TEMPERATURA DO AR", "Data"]].groupby("Data").agg(
        lambda x: list(set(x))).reset_index()

    concatenando_media = pd.concat([agrupando2_data, agrupando2_media])
    concatenando_media.reset_index(inplace=True)
    agrupando_data_media = concatenando_media[["TEMPERATURA DO AR", "Data"]].groupby("Data").agg(
        lambda x: list(set(x))).reset_index()


    arquivo_referencia = agrupando_data_media.copy()

    if data_inicial:
        diagrama = gantt(df_gantt, data_inicial, data_final)
        agrupando_data_media['Data'] = pd.to_datetime(agrupando_data_media['Data'])
        agrupando_data_media['Data'] = agrupando_data_media['Data'].dt.strftime("%Y-%m-%d")
        agrupando_data_media.set_index("Data", inplace=True)
        agrupando_data_media = agrupando_data_media.loc[str(data_inicial):str(data_final)]
        agrupando_data_media.reset_index(inplace=True)

        agrupando_max_min['Data'] = pd.to_datetime(agrupando_max_min['Data'])
        agrupando_max_min['Data'] = agrupando_max_min['Data'].dt.strftime("%Y-%m-%d")
        agrupando_max_min.set_index("Data", inplace=True)
        agrupando_max_min = agrupando_max_min.loc[str(data_inicial):str(data_final)]
        agrupando_max_min.reset_index(inplace=True)




    array_max_min = list(agrupando_max_min["TEMPERATURA DO AR"].values)
    array_media = list(agrupando_data_media["TEMPERATURA DO AR"].values)

    IC_max_min = []
    for i in range(0, len(array_max_min)):
        if len(array_max_min[i])==2:
            array_max_min[i].append(array_max_min[i][1])
        numeros_ordenados = sorted(array_max_min[i], reverse=True)
        numeros_ordenados_2 = numeros_ordenados.copy()
        del numeros_ordenados_2[0]
        numeros_ordenados_2 = sorted(numeros_ordenados_2)
        numeros_ordenados_2.insert(0, int(numeros_ordenados[0]))
        IC_max_min.append(numeros_ordenados_2)

    IC_media = []
    for i in range(0, len(array_max_min)):
        numeros_ordenados = sorted(array_media[i], reverse=True)
        numeros_arredondados = round(numeros_ordenados[1], 2)
        del numeros_ordenados[1]
        numeros_ordenados.insert(1, numeros_arredondados)
        IC_media.append(numeros_ordenados)

    return IC_max_min, IC_media, agrupando_data_media, arquivo_referencia, coluna, diagrama


def gantt (df_gantt,data_inicial,data_final):
    df_gantt["Data"] = df_gantt["Data Medicao"]
    del df_gantt["Data Medicao"]
    df_gantt = df_gantt.iloc[0::, [0,-1]]
    df_gantt['Data'] = pd.to_datetime(df_gantt['Data'])
    df_gantt['Data'] = df_gantt['Data'].dt.strftime("%Y-%m-%d")
    df_gantt.reset_index(inplace=True)
    df_gantt.set_index("Data", inplace=True)
    gantt = df_gantt.loc[str(data_inicial):str(data_final)]
    gantt.reset_index(inplace=True)
    gantt_principal = gantt.copy()
    gantt = gantt.iloc[0::, [2]]

    gantt_nan = preparando_nan(gantt_principal,data_inicial,data_final)

    df_dados = preparando_dados(gantt, gantt_principal)

    df_unidos = pd.concat([df_dados,gantt_nan])

    colors = ["rgb(220, 0, 0)", "rgb(0, 0, 0)"]
    gantt = ff.create_gantt(df_unidos, colors=colors,
                            show_colorbar=True, bar_width=0.50, showgrid_x=True, showgrid_y=True,
                            group_tasks=True, height=275, title="Diagrama de Gantt", index_col="Resource")

    diagrama= plot(gantt, auto_open=False, output_type='div')

    return diagrama



def preparando_dados(gantt, gantt_principal):
    gantt_dados = gantt.dropna().index.to_series()

    start = gantt_dados[gantt_dados.diff(1) != 1].reset_index(drop=True)
    end = gantt_dados[gantt_dados.diff(-1) != -1].reset_index(drop=True)
    df_dados = pd.DataFrame({'Start': start, 'Finish': end, "Task": "Dados", "Resource": "Contém Dados"},
                            columns=['Start', 'Finish', "Task", "Resource"])


    df_dados["Start"] = pd.DataFrame(df_dados["Start"].apply(
        lambda indice: f'{gantt_principal["Data"][indice]} 00:00:00'
    )

    )
    df_dados["Finish"] = pd.DataFrame(df_dados["Finish"].apply(
        lambda indice: f'{gantt_principal["Data"][indice]} 23:59:59'
    )
    )

    df_dados = df_dados.drop_duplicates(subset='Start', keep='last')

    return df_dados



def preparando_nan(gantt_principal,data_inicial,data_final):
    gannt_ausente = gantt_principal.dropna()
    gannt_ausente = gannt_ausente.drop_duplicates(subset='Data', keep='last')
    gannt_ausente["Data"] = pd.to_datetime(gannt_ausente["Data"])
    gannt_ausente.set_index("Data", inplace=True)
    date_index2 = pd.date_range(start=data_inicial,end= data_final, freq="D")
    gannt_ausente = gannt_ausente.reindex(date_index2)
    gannt_ausente = gannt_ausente.isnull()

    gannt_ausente = gannt_ausente[gannt_ausente["index"]==True]

    gannt_ausente.reset_index(inplace=True)

    gannt_ausente["level_0"] = gannt_ausente["level_0"].dt.strftime("%Y/%m/%d")

    gannt_ausente["Data"] = pd.DataFrame(gannt_ausente["level_0"].apply(
        lambda Mes: int(datetime.datetime(
            *datetime.date(int(Mes[0:4]), int(Mes[5:7]), int(Mes[8::])).timetuple()[:3]).timestamp())
    )
    )
    gannt_ausente = gannt_ausente.iloc[0::, [3]]
    ausente = list(gannt_ausente["Data"].values)
    intervalo_nan = pd.Series(ausente)

    start = intervalo_nan[intervalo_nan.diff(1) != 86400].reset_index(drop=True)
    end = intervalo_nan[intervalo_nan.diff(-1) != -86400].reset_index(drop=True)
    gantt_nan = pd.DataFrame({'Start': (start-10799), 'Finish': (end+75599), "Task": "Dados", "Resource": "Dados Ausentes"}
                             , columns=['Start', 'Finish', "Task", "Resource"])

    gantt_nan['Start'] = gantt_nan['Start'].astype('datetime64[s]')
    gantt_nan['Finish'] = gantt_nan['Finish'].astype('datetime64[s]')
    return gantt_nan












