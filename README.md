[![verifica_notas](https://github.com/andrewalkermo/AnSIAC/actions/workflows/run.yaml/badge.svg?event=schedule)](https://github.com/andrewalkermo/AnSIAC/actions/workflows/run.yaml)

# AnSIAC

Verifica se já botaram a minha nota no SIAC. 

Se tiver alguma nota nova desde a última verificação ele manda uma mensagem no Telegram. 

## Pré-requisitos
- Criar um bot no Telegram com o [@BotFather](https://t.me/BotFather) e pegar o token.
- Iniciar uma conversa com o bot e pegar o seu ID com o [@userinfobot](https://t.me/userinfobot).

## Como usar

### Fork no GitHub
O GitHub Actions vai executar o script a cada 5 minutos. ou manualmente clicando em "Run workflow" na página do Actions.

1. Clique no botão "Fork" no canto superior direito da página.
2. Clique no botão "Settings" no canto superior direito da página.
3. Clique em "Secrets" no menu lateral esquerdo.
4. Clique em "New repository secret" no canto superior direito da página.
5. Adicione as seguintes variaveis:
    - DYNACONF_SIAC__USERNAME: Seu usuário do SIAC.
    - DYNACONF_SIAC__PASSWORD: Sua senha do SIAC.
    - DYNACONF_TELEGRAM__BOT_TOKEN: O token do seu bot do Telegram.
    - DYNACONF_TELEGRAM__CHAT_ID: Seu CHAT ID da conversa do Telegram.

### Local
1. Clone o repositório.
2. copie o arquivo `settings.toml` para `.secrets.toml`.
3. Preencha as variaveis no arquivo `.secrets.toml`. 
4. Execute o comando `docker build -t ansiac .` para criar a imagem.
5. Execute o comando `docker run -v $PWD:/app ansiac` para executar o container.