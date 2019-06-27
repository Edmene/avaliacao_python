import random

personagens = []
personagens_enfrentaveis = []
props = {"espada": {"dano": 50, "acc": 25, "crit": 95}, "soqueira": {"dano": 8, "acc": 15, "crit": 92},
         "adaga": {"dano": 15, "acc": 20, "crit": 60}, "besta": {"dano": 35, "acc": 50, "crit": 30},
         "shuriken": {"dano": 35, "acc": 20, "crit": 55}, "pá": {"dano": 45, "acc": 30, "crit": 92},
         "pistola": {"dano": 100, "acc": 2, "crit": 1}}
itens = props.keys()
chaves = [item for item in itens]


def iniciar_variaveis():
    with open("../resources/personagens.txt") as arquivo:
        for line in arquivo:
            personagens.append(line.strip())
            personagens_enfrentaveis.append(line.strip())


def confere_s_n(entrada):
    return entrada.lower() == "sim"


def adiciona_arma_a_personagem(personagem, indice):
    personagem["arma"] = {chaves[indice]: retorna_arma(indice)}


def retorna_arma(indice):
    return props[chaves[indice]]


def acertou_e_critico(arma):
    probabilidade_arma = random.randrange(0, 101)
    probabilidade_critico = random.randrange(0, 101)
    acertou = arma["acc"] <= probabilidade_arma
    critico = arma["crit"] <= probabilidade_critico

    if acertou:
        if critico:
            return arma["dano"] * 2
        else:
            return arma["dano"]
    else:
        return 0


def selecao_de_arma(jogador, selecao):
    if selecao == 0:
        return jogador["dano"]
    else:
        itens_jogador = jogador["arma"].keys()
        arma = [item for item in itens_jogador][0]
        return jogador["arma"][arma]


def selecao_de_ataque(jogador):
    print("Voce pode atacar com ", jogador["arma"], "ou punhos: ", jogador["dano"])
    dano_ataque = {}

    arma = str([item for item in jogador["arma"].keys()][0]).title()
    selecao = int(input_processado(["0", "1"], "0) Punhos 1)"+arma+": "))
    dano_ataque["arma"] = arma
    dano_ataque["dano"] = acertou_e_critico(selecao_de_arma(jogador, selecao))
    return dano_ataque


def ataques_npc(adversario):
    return acertou_e_critico(adversario["dano"])


def define_npc(personagem, vida):
    arma = random.randrange(len(props.keys()))
    vulneravel = random.randrange(len(props.keys()))
    npc = {"nome": personagem, "vida": vida,
           "dano": props[chaves[arma]], "vulneravel": chaves[vulneravel]}
    return npc


def mostra_vida_inicio_rodada(jogador, adversario, aliado):
    print("Vida jogador:", jogador["vida"], "| Vida Inimigo:", adversario["vida"])
    if "viajando_com" in jogador.keys():
        if "aliado_morreu" not in jogador.keys():
            print("Vida do aliado: ", aliado["vida"])


def turno_jogador(jogador, adversario):
    print("Turno do jogador")
    resultado_ataque = selecao_de_ataque(jogador)
    if resultado_ataque["arma"].lower() == adversario["vulneravel"].lower():
        dano_jogador = resultado_ataque["dano"]*10
        adversario["vida"] -= dano_jogador
    else:
        dano_jogador = resultado_ataque["dano"]
        adversario["vida"] -= dano_jogador

    return dano_jogador


def turno_npc(npc, adversarios):

    dano_npc = ataques_npc(npc)
    for adversario in adversarios:
        if "vida" in adversario.keys():
            adversario["vida"] -= dano_npc

    return dano_npc


def mostrar_resultado_rodada(jogador, dano_jogador, dano_aliado, dano_inimigo):

    print("\n\n**********Resultados_Rodada*********")
    print(f"Adversario -{dano_jogador+dano_aliado} vida\nJogador -{dano_inimigo} vida ")
    if "viajando_com" in jogador.keys():
        if "aliado_morreu" not in jogador.keys():
            print(f"Aliado -{dano_inimigo} vida")
    print("*********************************")
    print("\n")


def mostrar_resultado_batalha(jogador, adversario, aliado):
    resultado_adversario = ""
    resultado_jogador = ""
    resultado_aliado = ""
    if adversario["vida"] <= 0:
        resultado_adversario = "morreu"
    else:
        resultado_adversario = "sobreviveu"
    if jogador["vida"] <= 0:
        resultado_jogador = "morreu"
    else:
        resultado_jogador = "sobreviveu"
    print("\n\n**********Resultados_Batalha*********")
    print(f"Adversario {adversario['vida']}  vida -> {resultado_adversario}\nJogador {jogador['vida']} vida -> {resultado_jogador}")
    if "viajando_com" in jogador.keys():
        if "aliado_morreu" not in jogador.keys():
            if jogador["vida"] <= 0:
                resultado_aliado = "morreu"
            else:
                resultado_aliado = "sobreviveu"
            print(f"Aliado {aliado['vida']} vida -> {resultado_aliado}")
    print("*********************************")
    print("\n")


