import pandas as pd
import win32com.client as win32

# importar a base de dados
tabela_vendas = pd.read_excel('Vendas.xlsx') 

# visualizar a base de dados
pd.set_option('display.max_columns', None)
print(tabela_vendas)
print('-'*50)
# faturamento por loja 
faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)
print('-'*50)
# quantidade de produtos vendidos por loja
quantidade = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(quantidade)

print('-'*50)
# ticket medio por produto vendido por loja
ticket_medio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
print(ticket_medio)
print('-'*50)

# enviar um email para as lojas
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'martinsgrigolenzotech@gmail.com'
mail.Subject = 'Relatório de Vendas por Loja'
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.</p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade Vendida:</p>
{quantidade.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Att.,</p>
<p>Enzo</p>
'''

mail.Send()