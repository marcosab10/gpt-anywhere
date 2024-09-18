import os
import boto3
import pytest
import requests

"""
Certifique-se de que a variável de ambiente AWS_SAM_STACK_NAME exista com o nome da stack que vamos testar.
"""

class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """ Obtém a URL do API Gateway a partir das saídas da CloudFormation Stack """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Por favor, defina a variável de ambiente AWS_SAM_STACK_NAME com o nome da sua stack')

        client = boto3.client("cloudformation")

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Não foi possível encontrar a stack {stack_name}. \n"
                f'Certifique-se de que uma stack com o nome "{stack_name}" existe.'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "PromptLambdaFunctionApi"]

        if not api_outputs:
            raise KeyError(f"API Gateway não encontrado na stack {stack_name}")

        return api_outputs[0]["OutputValue"]  # Extrair a URL da saída da stack

    def test_api_gateway(self, api_gateway_url):
        """ Faz uma chamada ao endpoint do API Gateway e verifica a resposta """
        headers = {
            "Content-Type": "application/json"
        }

        # Definir o corpo da requisição com um prompt de teste
        data = {
            "prompt": "Test prompt"
        }

        # Faz uma requisição POST para o endpoint
        response = requests.post(api_gateway_url, json=data, headers=headers)

        # Verificar o código de status da resposta
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

        # Verificar se a resposta contém a chave "message"
        response_json = response.json()
        assert "message" in response_json, f"Expected 'message' in response, got {response_json}"

        # Verificar que a mensagem não está vazia
        assert response_json["message"], "Expected non-empty 'message' in response"
