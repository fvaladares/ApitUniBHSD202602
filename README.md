# Template de API RESTful (FastAPI + SQLite) - Projeto A3

Este repositório contém uma API educacional desenvolvida para o **Projeto A3**, organizada em módulos para separar a conexão com o banco, os contratos de dados e as rotas HTTP.

Desenvolvida em Python com **FastAPI** e **SQLite**, a API oferece persistência de dados e documentação automática, servindo como backend para integração com a UC de Usabilidade.

## 🛠 Tecnologias e Pré-requisitos

* **Python 3.12+**
* **uv** (Gerenciador de pacotes e projetos ultrarrápido para Python)
* **FastAPI** (Framework web de alta performance)
* **Uvicorn** (Servidor web ASGI)
* **SQLite** (Banco de dados relacional nativo do Python)

## ⚙️ Como configurar e executar (usando `uv`)

1. Clone este repositório para o seu ambiente local (ou abra no GitHub Codespaces).
2. No terminal, dentro da pasta do projeto, instale o **uv**
```bash
pip install uv
```
3. No terminal, dentro da pasta do projeto, inicialize o ambiente com o **uv** (isso criará o `pyproject.toml` e preparará o ambiente virtual isolado):
   ```bash
   uv init
   ```
4. Adicione as dependências do projeto. O **uv** fará o download e a instalação em frações de segundo:
   ```bash
   uv add fastapi uvicorn
   ```
5. Inicie o servidor local da API utilizando o comando `run` do **uv**:
   ```bash
   uv run uvicorn main:app --reload
   ```
   *(Na primeira execução, o banco de dados será criado automaticamente na mesma pasta).*

6. O servidor estará rodando em: `http://127.0.0.1:8000`

## 📖 Documentação e Testes (Swagger UI)

A API possui documentação interativa gerada automaticamente. Você não precisa de ferramentas externas como Postman ou Insomnia para testar as rotas.

Com o servidor em execução, acesse no navegador:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

## 🚀 Resumo dos Endpoints Disponíveis

A API implementa o CRUD completo. Todos os endpoints estão definidos no arquivo `main.py`:

* **POST `/registros`**: Cria um novo registro no banco (Status `201 Created` ou `400 Bad Request`).
* **GET `/registros`**: Retorna a lista com todos os registros salvos (Status `200 OK`).
* **GET `/registros/{id}`**: Busca os detalhes de um registro específico (Status `200 OK` ou `404 Not Found`).
* **PUT `/registros/{id}`**: Atualiza os dados de um registro existente (Status `200 OK` ou `404 Not Found`).
* **DELETE `/registros/{id}`**: Exclui um registro do banco de dados (Status `200 OK` ou `404 Not Found`).

---

## 🏗️ Organização do projeto

* `database.py`: conexão com o SQLite e criação da tabela inicial.
* `models.py`: contratos de entrada e saída definidos com Pydantic.
* `main.py`: inicialização do FastAPI e endpoints CRUD.
* `nginx/fastapi.conf`: configuração do NGINX como proxy reverso da API.

O módulo `App.py` continua disponível como compatibilidade para inicializações antigas com `App:app`. Para novas execuções, use o comando `uvicorn main:app --reload` descrito acima.

---

## 🌐 Configurando o NGINX (proxy reverso)

Nesta seção, o **NGINX** é colocado na frente da API. O Uvicorn continua rodando a aplicação em uma porta interna (`8000`), e o NGINX recebe as requisições na porta `80` e as repassa para ele. Esse padrão se chama **proxy reverso**.

```
Navegador  ──►  NGINX (porta 80)  ──►  Uvicorn / FastAPI (127.0.0.1:8000)  ──►  banco_a3.db
```

Por que usar? O NGINX lida melhor com muitas conexões simultâneas, permite adicionar HTTPS, servir arquivos estáticos e balancear carga, além de esconder a porta da aplicação.

### Pré-requisitos

