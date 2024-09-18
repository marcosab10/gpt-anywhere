import os
import json
import google.generativeai as genai

def lambda_handler(event, context):
    # Recuperar a chave da API da variável de ambiente
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Permite requisições de qualquer origem
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": "API key is not set in environment variables"})
        }

    # Configurar a chave da API
    genai.configure(api_key=api_key)

    # Extrair o corpo da requisição e fazer o parsing do JSON
    try:
        body = json.loads(event.get("body", "{}"))
        prompt = body.get("prompt", "Escreva exatamente a mensagem: 'Em que posso ajudar?'")
    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Permite requisições de qualquer origem
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": "Invalid JSON in request body"})
        }

    try:
        # Usar o modelo para gerar o conteúdo
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Retornar a resposta gerada pela API
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Permite requisições de qualquer origem
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "message": response.text
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Permite requisições de qualquer origem
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({
                "error": "Failed to generate content",
                "details": str(e)
            }),
        }
