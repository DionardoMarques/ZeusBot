import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def botStarted(start_date):
    message = EmailMessage()

    message['Subject'] = 'ZeusBot Iniciado'
    message['From'] = 'email.sam@tlsv.com.br'
    message['To'] = 'dionardo.marques@tlsv.com.br'
    
    message.set_content(f"ZeusBot iniciado na data e hora: {start_date}")

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)

def botFinished(end_date, start_date, duration, zeus_data):
    message = EmailMessage()

    message['Subject'] = 'ZeusBot Finalizado'
    message['From'] = 'email.sam@tlsv.com.br'
    message['To'] = 'dionardo.marques@tlsv.com.br'
    
    message.set_content(f"\nTotal atividades: {str(len(zeus_data))}\nTempo total: {str(duration)}\nData e hora inicio: {str(start_date)}\nData e hora fim: {str(end_date)}")

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)

def wrongPassword():
    message = EmailMessage()

    message['Subject'] = 'ZeusBot Senha Errada'
    message['From'] = 'email.sam@tlsv.com.br'
    message['To'] = 'importacao.falhas@tlsv.com.br'
    
    message.set_content("Foram realizadas 7 tentativas de login no ZEUS. Provavelmente a senha está incorreta.")

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)