# Wishlist API

Uma API de lista de desejos construída com FastAPI e PostgreSQL.

## Desenvolvimento Local

### Usando Docker Compose

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/wishlist.git
cd wishlist
```

2. Crie um arquivo `.env` na raiz do projeto:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/wishlist
SECRET_KEY=seu_secret_key
```

3. Inicie os containers:
```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000` e a documentação em `http://localhost:8000/docs`.

### Desenvolvimento Local sem Docker

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente:
```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wishlist
export SECRET_KEY=seu_secret_key
```

3. Inicie o servidor:
```bash
uvicorn app.main:app --reload
```

## Testes

Execute os testes com:
```bash
pytest
```

## Produção

### Kubernetes

1. Configure os secrets (substitua os valores):
```bash
kubectl apply -f k8s/secrets.yaml
```

2. Implante o banco de dados:
```bash
kubectl apply -f k8s/database.yaml
```

3. Implante a API:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### GitHub Actions

O projeto inclui dois workflows:

1. **CI** (.github/workflows/ci.yml):
   - Executa testes
   - Constrói e publica a imagem Docker quando o push é feito na branch main

2. **CD** (.github/workflows/cd.yml):
   - Atualiza o deployment no Kubernetes após um CI bem-sucedido

Para usar o CD, você precisa configurar os seguintes secrets no GitHub:

- `DOCKERHUB_USERNAME`: Seu usuário do Docker Hub
- `DOCKERHUB_TOKEN`: Token de acesso do Docker Hub
- `KUBE_CONFIG`: Arquivo kubeconfig codificado em base64

## Estrutura do Projeto

```
.
├── app/
│   ├── core/
│   │   └── auth.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── models.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── customer.py
│   │   ├── product.py
│   │   └── wishlist.py
│   └── main.py
├── k8s/
│   ├── database.yaml
│   ├── deployment.yaml
│   ├── secrets.yaml
│   └── service.yaml
├── tests/
│   ├── test_auth.py
│   └── test_wishlist.py
├── Dockerfile
├── Dockerfile.dev
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Features

- Customer management (create, read, update, delete)
- Authentication using JWT tokens
- Wishlist management (add/remove products, view wishlist)
- Product validation against existing product database
- High-performance design with proper database indexing
- Comprehensive test suite

## Requirements

- Python 3.8+
- PostgreSQL
- pip

## Setup

1. Clone the repository
2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=postgresql://user:password@localhost/wishlist
SECRET_KEY=your-secret-key-here  # Generate a secure secret key
```

5. Create the database and apply migrations:
```bash
# Create database in PostgreSQL
createdb wishlist

# The tables will be created automatically when you run the application
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## Running Tests

The project includes a comprehensive test suite that covers authentication, customer management, and wishlist functionality. To run the tests:

```bash
pytest
```

To run tests with coverage report:

```bash
pytest --cov=app tests/
```

The tests use an in-memory SQLite database for faster execution and isolation.

## API Documentation

Once the application is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /token` - Get access token

### Customers
- `POST /customers/` - Create new customer
- `GET /customers/me` - Get current customer details
- `PUT /customers/me` - Update current customer
- `DELETE /customers/me` - Delete current customer

### Wishlist
- `GET /wishlist` - Get customer's wishlist
- `POST /wishlist/products/{product_id}` - Add product to wishlist
- `DELETE /wishlist/products/{product_id}` - Remove product from wishlist

## Security

- JWT token-based authentication
- Password hashing using bcrypt
- Email uniqueness validation
- Product existence validation
- Duplicate product prevention in wishlist 