* O projeto funcionando conforme a seção "Como configurar e executar".
* Linux (Ubuntu/Debian/Zorin). No Windows, use o **WSL** (Ubuntu) e siga os mesmos passos.
* Também funciona no **GitHub Codespaces** (que é um Ubuntu na nuvem). Neste tutorial usamos `service` em vez de `systemctl`, porque o Codespaces não tem `systemctl`.

### 1. Rodar a API apenas localmente

Dentro da pasta do projeto (é de lá que o `banco_a3.db` é criado e lido), instale as dependências definidas no `pyproject.toml` e suba o Uvicorn em `127.0.0.1`, para que **somente o NGINX** consiga acessá-lo:

```bash
uv sync
uv run uvicorn main:app --host 127.0.0.1 --port 8000 --proxy-headers
```

Teste direto, ainda sem o NGINX: http://127.0.0.1:8000/docs

> Deixe este terminal aberto. Os próximos comandos devem ser executados em **outro terminal**.

### 2. Instalar o NGINX

```bash
sudo apt update
sudo apt install nginx -y
```

### 3. Criar a configuração

O arquivo `nginx/fastapi.conf` deste repositório já contém a configuração:

```nginx
server {
    listen 80;
    server_name localhost;

    # Repassa todas as requisições para o Uvicorn (FastAPI)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

O que cada parte faz:

| Linha | Função |
|---|---|
| `listen 80` | O NGINX escuta na porta 80 (HTTP) |
| `server_name` | Nome do servidor (`localhost` para testes) |
| `proxy_pass` | Endereço da API para onde as requisições são enviadas |
| `proxy_set_header ...` | Repassa para a API o host e o IP real do cliente |

### 4. Ativar a configuração

Na pasta do projeto, execute:

```bash
sudo cp nginx/fastapi.conf /etc/nginx/sites-available/fastapi
sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
```

Verifique se a sintaxe está correta e reinicie o NGINX:

```bash
sudo nginx -t
sudo service nginx restart
```

### 5. Testar

Com o Uvicorn rodando, acesse **sem informar a porta 8000**:

👉 **http://localhost/docs**

Também é possível testar o CRUD pelo terminal, passando pelo NGINX:

```bash
# criar um registro
curl -X POST http://localhost/registros \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Teste via NGINX", "descricao": "Funcionou!"}'

# listar os registros
curl http://localhost/registros
```

Se o registro for criado e aparecer na listagem, o NGINX está repassando as requisições corretamente.

> **No GitHub Codespaces:** o `localhost` acima só funciona dentro do terminal do Codespaces (o `curl`). Para abrir no navegador, vá na aba **Portas** (ao lado de Terminal), localize a porta **80**, clique no ícone de globo para abrir no navegador e acrescente `/docs` no final do endereço.

### Problemas comuns

| Problema | Causa provável / solução |
|---|---|
| **`[Errno 98] ... address already in use` na porta 8000** | Já existe um processo usando a porta. Confira com `sudo ss -ltnp 'sport = :8000'`. Se for uma instância da API que você já iniciou, use-a em vez de iniciar outra; para pará-la, volte ao terminal dela e pressione `Ctrl+C`. Só encerre outro processo depois de confirmar que ele pode ser parado. |
| **502 Bad Gateway** | O Uvicorn não está rodando ou está em outra porta. Confira o `proxy_pass`. |
| Aparece a página "Welcome to nginx" | O site `default` ainda está ativo. Remova `/etc/nginx/sites-enabled/default` e reinicie. |
| `nginx -t` mostra erro | Erro de sintaxe no `.conf` (geralmente falta um `;` ou `}`). |
| Porta 80 ocupada | Veja quem está usando: `sudo ss -tulpn \| grep :80` |

Para investigar erros, acompanhe o log:

```bash
sudo tail -f /var/log/nginx/error.log
```

### Comandos úteis

```bash
sudo service nginx status      # ver se está rodando
sudo service nginx reload      # recarregar a config sem derrubar conexões
sudo service nginx stop        # parar o NGINX
```

## 👥 Equipe

* Caio
* Raphel
