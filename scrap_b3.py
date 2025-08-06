import json
import requests
import base64
import pandas as pd
from datetime import datetime
import boto3
import io

def run_scrap():
    # Monta o payload e codifica em Base64
    payload = {
        "language": "pt-br",
        "pageNumber": 1,
        "pageSize": 200,
        "index": "IBOV",
        "segment": "1"
    }
    payload_b64 = base64.b64encode(json.dumps(payload).encode("utf-8")).decode()

    # Faz a requisição
    url = f"https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetPortfolioDay/{payload_b64}"
    response = requests.get(url)
    
    response.raise_for_status()

    try:
        data = response.json()
    except Exception as e:
        print("Erro ao interpretar JSON:", e)
        print("Resposta bruta:", response.text)
        return

    # Converte em DataFrame
    df = pd.DataFrame(data["results"])

    # Remove os pontos da 'theoricalQty'
    df['theoricalQty'] = df['theoricalQty'].str.replace('.', '', regex=False)

    # Data de extração 
    extraction_date = datetime.today().strftime('%Y-%m-%d')
    df['extraction_date'] = extraction_date

    # Nome do arquivo do Bucket S3
    file_name = f"raw/{extraction_date}/b3_{extraction_date}.parquet"
    bucket_s3 = "fiap-5mlet-tc2-b3-raw"

    # Converte para Parquet em memória
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)

    # Salva no S3
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_s3, Key=file_name, Body=buffer.getvalue())

    print(f"Arquivo enviado para s3://{bucket_s3}/{file_name}")

if __name__ == "__main__":
    run_scrap()