def batalha(jogador, personagem, vida_adversario):
    adversario = define_npc(personagem, vida_adversario)
    aliado = {}

    if "viajando_com" in jogador.keys():
        aliado = define_npc(jogador["viajando_com"], 320)
    print("Batalha mortal contra ", personagem)

    while jogador["vida"] > 0 and adversario["vida"] > 0:
        dano_aliado = 0
        mostra_vida_inicio_rodada(jogador, adversario, aliado)

        dano_jogador = turno_jogador(jogador, adversario)

        print("Turno do adversario")
        dano_inimigo = turno_npc(adversario, [jogador, aliado])

        if "viajando_com" in jogador.keys():
            if "aliado_morreu" not in jogador.keys():
                dano_aliado = turno_npc(aliado, [adversario])
            elif aliado["vida"] <= 0:
                jogador["aliado_morreu"] = True
                print(f"{jogador['nome']} terá de enfreentar seu inimigos sozinho pois seu aliado morreu")

        mostrar_resultado_rodada(jogador, dano_jogador, dano_aliado, dano_inimigo)
        jogador["score"] += dano_jogador

    mostrar_resultado_batalha(jogador, adversario, aliado)
    if jogador["vida"] > 0:
        print("VOCÊ VENCEU A BATALHA")
        jogador["vida"] = 300
        if "viajando_com" in jogador.keys():
            if "aliado_morreu" not in jogador.keys():
                dano_aliado = turno_npc(aliado, [adversario])
                aliado["vida"] = 200
    else:
        print("VOCÊ PERDEU A BATALHA")

    if jogador["vida"] <= 0:
        morreu("")


def morreu(mensagem_extra):
    print("Você morreu.", mensagem_extra)
    print(" X X ")
    print("  0  ")


def mensagem_batalha3(personagem):
    return f"Antes de entrentar face a face o rei voce encontra {personagem}, que foi ignorado antes, e ele o desafia para um duelo"


def input_processado(entradas_aceitas, mensagem):
    entrada = ""
    while entrada not in entradas_aceitas:
        entrada = input(mensagem).lower()
        if entrada not in entradas_aceitas:
            print("Digite uma entrada válida")
    return entrada


def jogo(nome):

    iniciar_variaveis()
    jogador = {"nome": nome, "vida": 300, "dano": {"dano": 5, "acc": 10, "crit": 100}, "score": 0}

    print("O mundo foi devastado e agora é governardo pelo Rei Malvado. Resta a você salvar o reino...")

    item = random.randrange(len(personagens))

    print(f"O personagem {personagens[item]} se aproxima de você e pede se está indo enfrentar o Rei Malvado!")

    escolha = input_processado(["nao", "sim"], "Você vai dizer sim/nao? ")

    if confere_s_n(escolha):
        jogador["viajando_com"] = personagens[item]
        personagens_enfrentaveis.remove(personagens[item])
    else:
        jogador["ignorou"] = personagens[item]

    escolha_1 = "Ao se aproximar de um mercador voce ve que ele esta vendendo armas."
    escolha_1_alt = "EVENTO ESPECIAL: Voce ve um bau e decide abri-lo"
    pergunta_1 = "Comprar uma  => "
    batalha_1 = "Indo rumo ao castelo encontras o general"
    batalha_2 = "Se aproximando do castelo um guarda real que lhe enfrenta ele é"

    selecao_evento = random.randrange(2)

    arma_mercador = []
    armas_indices = []
    limite_lista = random.randrange(len(itens))
    if limite_lista == 0:
        limite_lista = 1
    i = 0
    for item in itens:
        if i < limite_lista:
            arma_mercador.append(f"{i + 1}:{item}")
            armas_indices.append(str(i))
            i += 1

    if selecao_evento == 1:
        print(escolha_1)
        pergunta = int(input_processado(armas_indices, pergunta_1 + str(arma_mercador) + " Escolha pelo numero correspondente: "))

        if pergunta in range(1, limite_lista+1):
            adiciona_arma_a_personagem(jogador, pergunta - 1)
    else:
        print(escolha_1_alt)
        if random.randrange(8) < 5:
            aleatorio_bau = random.randrange(4, 7)
            adiciona_arma_a_personagem(jogador, aleatorio_bau)
            print(f"RESULTADO: Você achou a arma {chaves[aleatorio_bau]}")
        else:
            morreu(", era um mimico, não um baú!!! ")
            return jogador

    inimigo = define_personagem_inimigo(None)
    print(batalha_1, inimigo)
    if not decisao_de_fugir():
        batalha(jogador, inimigo, 200)
        if jogador["vida"] < 0:
            return jogador

    inimigo = define_personagem_inimigo(None)
    print(batalha_2, inimigo)
    if not decisao_de_fugir():
        batalha(jogador, inimigo, 240)
        if jogador["vida"] < 0:
            return jogador

    if "viajando_com" not in jogador.keys():
        inimigo = define_personagem_inimigo(jogador["ignorou"])
        mensagem_batalha3(inimigo)
        if not decisao_de_fugir():
            batalha(jogador, inimigo, 250)
            if jogador["vida"] < 0:
                return jogador

    return jogador


def decisao_de_fugir():
    entrada = input_processado(["f", "l"], "Você deseja fugir ou lutar: f/l: ")
    if entrada == "f":
        fuga_bem_sucedida = random.randrange(20) > 17
        if not fuga_bem_sucedida:
            print("A fuga falhou, terá de enfrentar seu adversario")
        return fuga_bem_sucedida
    else:
        return False


def define_personagem_inimigo(personagem):
    inimigo = ""
    if personagem is None:
        item = random.randrange(len(personagens_enfrentaveis))
        inimigo = personagens_enfrentaveis[item]
    else:
        inimigo = personagem

    personagens_enfrentaveis.remove(inimigo)
    return inimigo


def menu():
    game_loop = True
    while game_loop:
        print("****Bem vindo ao RPG da Avaliação****")

        print("*********Escolha uma opção!**********")

        print("I - Iniciar\nS - Sair")

        opcao = input_processado(["i", "s"], "Opção: ")

        if opcao == "s":
            game_loop = False
        else:
            nome = input("Digite seu nome: ")
            print("Vamos começar a aventura,", nome + "!")

            resultado = jogo(nome)
            print(resultado)
            game_loop = False


menu()
