# pegar todos os logs de uma collection
# transformar em dicionário
import requests


def findAllTraces(subject):
    try:
        url = f"http://localhost:8183/traces/{subject}"
        response = requests.get(url)
        print(f"Response para {subject}: {response}")
        return response.json()
    except Exception as e:
        raise Exception(
            f"[SERVICE] An error occurred while attempting to get traces from '{subject}': {e}")
    
def extractField(data, field):
    extractedData = []
    for d in data:
        if field in d:
            extractedData.append(d[field])
    return extractedData
