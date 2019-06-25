import random

personagens = []

with open("../resources/personagens.txt") as arquivo:
    for line in arquivo:
        personagens.append(line.strip())

def confere_s_n(entrada):
    return entrada.lower() == "sim"

def jogo(nome):

    print("O mundo foi devastado e agora é governardo pelo Rei Malvado. Resta a você salvar o reino...")

    item = random.randrange(len(personagens))

    print(f"O personagem {personagens[item]} se aproxima de você e pede se está indo enfrentar o Rei Malvado!")

    escolha = input("Você vai dizer Sim/Não? ")

    relacoes_personagens = {}

    if confere_s_n(escolha):
        relacoes_personagens["viajando_com"] = personagens[item]
    else:
        relacoes_personagens["ignorou"] = personagens[item]



    print(relacoes_personagens)


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

            jogo(nome)
            game_loop = False


menu()
