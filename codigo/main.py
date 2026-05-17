import requests

__version__ = "1.1.0"


def adicionar_medicamento(lista, nome, horario, dosagem):
    if not nome or not horario:
        return False, "Nome e horário são obrigatórios."
    medicamento = {"nome": nome, "horario": horario, "dosagem": dosagem}
    lista.append(medicamento)
    return True, "Medicamento adicionado com sucesso!"


def listar_medicamentos(lista):
    if not lista:
        return "Nenhum medicamento agendado."
    output = "\n--- Lista de Medicamentos ---\n"
    for i, med in enumerate(lista):
        linha = (f"{i+1}. {med['nome']} - {med['horario']} "
                 f"({med['dosagem']})\n")
        output += linha
    return output


def buscar_endereco_cep(cep):
    cep_limpo = cep.replace("-", "").replace(" ", "")
    if len(cep_limpo) != 8 or not cep_limpo.isdigit():
        return False, "CEP inválido. Deve conter 8 dígitos."

    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            dados = resposta.json()
            if "erro" in dados:
                return False, "CEP não encontrado."
            endereco = (f"{dados.get('logradouro', '')}, "
                        f"{dados.get('bairro', '')} - "
                        f"{dados.get('localidade', '')}/{dados.get('uf', '')}")
            return True, endereco
        return False, "Erro ao conectar com o serviço de CEP."
    except requests.RequestException:
        return False, "Falha na conexão de rede."


def main():
    medicamentos = []
    endereco_emergencia = "Não cadastrado"
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
                print(f"Endereço cadastrado: {endereco_emergencia}")
            else:
                print(f"Erro: {resultado}")
        elif opcao == "4":
            print(f"\n--- Contato e Emergência ---\n"
                  f"Endereço da Farmácia/Idoso: {endereco_emergencia}")
        elif opcao == "5":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()