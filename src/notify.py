import win32com.client as win32

def wrongPassword(start_date):
    outlook = win32.Dispatch('outlook.application')
    
    mail = outlook.CreateItem(0)
    # mail.To = 'importacao.falhas@tlsv.com.br'
    mail.To = 'dionardo.marques@tlsv.com.br'
    mail.Subject = 'Senha errada ZeusBot'
    mail.Body = 'Houveram 7 tentativas de login e todas falharam. Possivelmente a senha atual está desatualizada.'
    # mail.HTMLBody = '<h2>HTML Message body</h2>' #this field is optional

    # To attach a file to the email (optional):
    # attachment  = "Path to the attachment"
    # mail.Attachments.Add(attachment)

    mail.Send()