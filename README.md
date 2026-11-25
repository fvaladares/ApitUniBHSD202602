# Template de API RESTful (FastAPI + SQLite) - Monolito (Projeto A3)

> 💡 **AVISO IMPORTANTE:** Este repositório contém a estrutura base desenvolvida para o **Projeto A3** em formato **monolítico**. Todo o ciclo de vida da aplicação — conexão com o banco, estruturação de dados e roteamento — está concentrado em um único arquivo (`App.py`). Ao final deste documento, há um guia prático de como evoluir esta base para o **Projeto A4**, adotando uma arquitetura em múltiplas camadas.

Esta é uma API educacional desenvolvida em Python com o framework **FastAPI** e banco de dados relacional **SQLite**. Ela atende aos requisitos iniciais de persistência de dados e documentação automática, servindo como backend para integração com a UC de Usabilidade.

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
3. Instale as dependências do projeto:
   ```bash
   uv sync
   ```
4. Inicie o servidor local da API utilizando o comando `run` do **uv**:
   ```bash
   uv run uvicorn App:app --host 0.0.0.0 --port 8000
   ```
   *(Na primeira execução, o banco de dados será criado automaticamente na mesma pasta).*

5. O servidor estará rodando em: `http://127.0.0.1:8000`

## 📖 Documentação e Testes (Swagger UI)

A API possui documentação interativa gerada automaticamente. Você não precisa de ferramentas externas como Postman ou Insomnia para testar as rotas.

Com o servidor em execução, acesse no navegador:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

## 🚀 Resumo dos Endpoints Disponíveis

A API implementa o CRUD completo. Todos os endpoints estão definidos no arquivo `App.py`:

* **POST `/registros`**: Cria um novo registro no banco (Status `201 Created` ou `400 Bad Request`).
* **GET `/registros`**: Retorna a lista com todos os registros salvos (Status `200 OK`).
* **GET `/registros/{id}`**: Busca os detalhes de um registro específico (Status `200 OK` ou `404 Not Found`).
* **PUT `/registros/{id}`**: Atualiza os dados de um registro existente (Status `200 OK` ou `404 Not Found`).
* **DELETE `/registros/{id}`**: Exclui um registro do banco de dados (Status `200 OK` ou `404 Not Found`).

---

## 🏗️ Guia de Evolução: Do Monolito (A3) para Múltiplas Camadas (A4)

Manter todo o código em um único arquivo (`App.py`) é excelente para o aprendizado inicial e testes rápidos, mas torna a manutenção difícil conforme o sistema cresce.

Para o **Projeto A4**, o grupo deverá refatorar este monolito em uma **arquitetura de múltiplas camadas**. Siga estes passos para organizar a casa:

1. **Isole o Banco de Dados (`database.py`)**
   * Crie um novo arquivo chamado `database.py`.
   * Mova para ele toda a lógica de conexão com o SQLite (a criação da `engine`, do `cursor` ou a configuração do ORM que estiverem usando) e a função que cria as tabelas iniciais.
   * *Analogia:* Este será o almoxarifado exclusivo do seu sistema.

2. **Separe os Contratos de Dados (`models.py`)**
   * Crie um arquivo `models.py`.
   * Recorte do seu `App.py` todas as classes que herdam de `BaseModel` do Pydantic (como `RegistroCreate`, `RegistroResponse`, etc.) e cole neste novo arquivo.
   * *Analogia:* Este arquivo será o setor de controle de qualidade, ditando o que pode entrar ou sair do sistema.

3. **Limpe as Rotas (`App.py`)**
   * O seu `App.py` agora deve ficar muito mais limpo.
   * Mantenha apenas a inicialização do FastAPI (`app = FastAPI()`) e as funções de rota (os `@app.get`, `@app.post`, etc.).
   * No topo do `App.py`, importe os módulos que você acabou de criar:
     ```python
     from database import conectar_banco, criar_tabelas
     from models import RegistroCreate, RegistroResponse
     ```

Após essa divisão, seu código estará preparado para escalar, integrando facilmente novas funcionalidades de segurança, como um proxy reverso Nginx, de forma totalmente estruturada e profissional.

---

## Observabilidade da API RESTful

