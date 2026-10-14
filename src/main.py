import json
import os

# ==========================================
# TaskTracker - Sistema de Gerenciamento de Tarefas
# ==========================================

ARQUIVO_DADOS = 'tarefas.json'
tarefas = []
id_contador = 1

def carregar_dados():
    """Carrega os dados do arquivo JSON para a memória."""
    global tarefas, id_contador
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
            tarefas = json.load(f)
            if tarefas:
                # Atualiza o contador de ID para ser o maior ID existente + 1
                id_contador = max(t['id'] for t in tarefas) + 1

def salvar_dados():
    """Salva a lista de tarefas atual no arquivo JSON."""
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(tarefas, f, ensure_ascii=False, indent=4)

def exibir_totalizadores(lista_alvo=None):
    """Exibe o totalizador de status. Pode receber uma lista filtrada ou usar a global."""
    if lista_alvo is None:
        lista_alvo = tarefas
        
    pendentes = sum(1 for t in lista_alvo if t['status'] == 'Pendente')
    concluidas = sum(1 for t in lista_alvo if t['status'] == 'Concluída')
            
    print(f"\nResumo: {pendentes} tarefa(s) pendente(s) | {concluidas} tarefa(s) concluída(s)")

def cadastrar_tarefa():
    global id_contador
    print("\n--- Cadastrar Nova Tarefa ---")
    
    while True:
        titulo = input("Título da tarefa: ").strip()
        if titulo == "":
            print("Erro: O Título da tarefa não pode estar em branco. Tente novamente.")
        else:
            break
            
    descricao = input("Descrição (opcional): ").strip()
    
    prioridades_validas = ["Alta", "Média", "Media", "Baixa"]
    while True:
        prioridade = input("Prioridade (Alta / Média / Baixa): ").strip().capitalize()
        if prioridade in prioridades_validas:
            if prioridade == "Media":
                prioridade = "Média"
            break
        else:
            print("Erro: Prioridade inválida. Escolha somente entre Alta, Média ou Baixa.")
            
    data_limite = input("Data Limite (opcional - pressione Enter para pular): ").strip()
    
    nova_tarefa = {
        "id": id_contador,
        "titulo": titulo,
        "descricao": descricao,
        "prioridade": prioridade,
        "data_limite": data_limite if data_limite else "Não informada",
        "status": "Pendente"
    }
    
    tarefas.append(nova_tarefa)
    id_contador += 1
    salvar_dados() # Salva no JSON
    print("\nSucesso: Tarefa cadastrada com sucesso!")

def imprimir_tarefa(t):
    """Função auxiliar para imprimir uma tarefa formatada."""
    print("-" * 40)
    print(f"ID: {t['id']}")
    print(f"Título: {t['titulo']}")
    print(f"Descrição: {t.get('descricao', '')}")
    print(f"Prioridade: {t['prioridade']}")
    print(f"Data Limite: {t['data_limite']}")
    print(f"Status: {t['status']}")

def visualizar_tarefas():
    print("\n--- Lista de Tarefas ---")
    if not tarefas:
        print("Nenhuma tarefa cadastrada no momento.")
        return

    for t in tarefas:
        imprimir_tarefa(t)
    exibir_totalizadores()

def concluir_tarefa():
    if not tarefas:
        print("\nErro: Nenhuma tarefa cadastrada no sistema ainda.")
        return
        
    print("\n--- Concluir Tarefa ---")
    try:
        id_informado = int(input("Digite o ID da tarefa que deseja concluir: "))
    except ValueError:
        print("Erro: O ID informado deve ser um número inteiro.")
        return

    for t in tarefas:
        if t['id'] == id_informado:
            if t['status'] == 'Pendente':
                t['status'] = 'Concluída'
                salvar_dados()
                print("\nSucesso: Tarefa concluída com sucesso!")
            else:
                print("\nAviso: Esta tarefa já foi finalizada anteriormente.")
            return
            
    print("\nErro: Tarefa não encontrada. Verifique o ID e tente novamente.")

