from django.shortcuts import render
from django.views.generic import View
import pandas as pd
import datetime
from utils.grafico_clima import gerando_grafico
from .templatetags.filtro_select import concatenando_string, removendo_string
import os

class Clima(View):
    def get(self, *args, **kwargs):
        if self.request.GET:
            nome_arquivo = self.request.GET.get("arquivo")
            titulo = concatenando_string(nome_arquivo)
            requisicao = True
        else:
            requisicao = False
            nome_arquivo = "dados_A327_PALMEIRA DOS INDIOS_2010-01-01_2020-12-31.csv"
            titulo= ""

        todos_arq = os.listdir("arquivos")


        arq_cor = pd.read_csv(f"arquivos/{nome_arquivo}", header=9, sep=";", encoding="cp1252")
        tipo_dado = self.request.GET.get("tipo_dado")
        sufixo = arq_cor.columns[2:-1]

        data_inicial = self.request.GET.get("data_inicial")
        data_final = self.request.GET.get("data_final")

        IC_max_min, IC_media, agrupando_data_media, arquivo_referencia, coluna, diagrama =\
            gerando_grafico(arq_cor, tipo_dado, data_inicial, data_final)


        context = {
            "categories": IC_max_min,
            'values': IC_media,
            'data_inicial_filtro': str(agrupando_data_media['Data'][0]).replace('/', '-'),
            'data_final_filtro': str(agrupando_data_media['Data'][len(agrupando_data_media["Data"]) - 1]).replace('/', '-'),
            'data_inicial': str(arquivo_referencia['Data'][0]).replace('/', '-'),
            'data_final': str(arquivo_referencia['Data'][len(arquivo_referencia["Data"]) - 1]).replace('/', '-'),
            'colunas': str(coluna),
            'requisicao': requisicao,
            'sufixo': sufixo,
            'todos_arq': todos_arq,
            'titulo': titulo,
            'diagrama': diagrama
        }

        return render(self.request, "clima/caracterizando_clima.html", context=context)


def index (request):
    return render(request, "clima/index.html")

