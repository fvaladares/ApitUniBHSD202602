# Template de API RESTful (FastAPI + SQLite) - Monolito (Projeto A3)

> 💡 **AVISO IMPORTANTE:** Este repositório contém a estrutura base desenvolvida para o **Projeto A3** em formato **monolítico**. Todo o ciclo de vida da aplicação — conexão com o banco, estruturação de dados e roteamento — está concentrado em um único arquivo (`main.py`). Ao final deste documento, há um guia prático de como evoluir esta base para o **Projeto A4**, adotando uma arquitetura em múltiplas camadas.

Esta é uma API educacional desenvolvida em Python com o framework **FastAPI** e banco de dados relacional **SQLite**. Ela atende aos requisitos iniciais de persistência de dados e documentação automática, servindo como backend para integração com a UC de Usabilidade.

## 🛠 Tecnologias e Pré-requisitos

* **Python 3.8+**
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

## 🏗️ Guia de Evolução: Do Monolito (A3) para Múltiplas Camadas (A4)

Manter todo o código em um único arquivo (`main.py`) é excelente para o aprendizado inicial e testes rápidos, mas torna a manutenção difícil conforme o sistema cresce. 

Para o **Projeto A4**, o grupo deverá refatorar este monolito em uma **arquitetura de múltiplas camadas**. Siga estes passos para organizar a casa:

1. **Isole o Banco de Dados (`database.py`)**
   * Crie um novo arquivo chamado `database.py`.
   * Mova para ele toda a lógica de conexão com o SQLite (a criação da `engine`, do `cursor` ou a configuração do ORM que estiverem usando) e a função que cria as tabelas iniciais.
   * *Analogia:* Este será o almoxarifado exclusivo do seu sistema.

2. **Separe os Contratos de Dados (`models.py`)**
   * Crie um arquivo `models.py`.
   * Recorte do seu `main.py` todas as classes que herdam de `BaseModel` do Pydantic (como `RegistroCreate`, `RegistroResponse`, etc.) e cole neste novo arquivo.
   * *Analogia:* Este arquivo será o setor de controle de qualidade, ditando o que pode entrar ou sair do sistema.

3. **Limpe as Rotas (`main.py`)**
   * O seu `main.py` agora deve ficar muito mais limpo.
   * Mantenha apenas a inicialização do FastAPI (`app = FastAPI()`) e as funções de rota (os `@app.get`, `@app.post`, etc.).
   * No topo do `main.py`, importe os módulos que você acabou de criar:
     ```python
     from database import conectar_banco, criar_tabelas
     from models import RegistroCreate, RegistroResponse
     ```

Após essa divisão, seu código estará preparado para escalar, integrando facilmente novas funcionalidades de segurança, como um proxy reverso Nginx, de forma totalmente estruturada e profissional.

## Atividade complementar — Sistemas Distribuídos com Nginx

Nesta atividade, o projeto foi organizado em pacotes e recebeu o Nginx como intermediário entre o cliente e a API FastAPI.

### 1. Organização dos arquivos

O código foi separado por responsabilidade:

- `app/main.py`: inicialização da API.
- `app/database.py`: conexão com o banco e criação das tabelas.
- `app/models.py`: modelos de dados.
- `app/routes/registros.py`: rotas de cadastro, consulta, atualização e exclusão.
- `nginx/nginx.conf`: configuração do Nginx.

### 2. Instalação do Nginx

No GitHub Codespaces, foi instalado o Nginx utilizando os comandos `sudo apt-get update` e `sudo apt-get install -y nginx`.

### 3. Configuração do Nginx

O Nginx foi configurado para receber requisições na porta 8080 e encaminhá-las para duas instâncias da API FastAPI, nas portas 8000 e 8001.

Foram implementadas as seguintes funcionalidades:

- **Proxy reverso:** recebe as requisições dos clientes e encaminha para a API.
- **Balanceamento de carga:** distribui as requisições entre as duas instâncias.
- **Cache HTTP:** armazena temporariamente respostas de consultas GET.
- **Limitação de requisições:** configura um limite de 5 requisições por segundo, permitindo pequenos picos de acesso.

### 4. Como executar

Para iniciar a primeira instância da API, utilize `uv run uvicorn app.main:app --reload`.

Em outro terminal, inicie a segunda instância com `uv run uvicorn app.main:app --host 127.0.0.1 --port 8001`.

Depois, teste a configuração do Nginx com `sudo nginx -t -c "$PWD/nginx/nginx.conf"` e inicie-o com `sudo nginx -c "$PWD/nginx/nginx.conf"`.

A documentação da API pode ser acessada pelo endereço `http://localhost:8080/docs`.

### 5. Testes realizados

Os testes foram realizados com sucesso no GitHub Codespaces:

- A documentação da API foi acessada através do Nginx.
- Na primeira consulta, o cabeçalho `X-Cache-Status` apresentou `MISS`, indicando que a resposta ainda não estava armazenada.
- Na segunda consulta, apresentou `HIT`, comprovando o funcionamento do cache.
- Duas requisições POST foram encaminhadas para instâncias diferentes: uma na porta 8001 e outra na porta 8000, comprovando o balanceamento de carga.

