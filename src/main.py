
import json
import os
import tempfile
from datetime import datetime, date

# ==========================================
# TaskTracker - Sistema de Gerenciamento
# Compatível com VS Code e Google Colab
# ==========================================

try:
    PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Google Colab / Jupyter
    PASTA_SCRIPT = os.getcwd()

# Permite configurar uma pasta específica para os dados.
# Útil para usar o Google Drive no Colab.
BASE_DIR = os.environ.get("TASKTRACKER_DIR", PASTA_SCRIPT)
BASE_DIR = os.path.abspath(BASE_DIR)

os.makedirs(BASE_DIR, exist_ok=True)

ARQUIVO_DADOS = os.path.join(BASE_DIR, "tarefas.json")

PRIORIDADES = ["Alta", "Média", "Baixa"]
STATUS_VALIDOS = ["Pendente", "Concluída"]

tarefas = []
id_contador = 1


# ==========================================
# 1. VALIDAÇÃO E NORMALIZAÇÃO
# ==========================================

def normalizar_prioridade(valor):
    """Padroniza prioridades, aceitando variações de acentuação."""
    if not isinstance(valor, str):
        return None

    prioridades = {
        "alta": "Alta",
        "média": "Média",
        "media": "Média",
        "baixa": "Baixa"
    }

    return prioridades.get(valor.strip().casefold())


def normalizar_status(valor):
    """Padroniza os status aceitos pelo sistema."""
    if not isinstance(valor, str):
        return None

    status = {
        "pendente": "Pendente",
        "concluída": "Concluída",
        "concluida": "Concluída"
    }

    return status.get(valor.strip().casefold())


def validar_data(valor):
    """
    Aceita DD/MM/AAAA, string vazia ou 'Não informada'.
    Retorna a data padronizada ou None se inválida.
    """
    if not isinstance(valor, str):
        return None

    valor = valor.strip()

    if valor.casefold() == "não informada" or valor == "":
        return "Não informada"

    try:
        data_validada = datetime.strptime(
            valor, "%d/%m/%Y"
        ).date()

        # Exige exatamente o formato DD/MM/AAAA.
        if data_validada.strftime("%d/%m/%Y") != valor:
            return None

        return data_validada.strftime("%d/%m/%Y")

    except ValueError:
        return None


def validar_tarefa(tarefa):
    """Valida e padroniza um registro carregado do JSON."""
    if not isinstance(tarefa, dict):
        raise ValueError("Uma tarefa não é um objeto válido.")

    campos_obrigatorios = [
        "id", "titulo", "prioridade", "status"
    ]

    for campo in campos_obrigatorios:
        if campo not in tarefa:
            raise ValueError(f"Campo ausente: {campo}")

    identificador = tarefa["id"]

    # bool também é considerado int em Python.
    if type(identificador) is not int or identificador <= 0:
        raise ValueError("ID deve ser um inteiro positivo.")

    titulo = tarefa["titulo"]

    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError(
            f"Título inválido na tarefa {identificador}."
        )

    prioridade = normalizar_prioridade(tarefa["prioridade"])
    status = normalizar_status(tarefa["status"])

    if prioridade is None:
        raise ValueError(
            f"Prioridade inválida na tarefa {identificador}."
        )

    if status is None:
        raise ValueError(
            f"Status inválido na tarefa {identificador}."
        )

    descricao = tarefa.get("descricao", "")

    if not isinstance(descricao, str):
        raise ValueError(
            f"Descrição inválida na tarefa {identificador}."
        )

    data_limite = validar_data(tarefa.get("data_limite", ""))

    if data_limite is None:
        raise ValueError(
            f"Data inválida na tarefa {identificador}."
        )

    return {
        "id": identificador,
        "titulo": titulo.strip(),
        "descricao": descricao.strip(),
        "prioridade": prioridade,
        "data_limite": data_limite,
        "status": status
    }


# ==========================================
# 2. PERSISTÊNCIA EM JSON
# ==========================================

