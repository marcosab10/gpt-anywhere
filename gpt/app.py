import os
import json
import google.generativeai as genai

def lambda_handler(event, context):
    # Recuperar a chave da API da variável de ambiente
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "API key is not set in environment variables"})
        }

    # Configurar a chave da API
    genai.configure(api_key=api_key)

    # Extrair o prompt do evento, com um valor padrão caso não seja fornecido
    prompt = event.get("prompt", "Escreva extamente a mensagem: 'Em que posso ajudar?'")

    try:
        # Usar o modelo para gerar o conteúdo
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)

        # Retornar a resposta gerada pela API
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": response.text
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Failed to generate content",
                "details": str(e)
            }),
        }
