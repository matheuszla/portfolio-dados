#%% Importar bibliotecas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%% Carregar os dados
# Carregar os dados CSV
clientes = pd.read_csv('E:\Portifolio\Projeto Imobiliario\clientes.csv')
contratos = pd.read_csv('E:\Portifolio\Projeto Imobiliario\contratos.csv')

# Verificar os primeiros registros
print(clientes.head())
print(contratos.head())

#%% Verificar e tratar valores nulos
# Verificar valores nulos
print("\nValores nulos - Clientes:\n", clientes.isnull().sum())
print("\nValores nulos - Contratos:\n", contratos.isnull().sum())

# Tratamento de valores nulos
clientes['renda_mensal'].fillna(clientes['renda_mensal'].mean(), inplace=True)
clientes['idade'].fillna(clientes['idade'].mean(), inplace=True)

# Verificar se os nulos foram tratados
print("\nApós tratamento:\n", clientes.isnull().sum())

#%% Gráfico da distribuição da idade dos clientes
plt.figure(figsize=(8,6))
sns.histplot(clientes['idade'], bins=20, kde=True, color='skyblue')
plt.title('Distribuição da Idade dos Clientes')
plt.xlabel('Idade')
plt.ylabel('Frequência')
plt.show()

#%% Analisar correlação entre idade, renda e valor financiado
# Juntar contratos com clientes
df_merged = pd.merge(contratos, clientes, on='cliente_id')

# Calcular correlação
corr = df_merged[['idade', 'renda_mensal', 'valor_financiado']].corr()
print("\nCorrelação entre Idade, Renda Mensal e Valor Financiado:\n", corr)

# Plotar heatmap da correlação
plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap='Blues')
plt.title('Mapa de Correlação')
plt.show()

#%% Gráfico de contratos por status
plt.figure(figsize=(7,5))
sns.countplot(data=contratos, x='status_contrato', palette='pastel')
plt.title('Total de Contratos por Status')
plt.xlabel('Status do Contrato')
plt.ylabel('Quantidade')
plt.show()
