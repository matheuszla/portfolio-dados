# %% Instalar pacotes (descomente e execute apenas uma vez)
# !pip install pandas numpy matplotlib seaborn plotly pytesseract opencv-python pillow
# %% Configuração inicial
import cv2
import pytesseract
import pandas as pd
from PIL import Image


# Caminhos
caminho_tabela = r"E:\elo group\tabela.jpeg"

# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#%% verificar se a imagem esta abrindo corretamente
def carregar_imagem(caminho):
    imagem = Image.open(caminho)
    imagem.show()
    print(f"Formato: {imagem.format}, Tamanho: {imagem.size}, Modo: {imagem.mode}")
    
# Visualizar imagem
carregar_imagem(caminho_tabela)
#%% extraindo o texto da imagem
def extrair_texto_ocr(caminho_imagem):
    imagem_cv = cv2.imread(caminho_imagem)
    texto = pytesseract.image_to_string(imagem_cv)
    print("Texto extraído:")
    print(texto)
    return texto

texto_extraido = extrair_texto_ocr(caminho_tabela)
#%% Processar os dados e transformar em Dataframe
def processar_texto_para_dataframe(texto):
    linhas = texto.strip().split('\n')
    if 'Date' in linhas[0]:
        linhas = linhas[1:]
    
    dados = []
    for linha in linhas:
        partes = linha.split()
        if len(partes) >= 4:
            data = partes[0]
            account_id = partes[2]
            user_id = partes[3]
            dados.append([data, account_id, user_id])
    
    df = pd.DataFrame(dados, columns=['Date', 'account_id', 'user_id'])
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    print(df)
    return df

df = processar_texto_para_dataframe(texto_extraido)
#%% Função para calcular taxa de retenção entre Dez/2022 e Jan/2023
def calcular_taxa_retencao(df):
    dez_2022 = df[(df['Date'].dt.year == 2022) & (df['Date'].dt.month == 12)] #Dataframe so com registros de dezembro 2022
    jan_2023 = df[(df['Date'].dt.year == 2023) & (df['Date'].dt.month == 1)]  #Dataframe so com registros de janeiro de 2023

    colabs_dez = dez_2022.groupby('account_id')['user_id'].apply(set).to_dict() #Agrupado por account_id de forma unica em dezembro 2022
    colabs_jan = jan_2023.groupby('account_id')['user_id'].apply(set).to_dict() #Agrupado por account_id de forma unica em janeiro 2023
    todos_accounts = set(colabs_dez) | set(colabs_jan) #Uniao dos conjuntos, para garantir que mesmo que so tenha em um conjunto nao ser ignorada

    retencao = {}
    for acc in todos_accounts: # para evitar erros nos calculos, garante que o conjunto exista mesmo vazio
        dez_colabs = colabs_dez.get(acc, set())
        jan_colabs = colabs_jan.get(acc, set())
        if len(dez_colabs) == 0:
            taxa = 0
        else:
            taxa = len(dez_colabs & jan_colabs) / len(dez_colabs) * 100
        retencao[acc] = taxa

    retencao_df = pd.DataFrame(retencao.items(), columns=['account_id', 'taxa_retencao'])
    retencao_df['taxa_retencao'] = retencao_df['taxa_retencao'].map('{:.2f}%'.format)
    retencao_df = retencao_df.sort_values(by='taxa_retencao', ascending=False).reset_index(drop=True)
    print(retencao_df)
    return retencao_df

retencao_df = calcular_taxa_retencao(df)