Esta atividade tem como objetivo implementar mecanismos de
observabilidade na API RESTful, permitindo acompanhar seu
desempenho, identificar erros e monitorar as requisições HTTP.

### Tecnologias utilizadas

- FastAPI: desenvolvimento da API RESTful.
- SQLite: persistência dos dados.
- Loguru: registro de logs da aplicação.
- Prometheus: coleta e armazenamento de métricas.
- Grafana 11.6.0: visualização dos indicadores.
- Docker Compose: gerenciamento dos serviços de monitoramento.
- Prometheus FastAPI Instrumentator: instrumentação da API.

### Estrutura dos arquivos

- App.py: aplicação FastAPI instrumentada.
- docker-compose.yml: configuração dos serviços.
- prometheus.yml: configuração da coleta de métricas.
- dashboard-observabilidade.json: dashboard exportado do Grafana.
- pyproject.toml: dependências do projeto.
- uv.lock: controle das versões das dependências.
- .gitignore: exclusão de arquivos locais e temporários.

### Executando a aplicação

Instale as dependências:

```bash
uv sync
```

Inicie a API:

```bash
uv run uvicorn App:app --host 0.0.0.0 --port 8000
```

Em outro terminal, inicie os serviços de monitoramento:

```bash
docker compose up -d
```

Verifique os containers:

```bash
docker compose ps
```

### Endereços dos serviços

| Serviço | Endereço |
|---|---|
| API FastAPI | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Métricas da API | http://localhost:8000/metrics |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

No GitHub Codespaces, utilize a aba Ports para acessar
os serviços pelo navegador.

### Configuração do Grafana

1. Acesse o Grafana pela porta 3000.
2. Adicione uma fonte de dados do tipo Prometheus.
3. Utilize a URL http://prometheus:9090.
4. Clique em Save & test.
5. Acesse a opção de importação de dashboards.
6. Importe o arquivo dashboard-observabilidade.json.
7. Selecione a fonte de dados Prometheus configurada.

### Indicadores de observabilidade

#### Vazão de requisições (Throughput)

Quantidade média de requisições HTTP por segundo
recebidas pela API.

```promql
sum(rate(http_requests_total{job="fastapi"}[1m]))
```

#### Taxa de erros HTTP (Error Rate)

Percentual de requisições que retornaram erros
HTTP das classes 4xx ou 5xx.

```promql
100 * (
  sum(rate(http_requests_total{job="fastapi",status=~"4xx|5xx"}[1m]))
  /
  sum(rate(http_requests_total{job="fastapi"}[1m]))
)
```

#### Latência média (Latency)

Tempo médio de resposta das requisições HTTP,
expresso em milissegundos.

```promql
1000 * (
  sum(rate(http_request_duration_seconds_sum{job="fastapi"}[5m]))
  /
  sum(rate(http_request_duration_seconds_count{job="fastapi"}[5m]))
)
```

### Registro de logs

A aplicação utiliza Loguru para registrar informações
sobre as requisições HTTP, incluindo:

- Data e horário.
- Método HTTP.
- Rota acessada.
- Código de status HTTP.
- Latência da requisição.

### Testes de observabilidade

Para gerar requisições bem-sucedidas:

```bash
for i in {1..100}; do
  curl -s http://127.0.0.1:8000/registros > /dev/null
  sleep 0.2
done
```

Para gerar erros HTTP 404 intencionalmente:

```bash
for i in {1..100}; do
  curl -s http://127.0.0.1:8000/pagina-inexistente > /dev/null
  sleep 0.2
done
```

### Resultados obtidos

Durante os testes realizados, foram observados:

- Vazão máxima aproximada de 1,8 requisição por segundo.
- Taxa de erros de 100% durante os testes de rotas inválidas.
- Taxa de erros de 0% durante os testes de sucesso posteriores.
- Latência média entre aproximadamente 1,2 e 2,3 ms.

Os três indicadores foram configurados, testados e
visualizados no dashboard do Grafana.

Na ausência de requisições, os indicadores de latência
e taxa de erros podem apresentar intervalos sem dados.

### Conclusão

A implementação da observabilidade permite acompanhar
o comportamento da API, identificar falhas e analisar
seu desempenho. A integração entre FastAPI, Loguru,
Prometheus e Grafana contribui para o monitoramento
e a manutenção da aplicação.
