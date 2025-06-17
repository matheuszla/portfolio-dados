# -*- coding: utf-8 -*-
#%% Instalação de pacotes
# pip install pandas numpy matplotlib seaborn plotly pytesseract opencv-python pillow

#%% Importar bibliotecas
from PIL import Image
import cv2
import pytesseract
import pandas as pd
import re

##Configurar o caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

## Caminhos das imagens
caminho_salario = r"E:\elo group\tabsal.jpg"
caminho_cargo = r"E:\elo group\tabcargo2.jpg"  # Usamos só essa imagem agora

#%% Função para abrir imagem e mostrar propriedades
def abrir_imagem(caminho):
        img = Image.open(caminho)
        img.show()
        print(f"Imagem: {caminho}")
        print(f"Formato: {img.format}, Tamanho: {img.size}, Modo: {img.mode}")
        
abrir_imagem(caminho_cargo)
abrir_imagem(caminho_salario)

#%% Função para extrair texto 
def extrair_texto_ocr(caminho_img):
        img_cv = cv2.imread(caminho_img)
        texto = pytesseract.image_to_string(img_cv)
        return texto

texto_salario = extrair_texto_ocr(caminho_salario)
texto_cargo = extrair_texto_ocr(caminho_cargo)


print("\n" + "="*50)
print("Texto extraído da imagem de SALÁRIO:\n")
print(texto_salario)

print("\n" + "="*50)
print("Texto extraído da imagem de CARGO:\n")
print(texto_cargo)

#%% Processar os dados de cargo e colocar eles em Data Frame

def processar_tabela_cargo(texto_cargo):
    linhas = texto_cargo.strip().split('\n')
    dados = []
    for linha in linhas[1:]:  # ignorar cabeçalho
        partes = linha.strip().split(maxsplit=1) #separa no maximo ate um espaço
        if len(partes) != 2:
            continue
        id_ = partes[0]
        cargo_data = partes[1]
        match = re.search(r'(\d{2}/\d{2}/\d{4})$', cargo_data) #regex para retirar a data
        if match:
            data = match.group(1)
            cargo = cargo_data[:match.start()].strip() #pega o que esta antes da data que é o cargo
        else:
            data = 'none'
            cargo = cargo_data.strip() #se for nulo pega tudo
        dados.append({'ID': id_, 'Cargo': cargo, 'Data': data})
    df = pd.DataFrame(dados)
    print("\nTabela Cargo processada:")
    print(df)
    return df

df_cargo = processar_tabela_cargo(texto_cargo)
#%% Processar os dados de salario e colocar eles em Data Frame

def processar_tabela_salario(texto_salario):
    linhas = texto_salario.strip().split('\n')
    dados = []
    for linha in linhas:
        partes = linha.strip().split()
        if len(partes) < 5 or not partes[0].isdigit(): #ignora linhas que tem menos de 5 partes
            continue
        id_ = partes[0]
        idx_data = None #procura o dado de data e salva a posiçao
        for i, parte in enumerate(partes):
            if re.match(r'\d{2}/\d{2}/\d{4}', parte):
                idx_data = i
                break
        if idx_data is None or idx_data < 3: 
            continue
        data = partes[idx_data]
        salario = partes[idx_data - 1]
        nome_completo = ' '.join(partes[1:idx_data - 1]).replace('_', '').strip() #junta as partes 2 e 3 por conta do nome composto
        departamento = ' '.join(partes[idx_data + 1:])
        dados.append({'ID': id_, 'Nome': nome_completo, 'Salario': salario, 'Data': data, 'Departamento': departamento})
    df = pd.DataFrame(dados)
    print("\nTabela Salário processada:")
    print(df)
    return df

df_salario = processar_tabela_salario(texto_salario)
#%% Junta os dois DataFrames fazendo um left join para trazer os colaboradores com seus salarios e cargos em uma tabela
def unir_tabelas(df_salario, df_cargo):
    df_merged = pd.merge(df_salario, df_cargo, on='ID', how='left')
    print("\nTabela Unificada:")
    print(df_merged)
    return df_merged

df_geral = unir_tabelas(df_salario, df_cargo)
#%% Encontrar a resposta da questao 2

def maior_salario_e_cargos(df_geral):
    df_geral['Salario'] = pd.to_numeric(df_geral['Salario'], errors='coerce') #converte salario para numerico
    df_validos = df_geral.dropna(subset=['Cargo']) #exclui cargos vazios
    maior_salario = df_validos['Salario'].max()
    cargos_maior = df_validos[df_validos['Salario'] == maior_salario]['Cargo'].unique() #verifica quais cargos tem o salario max encontrado
    print(f"\nO maior salário da empresa é de R$ {maior_salario:,.2f} e os cargos que possuem esse salário são: {' e '.join(cargos_maior)}.")

maior_salario_e_cargos(df_geral)
