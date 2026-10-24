# TaskTracker

## Descrição Funcional
O TaskTracker é um sistema de gestão de tarefas desenvolvido para centralizar e simplificar a organização diária. Permite o registo, visualização, edição, conclusão, reabertura, exclusão e filtragem de atividades, operando através de uma interface de linha de comandos. Os dados são guardados em um ficheiro `tarefas.json`.

## Tecnologias Utilizadas
* Python 3.11
* Git e GitHub
* Docker e Docker Compose

## Estrutura do Repositório
```text
tasktracker-projeto/
├── .gitignore
├── docs/
│   └── planejamento_logico.pdf   # Planejamento da Fase 1
├── src/
│   └── main.py                   # Código Python da Fase 2
├── Dockerfile                    # Receita da imagem (Fase 3)
├── docker-compose.yml            # Orquestração interativa (Fase 3)
└── README.md
```

## Como Executar Localmente (sem Docker)
1. Clone este repositório para a sua máquina local.
2. Abra o terminal e navegue até à pasta raiz do projeto.
3. Execute o comando:

```bash
python src/main.py
```

## Como Executar com Docker

**Pré-requisito:** Docker instalado e em execução ([instruções](https://docs.docker.com/get-docker/)).

### 1. Como construir a imagem
```bash
docker build -t tasktracker .
```

### 2. Como rodar o container em modo isolado
```bash
docker run -it --rm -v tasktracker-data:/data tasktracker
```
* `-it` mantém o terminal interativo (necessário porque o programa usa `input()`).
* `-v tasktracker-data:/data` guarda as tarefas em um volume, para não se perderem ao fechar o container.

### 3. Como rodar via orquestração (Recomendado)
```bash
docker compose run --rm tasktracker
```
O `docker-compose.yml` já configura `stdin_open: true`, `tty: true` e o volume de dados. Não é preciso passar nenhuma opção extra.

## Persistência dos Dados
As tarefas ficam no volume Docker `tasktracker-data`. Para apagar todos os dados guardados:

```bash
docker volume rm tasktracker-data
```

## Autor
[Seu Nome Completo] - [Curso] - [Polo]
