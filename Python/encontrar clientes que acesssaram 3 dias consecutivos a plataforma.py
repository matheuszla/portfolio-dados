# -*- coding: utf-8 -*-
#%% Instalando os pacotes
# pip install pandas numpy matplotlib seaborn plotly pytesseract opencv-python pillow

#%% Importar bibliotecas e definindo o caminho da imagem do banco

import pytesseract
import cv2
import pandas as pd
import re
from PIL import Image

# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Caminho da imagem
CAMINHO_IMAGEM = r"E:\elo group\Imagem1.jpg"

#%% verificar se a imagem esta abrindo corretamente

def abrir_imagem(caminho):
    img = Image.open(caminho)
    img.show()
    print(f"Formato: {img.format}, Tamanho: {img.size}, Modo: {img.mode}")

# Visualizar imagem
abrir_imagem(CAMINHO_IMAGEM)

#%% extraindo o texto da imagem

def extrair_texto_ocr(caminho):
    imagem = cv2.imread(caminho)
    return pytesseract.image_to_string(imagem)

# Extrair texto da imagem
texto_cru = extrair_texto_ocr(CAMINHO_IMAGEM)
print("Texto cru extraído:\n")
print(texto_cru)

#%% Corrigindo erros encontrados

def corrigir_ocr(texto):
    substituicoes = {
        'U?': 'U7', 'US': 'U5', 'UI': 'U1', 'ui': 'U1',
        '41': 'A1', 'Al': 'A1', 'A ': 'A1', 'Ud': 'U4',
        'AZ': 'A2', 'AS': 'A3'
    }
    for errado, certo in substituicoes.items():
        texto = texto.replace(errado, certo)
    return texto

# Corrigir texto
texto_corrigido = corrigir_ocr(texto_cru)
print("Texto corrigido:\n")
print(texto_corrigido)

#%% Estruturar os dados em DataFrame

def estruturar_dados(texto):
    linhas = texto.strip().split('\n')
    dados = []

    for linha in linhas:
        linha = linha.strip()
        if not linha:
            continue
#procura os dados de cada coluna 
        match_data = re.search(r'\d{4}-\d{2}-\d{2}', linha)
        if match_data:
            data = match_data.group()
            restante = linha.replace(data, '').strip()
            match_user_id = re.search(r'U\d+', restante)
            user_id = match_user_id.group() if match_user_id else ''
            account_id = restante.replace(user_id, '').strip()
#aloca os dados nas colunas correspondentes na lista 
            dados.append({'date': data, 'account_id': account_id, 'user_id': user_id})

    return pd.DataFrame(dados)

# Cria DataFrame estruturado
df = estruturar_dados(texto_corrigido)
print("Tabela estruturada:\n")
print(df)

#%% Encontrar a resposta questao 1

def usuarios_ativos_3_dias(df):
    df['date'] = pd.to_datetime(df['date']) 
    df = df.sort_values(['user_id', 'date']) #ordena por user_id
    df['diff'] = df.groupby('user_id')['date'].diff().dt.days #cria a coluna diff que calcula a diferença entre a data atual e a data anterior

    resultado = []
    for user, grupo in df.groupby('user_id'): #separa os usuarios com seu grupo de dados
        diffs = grupo['diff'].fillna(99).values #substitui os dados vazios por 99 para evitar erros na comparacao
        for i in range(len(diffs) - 2): # verifica usuario que tem diff = 1 duas vezes seguidas e adiciona na lista resultado
            if diffs[i] == 1 and diffs[i + 1] == 1:
                resultado.append(user)
                break

    return resultado

usuarios = usuarios_ativos_3_dias(df)
print("Usuários ativos por 3 dias consecutivos:\n")
print(usuarios)
