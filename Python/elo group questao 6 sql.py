#%% Instalando os pacotes
# # pip install pandas numpy matplotlib seaborn plotly pytesseract opencv-python pillow
#%% Subindo as imagens para análise

from PIL import Image  # Biblioteca usada para abrir e manipular imagens.

# Define o caminho da imagem no seu computador.
caminho = r"E:\elo group\tabela funcionarios.png"

# Abre a imagem
tabelafun = Image.open(caminho)

# Mostra a imagem na tela
tabelafun.show()


#%% Extraindo texto da imagem com Tesseract

import pytesseract  # Ferramenta que converte imagem em texto (OCR).
import cv2  
# Configura o caminho do executável do Tesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Lê a imagem usando OpenCV para poder aplicar o OCR.
imagem = cv2.imread(r"E:\elo group\tabela funcionarios.png")

# Usa o pytesseract para extrair o texto da imagem.
texto = pytesseract.image_to_string(imagem)

# Imprime o texto extraído
print("Texto extraído:")
print(texto)