def carregar_dados():
    """Carrega e valida os dados antes de disponibilizá-los."""
    global tarefas, id_contador

    if not os.path.exists(ARQUIVO_DADOS):
        tarefas = []
        id_contador = 1
        return

    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, list):
            raise ValueError(
                "O arquivo deve conter uma lista de tarefas."
            )

        tarefas_carregadas = []
        ids_encontrados = set()

        for registro in dados:
            tarefa = validar_tarefa(registro)

            if tarefa["id"] in ids_encontrados:
                raise ValueError(
                    f"ID duplicado: {tarefa['id']}."
                )

            ids_encontrados.add(tarefa["id"])
            tarefas_carregadas.append(tarefa)

        # Atualiza o estado somente após validar tudo.
        tarefas = tarefas_carregadas
        id_contador = max(ids_encontrados, default=0) + 1

    except (OSError, json.JSONDecodeError, ValueError, TypeError) as erro:
        raise RuntimeError(
            f"Não foi possível carregar {ARQUIVO_DADOS}: {erro}. "
            "Corrija ou recupere o arquivo antes de continuar."
        ) from erro


def salvar_dados():
    """Salva o JSON temporariamente e substitui o arquivo original."""
    caminho_temporario = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=BASE_DIR,
            prefix="tarefas_",
            suffix=".tmp",
            delete=False
        ) as arquivo:
            caminho_temporario = arquivo.name

            json.dump(
                tarefas,
                arquivo,
                ensure_ascii=False,
                indent=4
            )

            arquivo.write("\n")
            arquivo.flush()
            os.fsync(arquivo.fileno())

        # O temporário fica no mesmo diretório do destino.
        os.replace(caminho_temporario, ARQUIVO_DADOS)

    except (OSError, TypeError, ValueError) as erro:
        print(f"\nErro ao salvar os dados: {erro}")

        if (
            caminho_temporario
            and os.path.exists(caminho_temporario)
        ):
            try:
                os.remove(caminho_temporario)
            except OSError:
                pass

        raise RuntimeError(
            "A alteração não pôde ser salva no arquivo JSON."
        ) from erro


# ==========================================
# 3. EXIBIÇÃO E RELATÓRIOS
# ==========================================

def imprimir_tarefa(t):
    """Exibe os detalhes de uma tarefa."""
    print("-" * 45)
    print(f"ID: {t['id']}")
    print(f"Título: {t['titulo']}")
    print(f"Descrição: {t['descricao'] or 'Não informada'}")
    print(f"Prioridade: {t['prioridade']}")
    print(f"Data limite: {t['data_limite']}")
    print(f"Status: {t['status']}")


def tarefa_vencida(t, hoje=None):
    """Verifica se uma tarefa pendente já passou do prazo."""
    if hoje is None:
        hoje = date.today()

    if t["status"] != "Pendente":
        return False

    if t["data_limite"] == "Não informada":
        return False

    prazo = datetime.strptime(
        t["data_limite"], "%d/%m/%Y"
    ).date()

    return prazo < hoje


def exibir_totalizadores(lista_alvo=None):
    """Apresenta estatísticas da lista completa ou filtrada."""
    if lista_alvo is None:
        lista_alvo = tarefas

    total = len(lista_alvo)

    pendentes = sum(
        t["status"] == "Pendente" for t in lista_alvo
    )

    concluidas = sum(
        t["status"] == "Concluída" for t in lista_alvo
    )

    vencidas = sum(
        tarefa_vencida(t) for t in lista_alvo
    )

    alta = sum(
        t["prioridade"] == "Alta" for t in lista_alvo
    )

    percentual = concluidas / total * 100 if total else 0

    print("\n" + "=" * 45)
    print("RESUMO DAS TAREFAS")
    print("=" * 45)
    print(f"Total: {total}")
    print(f"Pendentes: {pendentes}")
    print(f"Concluídas: {concluidas}")
    print(f"Vencidas: {vencidas}")
    print(f"Prioridade alta: {alta}")
    print(f"Conclusão: {percentual:.1f}%")
    print("=" * 45)


def chave_ordenacao(t):
    """Ordena por prioridade e, depois, pela data limite."""
    ordem_prioridade = {
        "Alta": 0,
        "Média": 1,
        "Baixa": 2
    }

    if t["data_limite"] == "Não informada":
        prazo = date.max
    else:
        prazo = datetime.strptime(
            t["data_limite"], "%d/%m/%Y"
        ).date()

    return ordem_prioridade[t["prioridade"]], prazo


def visualizar_tarefas():
    print("\n--- Lista de Tarefas ---")

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        exibir_totalizadores()
        return

    for t in sorted(tarefas, key=chave_ordenacao):
        imprimir_tarefa(t)

    exibir_totalizadores()


# ==========================================
# 4. CADASTRO
# ==========================================

