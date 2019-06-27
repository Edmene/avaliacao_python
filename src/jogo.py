import random

personagens = []
jogador = {"nome": "", "vida": 300, "dano": {"dano": 5, "acc": 10, "crit": 100}, "score": 0}

with open("../resources/personagens.txt") as arquivo:
    for line in arquivo:
        personagens.append(line.strip())

def confere_s_n(entrada):
    return entrada.lower() == "sim"

def jogo(nome):
    props = {"espada": {"dano": 50, "acc": 75, "crit": 5}, "punhos": {"dano": 5, "acc": 90, "crit": 1},
             "adaga": {"dano": 15, "acc": 80, "crit": 30}, "besta": {"dano": 35, "acc": 50, "crit": 70},
             "shuriken": {"dano": 35, "acc": 80, "crit": 65}, "pá": {"dano": 45, "acc": 70, "crit": 8},
             "pistola": {"dano": 100, "acc": 99, "crit": 100}}

    jogador = {"nome": nome, "vida": 300, "dano": props["punhos"]}

    print("O mundo foi devastado e agora é governardo pelo Rei Malvado. Resta a você salvar o reino...")

    item = random.randrange(len(personagens))

    print(f"O personagem {personagens[item]} se aproxima de você e pede se está indo enfrentar o Rei Malvado!")

    escolha = input("Você vai dizer Sim/Não? ")

    if confere_s_n(escolha):
        jogador["viajando_com"] = personagens[item]
    else:
        jogador["ignorou"] = personagens[item]

    escolha_1 = "Ao se aproximar de um mercador voce ve que ele esta vendendo armas."
    escolha_1_alt = "Voce ve um bau e decide abri-lo"
    pergunta_1 = "Comprar uma  => "
    escolha_2 = "Um inimigo ameacador eh avistado a alguns metros de voce, iras se esconder ou ariscar lutar"

    selecao_evento = random.randrange(2)

    arma_mercador = []

    itens = props.keys()
    chaves = []
    limite_lista = random.randrange(len(itens))
    i = 0
    for item in itens:
        if i < limite_lista:
            arma_mercador.append(f"{i + 1}:{item}")
            i += 1
        chaves.append(item)


    if selecao_evento == 1:

        print(escolha_1)
        pergunta = int(input(pergunta_1 + str(arma_mercador) + " Escolha pelo numero correspondente: "))

        if pergunta in range(1, limite_lista+1):

            jogador["arma"] = {chaves[pergunta-1]: props[chaves[pergunta -1]]}

    else:
        print(escolha_1_alt)
        if random.randrange(8) < 5:
            print(chaves, limite_lista)

            jogador["arma"] = {chaves[limite_lista]: props[chaves[limite_lista]]}
            print(f"Você achou a arma {chaves[limite_lista]}")
        else:
            print("Você morreu, era um mimico, não um baú!!! ")
            print(" X X ")
            print("  0  ")
            return


    print(jogador)

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
