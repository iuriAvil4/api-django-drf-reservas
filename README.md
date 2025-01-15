# Descrição do projeto.

Projeto desenvolvido utilizando Django e Django Rest Framework. A API fornece endpoints para gerenciar a criação e reservas de salas.

Este projeto foi pensado para consolidar conceitos que eu já conhecia e explorar novos aprendizados, especialmente através da documentação oficial do DRF.

A API oferece funcionalidades como:

🔍 Pesquisa
🔀 Ordenação
📋 Paginação

Além disso, o projeto inclui:

- Testes unitários para validar todos os endpoints e garantir confiabilidade.
- Documentação interativa criada com Swagger, facilitando o uso e entendimento dos endpoints.
## Base URL

`/api/`

## Endpoints Disponíveis

- **Reservas**
  - `/reservas/`
    - `GET`: Obter lista de todas das reservas.
  - `/data/reservas/`
    - `GET`: Obter detalhes de uma reserva por ID.
    - `POST`: Criar uma nova reserva.
    - `PUT`: Atualizar detalhes de uma reserva existente.
    - `DELETE`: Excluir uma reserva existente.
    
- **Salas**
  - `/salas/`
    - `GET`: Obter lista de todas as salas.
  - `/data/salas/`
    - `GET`: Obter detalhes de uma sala por ID.
    - `POST`: Criar uma nova sala.
    - `PUT`: Atualizar detalhes de uma sala existente.
    - `DELETE`: Excluir uma sala existente.

## Parâmetros de Requisição

- **GET**
  - `reservas`: ID da reserva desejada.
  - `salas`: ID da sala desejada.

## Exemplos

### Obter Lista de Reservas por ID

```http
GET /api/data/reservas/?id_reserva=4
```

### Obter Lista de Reservas utilizando Paginação e Pesquisa personalizada.
```http
GET /api/reservas/?page=1&page_size=10&reservado_por=Iuri%20Avila
```

# Instalação e Configuração

Siga estas instruções para configurar e executar o projeto em seu ambiente local.

## Pré-requisitos

Certifique-se de ter o Python e o Django instalados em seu sistema. Você também pode usar um ambiente virtual para isolar as dependências do projeto. </br>

### Clone o repositório

   1. Clone este repositório para o seu ambiente local usando o seguinte comando:

   ```bash
   git clone https://github.com/iuriAvil4/api-django-drf-reservasdesala
   ```
 ### Ativar o Ambiente Virtual (venv)

2. Antes de executar os comandos relacionados ao projeto Django, ative o ambiente virtual `venv`. Dependendo do seu sistema operacional e do método de criação do ambiente virtual, os comandos podem variar. 

#### Windows

```bash
.\venv\Scripts\activate
````

   ### Instale as Dependências

3. Navegue até o diretório do projeto e instale as dependências listadas no arquivo `requirements.txt` usando o pip:

```bash
cd api-django-drf
pip install -r requirements.txt
```
### Migrar Banco de Dados

4. Execute as migrações para criar as tabelas do banco de dados:

```bash
python manage.py migrate
```
### Executar o Servidor de Desenvolvimento

5. Para iniciar o servidor de desenvolvimento Django, utilize o seguinte comando:

```bash
python manage.py runserver
