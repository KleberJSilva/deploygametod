import pandas as pd
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

#Informações para fingir ser um navegador
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

#A url que você quer acesssar
url_link1 = "https://www.soccerstats.com/matches.asp?matchday=1&listing=1"
url_link2 = "https://www.soccerstats.com/matches.asp?matchday=1&listing=2"

#juntamos tudo com a requests
r1 = requests.get(url_link1, headers=header)
r2 = requests.get(url_link2, headers=header)

#E finalmente usamos a função read_html do pandas
df1 = pd.read_html(r1.text)
df2 = pd.read_html(r2.text)

jogos_today1 = df1[6]
jogos_today1 = jogos_today1[['Country','2.5+','1.5+','GA','GF','TG','PPG','Unnamed: 9','Unnamed: 10','Unnamed: 11','PPG.1','TG.1','GF.1','GA.1','1.5+.1','2.5+.1']]
jogos_today1.columns = ['País','Over25_H','Over15_H','GolsSofridos_H','GolsMarcados_H','MediaGols_H','PPG_H','Home','Hora','Away','PPG_A','MediaGols_A','GolsMarcados_A','GolsSofridos_A','Over15_A','Over25_A']

jogos_today2 = df2[6]
jogos_today2 = jogos_today2[['BTS','W%','BTS.1','W%.1']]
jogos_today2.columns = ['BTTS_H','%Vitorias_H','BTTS_A','%Vitorias_A']

jogos_today2 = df2[6]
jogos_today2 = jogos_today2[['BTS','W%','BTS.1','W%.1']]
jogos_today2.columns = ['BTTS_H','%Vitorias_H','BTTS_A','%Vitorias_A']

jogos_today = pd.concat([jogos_today1,jogos_today2],axis=1)
jogos_today = jogos_today[['País','Hora','Home','Away','%Vitorias_H','%Vitorias_A','Over15_H','Over25_H','Over15_A','Over25_A','BTTS_H','BTTS_A','GolsMarcados_H','GolsSofridos_H','GolsMarcados_A','GolsSofridos_A','MediaGols_H','MediaGols_A','PPG_H','PPG_A']]

jogos_today = jogos_today.sort_values('Hora')
jogos_today['Hora'] = pd.to_datetime(jogos_today['Hora']) - pd.DateOffset(hours=4)
jogos_today['Hora'] = pd.to_datetime(jogos_today['Hora'], format='%H:%M').dt.time
jogos_today = jogos_today.dropna()
# Resetando o Index
jogos_today.reset_index(inplace=True, drop=True)
jogos_today.index = jogos_today.index.set_names(['Nº'])
jogos_today = jogos_today.rename(index=lambda x: x + 1)
# Exportando para o Excel
jogos_today.to_excel("Jogos de Hoje.xlsx")


def enviar_email():  
  # Dados do remetente
  email_user = 'klebersccp.958@gmail.com'
  email_password = 'ddsmufqbrainbadg'
  email_send = 'kleber958@hotmail.com'

  # Criando a mensagem
  msg = MIMEMultipart()
  msg['From'] = email_user
  msg['To'] = email_send
  msg['Subject'] = 'Jogos do dia'

  # Anexando um arquivo
  filename = 'Jogos de Hoje.xlsx'
  attachment = open(filename, 'rb')
  part = MIMEBase('application', 'octet-stream')
  part.set_payload((attachment).read())
  encoders.encode_base64(part)
  part.add_header('Content-Disposition', "attachment; filename= " + filename)

  # Adicionando o corpo da mensagem e o anexo
  msg.attach(MIMEText("Aqui estão os jogos de amanhã"))
  msg.attach(part)

  # Enviando o email
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(email_user, email_password)
  text = msg.as_string()
  server.sendmail(email_user, email_send, text)
  server.quit()

enviar_email()