def cadastrar_tarefa():
    global id_contador

    print("\n--- Cadastrar Nova Tarefa ---")

    while True:
        titulo = input("Título da tarefa: ").strip()

        if titulo:
            break

        print("Erro: o título não pode ficar em branco.")

    descricao = input("Descrição (opcional): ").strip()

    while True:
        entrada = input(
            "Prioridade (Alta / Média / Baixa): "
        )

        prioridade = normalizar_prioridade(entrada)

        if prioridade:
            break

        print("Erro: escolha Alta, Média ou Baixa.")

    while True:
        entrada = input(
            "Data limite (DD/MM/AAAA ou Enter para pular): "
        ).strip()

        data_limite = validar_data(entrada)

        if data_limite is not None:
            break

        print("Data inválida. Use o formato DD/MM/AAAA.")

    nova_tarefa = {
        "id": id_contador,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_limite": data_limite,
        "status": "Pendente"
    }

    tarefas.append(nova_tarefa)

    try:
        salvar_dados()
    except RuntimeError:
        tarefas.pop()
        return

    id_contador += 1
    print("\nSucesso: tarefa cadastrada!")


# ==========================================
# 5. LOCALIZAÇÃO E STATUS
# ==========================================

def buscar_por_id(identificador):
    """Retorna uma tarefa pelo ID ou None se não existir."""
    return next(
        (t for t in tarefas if t["id"] == identificador),
        None
    )


def solicitar_id(mensagem):
    """Solicita e valida um ID."""
    try:
        identificador = int(input(mensagem).strip())

        if identificador <= 0:
            raise ValueError

        return identificador

    except ValueError:
        print("Erro: informe um ID inteiro positivo.")
        return None


def alterar_status(novo_status):
    if not tarefas:
        print("\nNenhuma tarefa cadastrada.")
        return

    identificador = solicitar_id("Digite o ID da tarefa: ")

    if identificador is None:
        return

    tarefa = buscar_por_id(identificador)

    if tarefa is None:
        print("Erro: tarefa não encontrada.")
        return

    status_anterior = tarefa["status"]

    if status_anterior == novo_status:
        print(f"A tarefa já está com status '{novo_status}'.")
        return

    tarefa["status"] = novo_status

    try:
        salvar_dados()
    except RuntimeError:
        tarefa["status"] = status_anterior
        return

    print(f"Tarefa atualizada para '{novo_status}'!")


def concluir_tarefa():
    print("\n--- Concluir Tarefa ---")
    alterar_status("Concluída")


def reabrir_tarefa():
    print("\n--- Reabrir Tarefa ---")
    alterar_status("Pendente")


# ==========================================
# 6. EDIÇÃO
# ==========================================

def editar_tarefa():
    print("\n--- Editar Tarefa ---")

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    identificador = solicitar_id(
        "Digite o ID da tarefa que deseja editar: "
    )

    if identificador is None:
        return

    tarefa = buscar_por_id(identificador)

    if tarefa is None:
        print("Erro: tarefa não encontrada.")
        return

    # Cópias para evitar alterações parciais.
    original = tarefa.copy()
    editada = tarefa.copy()

    print("\nPressione Enter para manter o valor atual.")
    print("Digite /limpar para limpar campos opcionais.")

    titulo = input(
        f"Título [{editada['titulo']}]: "
    ).strip()

    if titulo:
        editada["titulo"] = titulo

    descricao = input(
        f"Descrição [{editada['descricao']}]: "
    ).strip()

    if descricao.casefold() == "/limpar":
        editada["descricao"] = ""
    elif descricao:
        editada["descricao"] = descricao

    while True:
        entrada = input(
            f"Prioridade [{editada['prioridade']}]: "
        ).strip()

        if not entrada:
            break

        prioridade = normalizar_prioridade(entrada)

        if prioridade:
            editada["prioridade"] = prioridade
            break

        print(
            "Prioridade inválida. Escolha Alta, Média ou Baixa."
        )

    while True:
        entrada = input(
            f"Data limite [{editada['data_limite']}]: "
        ).strip()

        if not entrada:
            break

        if entrada.casefold() == "/limpar":
            editada["data_limite"] = "Não informada"
            break

        data_limite = validar_data(entrada)

        if data_limite is not None:
            editada["data_limite"] = data_limite
            break

        print("Data inválida. Use DD/MM/AAAA ou /limpar.")

    if editada == original:
        print("Nenhuma alteração realizada.")
        return

    tarefa.update(editada)

    try:
        salvar_dados()
    except RuntimeError:
        tarefa.update(original)
        return

    print("Sucesso: tarefa atualizada!")


# ==========================================
# 7. EXCLUSÃO
# ==========================================

