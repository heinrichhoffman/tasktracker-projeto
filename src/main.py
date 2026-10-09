# ==========================================
# TaskTracker - Sistema de Gerenciamento de Tarefas
# ==========================================

# Base de dados em memória (lista de dicionários)
tarefas = []
id_contador = 1  # Usado para gerar um identificador único para cada tarefa

def exibir_totalizadores():
    """3.4 Totalizador de Status"""
    pendentes = 0
    concluidas = 0
    
    for tarefa in tarefas:
        if tarefa['status'] == 'Pendente':
            pendentes += 1
        elif tarefa['status'] == 'Concluída':
            concluidas += 1
            
    print(f"\nResumo: {pendentes} tarefa(s) pendente(s) | {concluidas} tarefa(s) concluída(s)")

def cadastrar_tarefa():
    """3.1 Cadastro de Tarefa"""
    global id_contador
    print("\n--- Cadastrar Nova Tarefa ---")
    
    # R01: Validação de Título vazio
    while True:
        titulo = input("Título da tarefa: ").strip()
        if titulo == "":
            print("Erro (R01): O Título da tarefa não pode estar em branco. Tente novamente.")
        else:
            break
            
    descricao = input("Descrição (opcional): ").strip()
    
    # R02: Validação de Prioridade (Ajustado para aceitar "Media" sem acento)
    prioridades_validas = ["Alta", "Média", "Media", "Baixa"]
    while True:
        prioridade = input("Prioridade (Alta / Média / Baixa): ").strip().capitalize()
        if prioridade in prioridades_validas:
            if prioridade == "Media":
                prioridade = "Média" # Padroniza com acento
            break
        else:
            print("Erro (R02): Prioridade inválida. Escolha somente entre Alta, Média ou Baixa.")
            
    data_limite = input("Data Limite (opcional - pressione Enter para pular): ").strip()
    
    # R03: Status atribuído automaticamente como 'Pendente'
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
    
    print("\nSucesso: Tarefa cadastrada com sucesso!")

def visualizar_tarefas():
    """3.2 Visualização de Tarefas"""
    print("\n--- Lista de Tarefas ---")
    
    if len(tarefas) == 0:
        print("Nenhuma tarefa cadastrada no momento.")
        return

    # Percorrendo a lista
    for t in tarefas:
        print("-" * 40)
        print(f"ID: {t['id']}")
        print(f"Título: {t['titulo']}")
        print(f"Prioridade: {t['prioridade']}")
        print(f"Data Limite: {t['data_limite']}")
        print(f"Status: {t['status']}")
    
    # Apresentar o total de tarefas ao final da exibição
    exibir_totalizadores()

def concluir_tarefa():
    """3.3 Conclusão de Tarefa"""
    if len(tarefas) == 0:
        print("\nErro: Nenhuma tarefa cadastrada no sistema ainda.")
        return
        
    visualizar_tarefas()
    
    print("\n--- Concluir Tarefa ---")
    try:
        id_informado = int(input("Digite o ID da tarefa que deseja concluir: "))
    except ValueError:
        print("Erro: O ID informado deve ser um número inteiro.")
        return

    # Busca a tarefa pelo ID informado
    tarefa_encontrada = None
    for t in tarefas:
        if t['id'] == id_informado:
            tarefa_encontrada = t
            break
            
    # R05: Mensagem de erro caso a operação não possa ser realizada
    if tarefa_encontrada is None:
        print("\nErro: Tarefa não encontrada. Verifique o ID e tente novamente.")
        return
        
    # R04: Alterar o status para Concluída
    if tarefa_encontrada['status'] == 'Pendente':
        tarefa_encontrada['status'] = 'Concluída'
        print("\nSucesso: Tarefa concluída com sucesso!")
    else:
        print("\nAviso: Esta tarefa já foi finalizada anteriormente.")

def menu_principal():
    """3.5 Fluxo Geral do Sistema"""
    while True:
        print("\n" + "="*30)
        print("       TASKTRACKER")
        print("="*30)
        print("1. Cadastrar Tarefa")
        print("2. Visualizar Tarefas")
        print("3. Concluir Tarefa")
        print("4. Sair")
        print("="*30)
        
        opcao = input("Escolha uma opção (1-4): ").strip()
        
        if opcao == '1':
            cadastrar_tarefa()
        elif opcao == '2':
            visualizar_tarefas()
        elif opcao == '3':
            concluir_tarefa()
        elif opcao == '4':
            print("\nEncerrando o TaskTracker... Até logo!")
            break
        else:
            print("\nErro: Opção inválida! Escolha um número entre 1 e 4.")

# Ponto de entrada do sistema
if __name__ == "__main__":
    menu_principal()
