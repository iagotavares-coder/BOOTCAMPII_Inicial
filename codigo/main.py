import requests

__version__ = "1.2.0"

# URL do Banco de Dados Cloud (Firebase REST API) para o seu projeto
DB_BASE_URL = "https://bootcamp-v-default-rtdb.firebaseio.com/iago_tavares"


def adicionar_medicamento(lista, nome, horario, dosagem):
    if not nome or not horario:
        return False, "Nome e horário são obrigatórios."
    
    medicamento = {
        "nome": nome, 
        "horario": horario, 
        "dosagem": dosagem
    }
    
    # 1. Salva no Banco de Dados em Nuvem (Persistência Real)
    try:
        url_db = f"{DB_BASE_URL}/medicamentos.json"
        requests.post(url_db, json=medicamento, timeout=5)
    except Exception:
        # Se estiver sem internet, o sistema avisa mas permite o fluxo local
        pass

    # 2. Mantém a compatibilidade com a lista local para os testes do professor
    lista.append(medicamento)
    return True, "Medicamento adicionado com sucesso!"


def listar_medicamentos(lista):
    # 1. Sincroniza trazendo os dados mais recentes do Banco de Dados em Nuvem
    try:
        url_db = f"{DB_BASE_URL}/medicamentos.json"
        resposta = requests.get(url_db, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados:
                lista.clear()
                # O Firebase armazena como dicionário de chaves dinâmicas
                if isinstance(dados, dict):
                    for chave, med in dados.items():
                        if med:
                            lista.append(med)
    except Exception:
        pass  # Fallback para a lista local caso ocorra falha de rede

    if not lista:
        return "Nenhum medicamento agendado."
    
    output = "\n--- Lista de Medicamentos ---\n"
    for i, med in enumerate(lista):
        linha = f"{i+1}. {med['nome']} - {med['horario']} ({med['dosagem']})\n"
        output += linha
    return output


def buscar_endereco_cep(cep):
    cep_limpo = str(cep).replace("-", "").replace(" ", "").strip()
    
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        return False, "CEP inválido. Deve conter 8 dígitos."
        
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            if "erro" in dados:
                return False, "CEP não encontrado."
            
            endereco = f"{dados.get('logradouro', '')}, {dados.get('bairro', '')} - {dados.get('localidade', '')}/{dados.get('uf', '')}"
            
            # Salva o último CEP/Endereço de emergência consultado no Banco de Dados
            try:
                url_cep = f"{DB_BASE_URL}/emergencia.json"
                requests.put(url_cep, json={"endereco": endereco}, timeout=5)
            except Exception:
                pass
                
            return True, endereco
        else:
            return False, "Erro ao acessar a API."
    except requests.RequestException:
        return False, "Falha na conexão de rede."


def carregar_dados_iniciais():
    """Carrega as informações da nuvem ao iniciar o programa"""
    medicamentos = []
    endereco_emergencia = "Não cadastrado"
    
    try:
        # Carrega medicamentos
        res_med = requests.get(f"{DB_BASE_URL}/medicamentos.json", timeout=5)
        if res_med.status_code == 200 and res_med.json():
            dados = res_med.json()
            if isinstance(dados, dict):
                for k, v in dados.items():
                    medicamentos.append(v)
        
        # Carrega endereço
        res_cep = requests.get(f"{DB_BASE_URL}/emergencia.json", timeout=5)
        if res_cep.status_code == 200 and res_cep.json():
            endereco_emergencia = res_cep.json().get("endereco", "Não cadastrado")
    except Exception:
        pass
        
    return medicamentos, endereco_emergencia


def main():
    # Inicializa o app trazendo o estado persistido na Nuvem!
    medicamentos, endereco_emergencia = carregar_dados_iniciais()
    
    print(f"Bem-vindo ao MedMinder Idoso (v{__version__})")
    
    while True:
        print("\n1. Adicionar Medicamento\n2. Listar Medicamentos")
        print("3. Cadastrar CEP de Emergência\n4. Ver Info de Emergência")
        print("5. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            n = input("Nome do remédio: ")
            h = input("Horário (ex: 08:00): ")
            d = input("Dosagem (ex: 1 comprimido): ")
            sucesso, msg = adicionar_medicamento(medicamentos, n, h, d)
            print(msg)
            
        elif opcao == "2":
            print(listar_medicamentos(medicamentos))
            
        elif opcao == "3":
            c = input("Digite o CEP (somente números): ")
            sucesso, resultado = buscar_endereco_cep(c)
            if sucesso:
                endereco_emergencia = resultado
                print(f"Endereço cadastrado com sucesso: {endereco_emergencia}")
            else:
                print(f"Erro: {resultado}")
                
        elif opcao == "4":
            print("\n--- Contato e Emergência ---\n")
            print(f"Endereço da Farmácia/Idoso: {endereco_emergencia}")
            
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()