# TaskTracker

## Descrição Funcional

O **TaskTracker** é um sistema de gerenciamento de tarefas desenvolvido para centralizar e simplificar a organização diária. A aplicação permite registrar, visualizar, editar, concluir, reabrir, excluir e filtrar tarefas por meio de uma interface de linha de comando (CLI).

Os dados são armazenados localmente no arquivo `tarefas.json`.

## Tecnologias Utilizadas

- **Python 3.11** — desenvolvimento da aplicação.
- **Git e GitHub** — controle de versão e hospedagem do repositório.
- **Docker** — criação e execução de containers.
- **Docker Compose** — orquestração da execução da aplicação.

## Estrutura do Repositório

```text
tasktracker-projeto/
├── .gitignore
├── docs/
│   └── Planejamento Lógico TaskTracker.pdf
├── src/
│   └── main.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

- `docs/`: documentação e planejamento lógico do projeto, desenvolvido na Fase 1.
- `src/`: código-fonte da aplicação, desenvolvido na Fase 2.
- `Dockerfile`: instruções para construir a imagem Docker, desenvolvido na Fase 3.
- `docker-compose.yml`: configuração para orquestrar a execução da aplicação e mapear volumes, desenvolvido na Fase 3.
- `.gitignore`: arquivos e diretórios ignorados pelo Git.

## Como Executar Localmente (sem Docker)

**Pré-requisito:** Python 3.11 instalado.

1. Clone este repositório para sua máquina.
2. Abra o terminal e navegue até a pasta raiz do projeto.
3. Execute o comando:

   ```bash
   python src/main.py
   ```

## Como Executar com Docker

**Pré-requisito:** Docker instalado e em execução.

### 1. Construir a imagem

Na pasta raiz do projeto, execute:

```bash
docker build -t tasktracker-app .
```

### 2. Executar o container em modo isolado

Execute o comando:

```bash
docker run -it tasktracker-app
```

**Observação:** nesse modo, a pasta local do projeto não é mapeada para o container. Portanto, os arquivos criados dentro dele não são automaticamente persistidos na máquina host.

### 3. Executar com Docker Compose (recomendado)

Execute o comando:

```bash
docker compose run app
```

O arquivo `docker-compose.yml` configura a execução interativa por meio das opções `stdin_open: true` e `tty: true`, além do mapeamento de volume `./src:/app/src`.

## Persistência dos Dados

Ao executar a aplicação com o comando `docker compose run app`, o Docker Compose utiliza um **bind mount** para conectar o diretório `src/` da máquina local ao diretório `/app/src` do container.

Esse mapeamento permite que as alterações e os arquivos gravados nesse diretório sejam refletidos no ambiente local. Assim, se o arquivo `tarefas.json` for salvo em `src/`, os dados permanecerão disponíveis na máquina host mesmo após o encerramento do container.

> **Importante:** a persistência depende de o arquivo `tarefas.json` ser gravado no diretório mapeado. Se ele for salvo em outro diretório do container, o volume configurado não garantirá sua persistência.

## Autor

**Heinrich Hoffman Pereira da Silva**  
Curso: Ciência da Computação  
Polo: Asa Norte