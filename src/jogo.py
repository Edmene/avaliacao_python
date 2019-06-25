personagens = []

with open("../resources/personagens.txt") as arquivo:
    for line in arquivo:
        personagens.append(line.strip())


def menu():
    game_loop = True
    while game_loop:
        print("****Bem vindo ao RPG da Avaliação****")

        print("*********Escolha uma opção!**********")

        print("I - Iniciar\nS - Sair")

        opcao = input("Opção: ").lower()

        if opcao == "s":
            game_loop = False
        else:
            nome = input("Digite seu nome: ")
            print("Vamos começar a aventura,", nome + "!")

            game_loop = False


menu()
