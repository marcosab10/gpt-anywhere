# GPT Anywhere

## Guia rápido de utilização

Para usar a SAM CLI, você precisa das seguintes ferramentas:

* **SAM CLI** - [Instalar a SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* **Python 3.11 instalado** - [Baixar Python](https://www.python.org/downloads/)
* **Docker (opcional)** - [Instalar a edição comunitária do Docker](https://hub.docker.com/search/?type=edition&offering=community)

Na pasta do projeto executar:

```
$ aws configure

$ sam build; sam deploy
```

* Com isso irá obter como saída o endpoint do API Gateway  
Exemplo: https://utbppwr2uk.execute-api.us-east-2.amazonaws.com/Prod/

* E o link do CloudFront para o site estático exemplo: https://d36uoj13cjssno.cloudfront.net

* Precisa configurar a variável de ambiente `GENAI_API_KEY` nas propriedades da função lambda criada, informando a API KEY do Google AI.

* Realizar o upload do arquivo `index.html` no bucket S3 que inicia com o nome `static-site-XXXXX`

* Ao carregar o site estático em um browser, deve informar o endpoint do API Gateway no primeiro campo e então é só usar :)

![gpt](front.PNG)


Este projeto contém o código-fonte e arquivos de suporte para uma aplicação *serverless* que você pode implantar com a SAM CLI. Ele inclui os seguintes arquivos e pastas:

- **gpt** - Código para a função Lambda da aplicação e index.html para o site estático
- **events** - Eventos de invocação que você pode usar para invocar a função.
- **tests** - Testes unitários para o código da aplicação.
- **template.yaml** - Um modelo que define os recursos AWS da aplicação.

A aplicação usa vários recursos da AWS, incluindo funções Lambda e uma API do API Gateway. Esses recursos estão definidos no arquivo `template.yaml` deste projeto. Você pode atualizar o modelo para adicionar recursos AWS através do mesmo processo de implantação que atualiza o código da sua aplicação.

## Implantar a aplicação

A Interface de Linha de Comando do Modelo de Aplicação *Serverless* (SAM CLI) é uma extensão da AWS CLI que adiciona funcionalidade para criar e testar aplicações Lambda. Ela usa o Docker para executar suas funções em um ambiente Amazon Linux que corresponde ao Lambda. Também pode emular o ambiente de criação da sua aplicação e a API.



Para criar e implantar sua aplicação pela primeira vez, execute o seguinte no seu terminal:

```bash
sam build --use-container
sam deploy --guided
```

O primeiro comando criará o código-fonte da sua aplicação. O segundo comando empacota e implanta sua aplicação na AWS, com uma série de solicitações:

* Nome da Stack: O nome da stack para implantar no CloudFormation. Isso deve ser único para sua conta e região, e um bom ponto de partida seria algo que corresponda ao nome do seu projeto.

* Região da AWS: A região da AWS onde você deseja implantar sua aplicação.
Confirmar alterações antes da implantação: Se configurado como "sim", quaisquer conjuntos de alterações serão mostrados antes da execução para revisão manual. Se configurado como "não", a AWS SAM CLI implantará automaticamente as alterações da aplicação.

* Permitir a criação de funções IAM pela SAM CLI: Muitos modelos AWS SAM, incluindo este exemplo, criam funções AWS IAM necessárias para as funções AWS Lambda incluídas acessarem os serviços AWS. Por padrão, elas são limitadas às permissões mínimas necessárias. Para implantar uma stack do AWS CloudFormation que cria ou modifica funções IAM, o valor CAPABILITY_IAM para capabilities deve ser fornecido. Se a permissão não for fornecida por meio desta solicitação, para implantar este exemplo você deve passar explicitamente --capabilities CAPABILITY_IAM para o comando sam deploy.

* Salvar argumentos em samconfig.toml: Se configurado como "sim", suas escolhas serão salvas em um arquivo de configuração dentro do projeto, para que no futuro você possa simplesmente executar sam deploy sem parâmetros para implantar alterações na sua aplicação.

Você pode encontrar a URL do seu API Gateway nos valores de saída exibidos após a implantação.

## Usar a SAM CLI para criar e testar localmente
Crie sua aplicação com o comando `sam build --use-container`.


```bash
gpt-anywhere$ sam build --use-container
```

A SAM CLI instala as dependências definidas em `gpt/requirements.txt`, cria um pacote de implantação e o salva na pasta `.aws-sam/build`

Teste uma função individual invocando-a diretamente com um evento de teste. Um evento é um documento JSON que representa a entrada que a função recebe da fonte do evento. Eventos de teste estão incluídos na pasta `events` deste projeto.

Execute funções localmente e invoque-as com o comando `sam local invoke`.



```bash
gpt-anywhere$ sam local invoke GPTFunction --event events/event.json
```
A SAM CLI também pode emular a API da sua aplicação. Use o`sam local start-api` para executar a API localmente na porta 3000.

```bash
gpt-anywhere$ sam local start-api
gpt-anywhere$ curl http://localhost:3000/
```

A SAM CLI lê o modelo da aplicação para determinar as rotas da API e as funções que elas invocam. A propriedade `Events` na definição de cada função inclui a rota e o método para cada caminho.


```yaml
      Events:
        GPT:
          Type: Api
          Properties:
            Path: /
            Method: post
```

## Adicionar um recurso à sua aplicação
O modelo da aplicação usa o AWS Serverless Application Model (AWS SAM) para definir os recursos da aplicação. O AWS SAM é uma extensão do AWS CloudFormation com uma sintaxe mais simples para configurar recursos comuns de aplicações serverless, como funções, acionadores e APIs. Para recursos não incluídos na  [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), você pode usar os tipos de recursos padrão do [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html).



## Obter, monitorar e filtrar logs das funções Lambda
Para simplificar a solução de problemas, a SAM CLI tem um comando chamado `sam logs`. `sam logs` permite que você obtenha os logs gerados pela função Lambda implantada a partir da linha de comando. Além de imprimir os logs no terminal, este comando tem vários recursos úteis para ajudá-lo a encontrar rapidamente o erro.

`NOTA`: Este comando funciona para todas as funções AWS Lambda, não apenas para as que você implanta usando o SAM.


```bash
gpt-anywhere$ sam logs -n GPTFunction --stack-name "gpt-anywhere" --tail
```

Você pode encontrar mais informações e exemplos sobre filtragem de logs de funções Lambda na [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Testes
Os testes são definidos na pasta `tests` deste projeto. Use o PIP para instalar as dependências dos testes e executar os testes.


```bash
gpt-anywhere$ pip install -r tests/requirements.txt --user
# unit test
gpt-anywhere$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
gpt-anywhere$ AWS_SAM_STACK_NAME="gpt-anywhere" python -m pytest tests/integration -v
```

## Limpeza
Para excluir a aplicação de exemplo que você criou, use a AWS CLI. Supondo que você tenha usado o nome do seu projeto para o nome da stack, você pode executar o seguinte:

```bash
sam delete --stack-name "gpt-anywhere"
```

## Recursos
Veja o [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) para uma introdução à especificação SAM, à SAM CLI e aos conceitos de aplicações serverless.

Em seguida, você pode usar o Repositório de Aplicações Serverless da AWS para implantar aplicativos prontos para uso que vão além dos exemplos de GPT e aprender como os autores desenvolveram suas aplicações:[AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)

