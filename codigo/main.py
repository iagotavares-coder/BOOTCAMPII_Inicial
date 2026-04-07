__version__ = "1.0.0"


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
        output += (
            f"{i+1}. {med['nome']} - {med['horario']} "
            f"({med['dosagem']})\n"
        )
    return output


def main():
    medicamentos = []
    print(f"Bem-vindo ao MedMinder Idoso (v{__version__})")
    while True:
        print("\n1. Adicionar Medicamento\n2. Listar\n3. Sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            nome = input("Nome do remédio: ")
            horario = input("Horário (ex: 08:00): ")
            dosagem = input("Dosagem (ex: 1 comprimido): ")
            # Ajuste para evitar a linha longa (E501)
            res = adicionar_medicamento(
                medicamentos, nome, horario, dosagem
            )
            sucesso, msg = res
            print(msg)
        elif opcao == "2":
            print(listar_medicamentos(medicamentos))
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
