import requests
import os
from dotenv import load_dotenv

def sendMail(who, token):
    load_dotenv("mail.env")
    
    api_key = os.getenv("RESEND_API_KEY")
    
    data = {
        "from": "espeon@mieiro.online",
        "to": who,
        "subject": "Código de Acesso - ESPEON",
        "html": f"<p>Aqui está seu código de acesso: <strong>{token}</strong></p>",
        "text": f"Aqui está seu código de acesso: {token}"
    }
    
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            json=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"[EMAIL]Enviado para {who}")
            return True
        else:
            print(f"[EMAIL]Erro: {response.text}")
            return False
    except Exception as e:
        print(f"[EMAIL]Erro na API: {e}")
        return False