def excluir_tarefa():
    print("\n--- Excluir Tarefa ---")

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    identificador = solicitar_id(
        "Digite o ID da tarefa que deseja excluir: "
    )

    if identificador is None:
        return

    tarefa = buscar_por_id(identificador)

    if tarefa is None:
        print("Erro: tarefa não encontrada.")
        return

    imprimir_tarefa(tarefa)

    confirmacao = input(
        "\nConfirma a exclusão? (s/n): "
    ).strip().casefold()

    if confirmacao not in ("s", "sim"):
        print("Exclusão cancelada.")
        return

    indice = tarefas.index(tarefa)
    removida = tarefas.pop(indice)

    try:
        salvar_dados()
    except RuntimeError:
        tarefas.insert(indice, removida)
        return

    print("Sucesso: tarefa excluída!")


# ==========================================
# 8. FILTROS E BUSCAS
# ==========================================

def filtrar_tarefas():
    print("\n--- Filtrar / Buscar Tarefas ---")
    print("1. Por status")
    print("2. Por prioridade")
    print("3. Por palavra-chave no título ou descrição")
    print("4. Somente tarefas vencidas")

    opcao = input("Escolha uma opção (1-4): ").strip()

    resultados = []

    if opcao == "1":
        entrada = input("Status (Pendente / Concluída): ")
        status = normalizar_status(entrada)

        if status is None:
            print("Status inválido.")
            return

        resultados = [
            t for t in tarefas if t["status"] == status
        ]

    elif opcao == "2":
        entrada = input("Prioridade (Alta / Média / Baixa): ")
        prioridade = normalizar_prioridade(entrada)

        if prioridade is None:
            print("Prioridade inválida.")
            return

        resultados = [
            t for t in tarefas
            if t["prioridade"] == prioridade
        ]

    elif opcao == "3":
        termo = input("Palavra-chave: ").strip().casefold()

        if not termo:
            print("Informe uma palavra-chave.")
            return

        resultados = [
            t for t in tarefas
            if termo in t["titulo"].casefold()
            or termo in t["descricao"].casefold()
        ]

    elif opcao == "4":
        resultados = [
            t for t in tarefas if tarefa_vencida(t)
        ]

    else:
        print("Opção inválida.")
        return

    resultados = sorted(resultados, key=chave_ordenacao)

    if not resultados:
        print("\nNenhuma tarefa encontrada.")
        exibir_totalizadores(resultados)
        return

    print(f"\n--- Resultados: {len(resultados)} tarefa(s) ---")

    for t in resultados:
        imprimir_tarefa(t)

    exibir_totalizadores(resultados)


# ==========================================
# 9. MENU PRINCIPAL
# ==========================================

def menu_principal():
    try:
        carregar_dados()
    except RuntimeError as erro:
        print(f"\nERRO CRÍTICO: {erro}")
        print(
            "O programa será encerrado para preservar os dados."
        )
        return

    while True:
        print("\n" + "=" * 35)
        print("           TASKTRACKER")
        print("=" * 35)
        print("1. Cadastrar tarefa")
        print("2. Visualizar tarefas")
        print("3. Concluir tarefa")
        print("4. Editar tarefa")
        print("5. Excluir tarefa")
        print("6. Filtrar / buscar tarefas")
        print("7. Reabrir tarefa")
        print("8. Sair")
        print("=" * 35)

        try:
            opcao = input("Escolha uma opção (1-8): ").strip()

            if opcao == "1":
                cadastrar_tarefa()
            elif opcao == "2":
                visualizar_tarefas()
            elif opcao == "3":
                concluir_tarefa()
            elif opcao == "4":
                editar_tarefa()
            elif opcao == "5":
                excluir_tarefa()
            elif opcao == "6":
                filtrar_tarefas()
            elif opcao == "7":
                reabrir_tarefa()
            elif opcao == "8":
                print("\nEncerrando o TaskTracker... Até logo!")
                break
            else:
                print("Erro: escolha uma opção entre 1 e 8.")

        except KeyboardInterrupt:
            print("\n\nPrograma interrompido pelo usuário.")
            break

        except EOFError:
            print(
                "\nEntrada encerrada. "
                "O programa será finalizado."
            )
            break

        except RuntimeError as erro:
            print(
                f"\nNão foi possível concluir a operação: {erro}"
            )


# ==========================================
# 10. PONTO DE ENTRADA
# ==========================================

if __name__ == "__main__":
    menu_principal()