def editar_tarefa():
    print("\n--- Editar Tarefa ---")
    try:
        id_informado = int(input("Digite o ID da tarefa que deseja editar: "))
    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")
        return

    for t in tarefas:
        if t['id'] == id_informado:
            print("Deixe o campo em branco e pressione Enter se não quiser alterá-lo.")
            
            novo_titulo = input(f"Título atual ({t['titulo']}): ").strip()
            if novo_titulo: t['titulo'] = novo_titulo
            
            nova_desc = input(f"Descrição atual ({t['descricao']}): ").strip()
            if nova_desc: t['descricao'] = nova_desc
            
            nova_prio = input(f"Prioridade atual ({t['prioridade']}): ").strip().capitalize()
            if nova_prio in ["Alta", "Média", "Media", "Baixa"]:
                t['prioridade'] = "Média" if nova_prio == "Media" else nova_prio
                
            nova_data = input(f"Data Limite atual ({t['data_limite']}): ").strip()
            if nova_data: t['data_limite'] = nova_data

            salvar_dados()
            print("\nSucesso: Tarefa atualizada!")
            return
            
    print("\nErro: Tarefa não encontrada.")

def excluir_tarefa():
    global tarefas
    print("\n--- Excluir Tarefa ---")
    try:
        id_informado = int(input("Digite o ID da tarefa que deseja excluir: "))
    except ValueError:
        print("Erro: O ID deve ser um número inteiro.")
        return

    tamanho_original = len(tarefas)
    tarefas = [t for t in tarefas if t['id'] != id_informado]
    
    if len(tarefas) < tamanho_original:
        salvar_dados()
        print("\nSucesso: Tarefa excluída!")
    else:
        print("\nErro: Tarefa não encontrada.")

def filtrar_tarefas():
    print("\n--- Filtrar Tarefas ---")
    print("1. Por Status (Pendente/Concluída)")
    print("2. Por Prioridade (Alta/Média/Baixa)")
    print("3. Buscar por palavra no título")
    
    opcao = input("Escolha uma opção de filtro (1-3): ").strip()
    resultados = []
    
    if opcao == '1':
        status_busca = input("Digite o status (Pendente ou Concluída): ").strip().capitalize()
        if status_busca in ['Pendente', 'Concluida']: status_busca = 'Concluída' if status_busca == 'Concluida' else 'Pendente'
        resultados = [t for t in tarefas if t['status'] == status_busca]
        
    elif opcao == '2':
        prio_busca = input("Digite a prioridade (Alta, Média ou Baixa): ").strip().capitalize()
        if prio_busca == 'Media': prio_busca = 'Média'
        resultados = [t for t in tarefas if t['prioridade'] == prio_busca]
        
    elif opcao == '3':
        termo = input("Digite a palavra-chave para buscar no título: ").strip().lower()
        resultados = [t for t in tarefas if termo in t['titulo'].lower()]
        
    else:
        print("Opção inválida.")
        return

    if not resultados:
        print("\nNenhuma tarefa encontrada com esse filtro.")
    else:
        print(f"\n--- Resultados da Busca ({len(resultados)} encontrada(s)) ---")
        for t in resultados:
            imprimir_tarefa(t)
        exibir_totalizadores(resultados)


def menu_principal():
    carregar_dados() # Carrega os dados salvos ao abrir o programa
    
    while True:
        print("\n" + "="*30)
        print("       TASKTRACKER")
        print("="*30)
        print("1. Cadastrar Tarefa")
        print("2. Visualizar Tarefas")
        print("3. Concluir Tarefa")
        print("4. Editar Tarefa")
        print("5. Excluir Tarefa")
        print("6. Filtrar/Buscar Tarefas")
        print("7. Sair")
        print("="*30)
        
        opcao = input("Escolha uma opção (1-7): ").strip()
        
        if opcao == '1':
            cadastrar_tarefa()
        elif opcao == '2':
            visualizar_tarefas()
        elif opcao == '3':
            concluir_tarefa()
        elif opcao == '4':
            editar_tarefa()
        elif opcao == '5':
            excluir_tarefa()
        elif opcao == '6':
            filtrar_tarefas()
        elif opcao == '7':
            print("\nEncerrando o TaskTracker... Até logo!")
            break
        else:
            print("\nErro: Opção inválida! Escolha um número entre 1 e 7.")

# Ponto de entrada do sistema
if __name__ == "__main__":
    menu_principal()