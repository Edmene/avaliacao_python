import random

personagens = []
personagens_enfrentaveis = []
props = {"espada": {"dano": 50, "acc": 25, "crit": 95}, "soqueira": {"dano": 15, "acc": 15, "crit": 92},
         "adaga": {"dano": 25, "acc": 20, "crit": 60}, "besta": {"dano": 37, "acc": 50, "crit": 30},
         "shuriken": {"dano": 28, "acc": 20, "crit": 55}, "pá": {"dano": 45, "acc": 30, "crit": 92},
         "lanca": {"dano": 70, "acc": 15, "crit": 20}, "pistola": {"dano": 100, "acc": 2, "crit": 1}}
itens = props.keys()
chaves = [item for item in itens]
modificadores = ["penhasco", "vento", "buraco", "mina"]


def iniciar_variaveis():
    with open("../resources/personagens.txt") as arquivo:
        for line in arquivo:
            personagens.append(line.strip())
            personagens_enfrentaveis.append(line.strip())


def grava_resultado_arquivo(jogador):
    ganhou = "Nao"
    if jogador["ganhou"]:
        ganhou = "Sim"
    with open("../resources/scores.txt", "a") as arquivo:
        arquivo.writelines(f"Jogador: {jogador['nome']}, Score: {jogador['score']}, Ganhou: {ganhou};\n")


def le_scores_arquivo():
    with open("../resources/scores.txt", "r") as arquivo:
        linhas = arquivo.read().split(";")
        return linhas


def mostra_scores(linhas):
    if len(linhas[0].strip()) > 0:
        print("SCORES")
        for linha in linhas:
            print(linha.strip())
    else:
        print("Não há resultados registrados")


def gera_vulnerabilidade():
    vulneravel = random.randrange(len(props.keys()))
    return chaves[vulneravel]


def adiciona_arma_a_personagem(personagem, indice):
    if {chaves[indice]: retorna_arma(indice)} not in personagem["armas"]:
        personagem["armas"].append({chaves[indice]: retorna_arma(indice)})


def retorna_arma(indice):
    return props[chaves[indice]]


def listagem_armas_personagem(personagem):
    contador = 0
    texto = ""
    entradas_validas = []
    armas_personagem = personagem["armas"]
    armas = []
    for arma in armas_personagem:
        texto += f"{contador+1}){retorna_nome_dict_arma(arma).title()}"
        armas.append(arma)
        if contador + 1 < len(armas_personagem):
            texto += " "
        entradas_validas.append(str(contador+1))
        contador += 1
    return {"validos": entradas_validas, "armas_selecao": texto, "armas": armas}


def retorna_nome_dict_arma(arma):
    return str([item for item in arma.keys()][0])


def define_npc(personagem, vida):
    arma = random.randrange(len(props.keys()))

    npc = {"nome": personagem, "vida": float(vida),
           "dano": {chaves[arma]: props[chaves[arma]]}, "vulneravel": gera_vulnerabilidade(),
           "mostrar_vulneravel": False}
    return npc


def mostra_vida_inicio_rodada(jogador, adversario, aliado):
    print("Vida jogador:", jogador["vida"], "| Vida Inimigo:", adversario["vida"])
    if "viajando_com" in jogador.keys():
        if "aliado_morreu" not in jogador.keys():
            print("Vida do aliado: ", aliado["vida"])


def mostrar_resultado_rodada(jogador, dano_jogador, dano_aliado, dano_inimigo):
    dano_aliado_normalizado = 0
    if type(dano_aliado) is list:
        dano_aliado_normalizado = dano_aliado[0]
    print("\n\n**********Resultados_Rodada*********")
    print(f"Adversario -{dano_jogador+dano_aliado_normalizado} vida\nJogador -{dano_inimigo[0]} vida ")
    if "viajando_com" in jogador.keys():
        if "aliado_morreu" not in jogador.keys():
            print(f"Aliado -{dano_inimigo[1]} vida")
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
    print(f"Adversario {adversario['vida']}  vida -> {resultado_adversario}"
          f"\nJogador {jogador['vida']} vida -> {resultado_jogador}")

    if "viajando_com" in jogador.keys():
        if "aliado_morreu" not in jogador.keys():
            if jogador["vida"] <= 0:
                resultado_aliado = "morreu"
            else:
                resultado_aliado = "sobreviveu"
            print(f"Aliado {aliado['vida']} vida -> {resultado_aliado}")
    print("*********************************")
    print("\n")


def acertou_e_critico(arma, modificador):
    probabilidade_arma = random.randrange(0, 101)
    probabilidade_critico = random.randrange(0, 101)
    acertou = False
    critico = arma["crit"] <= probabilidade_critico

    if modificador == "vento":
        acertou = arma["acc"] <= probabilidade_arma
        if random.randrange(2) > 0:
            acertou = not acertou
    else:
        acertou = arma["acc"] <= probabilidade_arma

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
        itens_jogador = jogador["armas"]
        arma = itens_jogador[int(selecao)-1]
        chave = retorna_nome_dict_arma(arma)
        return arma[chave]


def selecao_de_ataque(jogador, modificador):
    dano_ataque = {}
    print("você pode atacar com as armas ", jogador["armas"], "ou punhos: ", jogador["dano"])
    listagem_armas = listagem_armas_personagem(jogador)
    selecao = int(input_processado(listagem_armas["validos"], "0) Punhos "+listagem_armas['armas_selecao']+": "))
    arma = listagem_armas["armas"][selecao-1]
    dano_ataque["arma"] = retorna_nome_dict_arma(arma)
    dano_ataque["dano"] = acertou_e_critico(selecao_de_arma(jogador, selecao), modificador)
    return dano_ataque


def turno_jogador(jogador, adversario, modificador):
    print("Turno do jogador")

    afetado_por_modificador = efeitos_modificador(modificador, jogador)

    mais_uma_vez = True
    compostura_adversario = 2
    dano_jogador = 0
    if not afetado_por_modificador:
        while mais_uma_vez and compostura_adversario > 0:
            resultado_ataque = selecao_de_ataque(jogador, modificador)
            if resultado_ataque["arma"].lower() == adversario["vulneravel"].lower():
                if resultado_ataque["dano"] > 0:
                    print("Ataque a vulnerabilidade: mais um ataque disponivel no turno")
                    adversario["mostrar_vulneravel"] = True
                    dano_jogador += resultado_ataque["dano"] * compostura_adversario+1
            else:
                dano_jogador += resultado_ataque["dano"]
                mais_uma_vez = False
            compostura_adversario -= 1

    adversario["vida"] -= dano_jogador

    return dano_jogador


def ataques_npc(adversario, modificador):
    arma = adversario["dano"]
    chave = retorna_nome_dict_arma(arma)
    return acertou_e_critico(arma[chave], modificador)


def turno_npc(npc, adversarios, modificador):
    afetado_por_modificador = efeitos_modificador(modificador, npc)

    array_de_danos = []
    if not afetado_por_modificador:

        for adversario in adversarios:
            dano_npc = 0
            if "vida" in adversario.keys():

                mais_uma_vez = True
                compostura_adversario = 1
                dano_npc_cumulativo = 0
                while mais_uma_vez and compostura_adversario > 0:
                    dano_npc = ataques_npc(npc, modificador)
                    if retorna_nome_dict_arma(npc["dano"]).lower() == adversario["vulneravel"].lower():
                        if dano_npc > 0:
                            print("Ataque a vulnerabilidade: mais um ataque disponivel no turno")
                            adversario["mostrar_vulneravel"] = True
                            dano_npc *= compostura_adversario+1
                    else:
                        mais_uma_vez = False
                    dano_npc_cumulativo += dano_npc
                    compostura_adversario -= 1

                adversario["vida"] -= dano_npc_cumulativo
                array_de_danos.append(dano_npc_cumulativo)
    else:
        for adversario in adversarios:
            array_de_danos.append(0)

    return array_de_danos


def efeitos_modificador(modificador, personagem):
    if modificador == "buraco":
        if random.randrange(10) > 3:
            print(f"{personagem['nome'].title()} tropeçou num buraco, logo perdeu a chance de atacar.")
            return True
    if modificador == "mina":
        numero_mina = random.randrange(4)
        if numero_mina > 2:
            personagem["vida"] -= (numero_mina * numero_mina)
            print(f"{personagem['nome'].title()} caiu numa mina, dano - > {(numero_mina * numero_mina)}")
            return True
    if modificador == "penhasco":
        if random.randrange(10) < 2:
            personagem["vida"] = 0
            print(f"{personagem['nome'].title()} caiu de um penhasco, dano - > {300.0}")
            return True


def batalha(jogador, personagem, vida_adversario, modificador):
    adversario = define_npc(personagem, vida_adversario)
    aliado = {}

    modificador_nome = modificador
    if modificador == "":
        modificador_nome = "nenhum"
    print(f"MODIFICADOR AMBIENTAL DE BATALHA: {modificador_nome.title()}")

    if "viajando_com" in jogador.keys():
        aliado = define_npc(jogador["viajando_com"], 320)
    print("Batalha mortal contra ", personagem)

    if random.randrange(30) > 25:
        print("você percebe um maneirismo do seu adversario e percebe pela sua experiencia")
        print(f"******{adversario['nome']} -> Vulneravel a {adversario['vulneravel']}*****")

    while jogador["vida"] > 0 and adversario["vida"] > 0:
        dano_aliado = 0
        dano_inimigo = 0
        mostra_vida_inicio_rodada(jogador, adversario, aliado)

        dano_jogador = turno_jogador(jogador, adversario, modificador)

        print("Turno do adversario")
        if jogador["vida"] > 0:
            dano_inimigo = turno_npc(adversario, [jogador, aliado], modificador)

        if "viajando_com" in jogador.keys():
            if "aliado_morreu" not in jogador.keys():
                if adversario["vida"] > 0:
                    print("Turno do aliado")
                    dano_aliado = turno_npc(aliado, [adversario], modificador)
            elif aliado["vida"] <= 0:
                jogador["aliado_morreu"] = True
                print(f"{jogador['nome']} terá de enfreentar seu inimigos sozinho pois seu aliado morreu")

        mostrar_resultado_rodada(jogador, dano_jogador, dano_aliado, dano_inimigo)

        if adversario["mostrar_vulneravel"]:
            print(f"******{adversario['nome']} -> Vulneravel a {adversario['vulneravel']}*****")
        jogador["score"] += dano_jogador

    mostrar_resultado_batalha(jogador, adversario, aliado)
    if jogador["vida"] > 0:
        print("VOCÊ VENCEU A BATALHA")
        jogador["vida"] = 300.0
        if adversario["dano"] not in jogador["armas"]:
            if random.randrange(2) >= 1:
                print("Ao final da batalha seu inimigo encontra-se em bom estado e você a pega")
                print("Ganhou arma:", retorna_nome_dict_arma(adversario["dano"]))
                jogador["armas"].append(adversario["dano"])
        if "viajando_com" in jogador.keys():
            if "aliado_morreu" not in jogador.keys():
                aliado["vida"] = 320.0
    else:
        print("VOCÊ PERDEU A BATALHA")

    if jogador["vida"] <= 0:
        morreu("", jogador)


def morreu(mensagem_extra, jogador):
    print("Você morreu.", mensagem_extra)
    print(" X X ")
    print("  0  ")
    print(f"SCORE: {jogador['score']}")


def mensagem_batalha3(personagem):
    return f"Antes de entrentar face a face o rei você encontra {personagem}, que foi ignorado antes," \
        f" e ele o desafia para um duelo"


def mensagem_vitoria(jogador):

    print("PARABENS, VOCÊ É O GRANDE GANHADOR")
    print("       ************** ")
    print("       *  ********  * ")
    print("       *  ********  * ")
    print("        ************  ")
    print("          ********    ")
    print("           ******     ")
    print("            ****      ")
    print("             **       ")
    print("           ******     ")
    print(f"        SCORE:{jogador['score']}")


def batalha_final(jogador):
    inimigo = define_personagem_inimigo(None)
    print("Finalmente após tantas dificuldades você se encontra face a face")
    print("Em uma noite com densa nevo, quando derrepende ao longe, você vê")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("                          /\\    /\\   /\\                      ")
    print("                          |            |                         ")
    print("                          -------------                         ")
    print("                          |            |                        ")
    print("                          | --      -- |                        ")
    print("                          |      |     |                        ")
    print("                          |      |     |                        ")
    print("                          |       --   |                        ")
    print("                          |    ______  |                        ")
    print("                          |____________|                        ")
    print(f"                        O REI {inimigo}")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    modificador = modificadores[random.randrange(len(modificadores))]
    batalha(jogador, inimigo, 300.0*jogador["dificuldade"], modificador)
    if jogador["vida"] < 0:
        print(f"Após uma luta ardua contra o rei malévolo {inimigo}")
        return
    mensagem_vitoria(jogador)
    jogador["ganhou"] = True
    return


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


def input_processado(entradas_aceitas, mensagem):
    entrada = ""
    while entrada not in entradas_aceitas:
        entrada = input(mensagem).lower()
        if entrada not in entradas_aceitas:
            print("Digite uma entrada válida")
    return entrada


def item_drop_aleatorio(jogador):
    item_aleatorio = "EVENTO ESPECIAL: você ve um bau e decide abri-lo"
    print(item_aleatorio)
    if random.randrange(8) < 5:
        aleatorio_bau = random.randrange(4, 7)
        adiciona_arma_a_personagem(jogador, aleatorio_bau)
        print(f"RESULTADO: Você achou a arma {chaves[aleatorio_bau]}")
        return True
    else:
        morreu(" Era um monstro, não um baú!!! ", jogador)
        return False


def seletor_de_dificuldade(jogador):
    entradas = ["litoral", "planicie", "montanhas"]
    entrada = input_processado(entradas, "você pode ir pelos caminhos litoral/planicie/montanha: ")
    if entrada == "litoral":
        jogador["dificuldade"] = 1
    if entrada == "planicie":
        jogador["dificuldade"] = 1.25
    if entrada == "montanhas":
        jogador["dificuldade"] = 1.5


def litoral(jogador):
    print("Ao atravessar percorrer a costa você encontra um conhecido seu!!")
    if random.randrange(7) < 3:
        jogador["vida"] += 50
        print("O conhecido lhe dá provisões e um local para descansar. +50 de vida no inicio da próxima batalha")
    else:
        jogador["vida"] -= 15
        print("Durante um periodo de distração enquanto pescam, você pisa em um ouriço." +
              " -15 de vida no inicio da próxima batalha")


def pantano(jogador):
    print("Ao atravessar um pantano na parte central do reino está ocorrendo a temporada de mosquitos!!")
    if random.randrange(12) < 3:
        jogador["vida"] -= 80
        print("Infelizmente você se contrai uma doença. -80 de vida no inicio da próxima batalha")
    else:
        print("Você consegue passar sem contrair nunhuma doença apesar das condições" +
              " nada agradáveis")


def avalanche(jogador):
    print("Ao atravessar as montanhas na parte norte do reino uma avalanche ocore!!")
    if random.randrange(9) < 3:
        jogador["vida"] -= 120
        print("Infelizmente você se fere durante a avalanche. -120 de vida no inicio da próxima batalha")
    else:
        print("Você consegue achar uma fenda nas rochas e consegue se protejer, " +
              "mas perde tempo com essa série de acontecimentos")


def evento_intermediario(jogador):
    if jogador["dificuldade"] == 1:
        litoral(jogador)
    if jogador["dificuldade"] == 1.25:
        pantano(jogador)
    if jogador["dificuldade"] == 1.5:
        avalanche(jogador)


def faz_as_pazes(jogador):
    fez_as_pazes = False
    entrada = input_processado(["conversar", "debochar"], "Antes de duelarem você vai tenta conversar/debochar: ")
    if entrada == "conversar":
        fez_as_pazes = random.randrange(2) > 0
        if not fez_as_pazes:
            print(f"Argumentar com {jogador['ignorou']} falhou, a batalha irá ocorrer")
        else:
            aliado = jogador["ignorou"]
            jogador["viajando_com"] = aliado
        return fez_as_pazes
    else:
        print(f"Isso só fez a situação ficar pior {jogador['ignorou']} agora está furioso")
        return 2 * jogador["dificuldade"]


def jogo(nome):

    iniciar_variaveis()
    jogador = {"nome": nome, "vida": 350.0, "dano": {"dano": 5, "acc": 10, "crit": 100}, "score": 0, "armas": [],
               "vulneravel": gera_vulnerabilidade(), "ganhou": False}

    print("O mundo foi devastado e agora é governardo pelo Rei Malvado. Resta a você salvar o reino...")
    print("Assim como no ditado todos os caminhos levam a capital do reino," +
          " com seus proprios desafios para aqueles que os percorrem.")

    seletor_de_dificuldade(jogador)

    item = random.randrange(len(personagens))

    print(f"O personagem {personagens[item]} se aproxima de você e pede se está indo enfrentar o Rei Malvado!")

    escolha = input_processado(["nao", "sim"], "Você vai dizer sim/nao? ")

    if escolha == "sim":
        jogador["viajando_com"] = personagens[item]
        personagens_enfrentaveis.remove(personagens[item])
    else:
        jogador["ignorou"] = personagens[item]

    escolha_1 = "Ao se aproximar de um mercador você ve que ele esta vendendo armas."
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
            armas_indices.append(str(i+1))
            i += 1

    if selecao_evento == 1:
        print(escolha_1)
        pergunta = int(input_processado(armas_indices, pergunta_1 + str(arma_mercador) + " Escolha pelo numero" +
                                        " correspondente: "))

        if pergunta in range(1, limite_lista+1):
            adiciona_arma_a_personagem(jogador, pergunta - 1)
    else:
        if not item_drop_aleatorio(jogador):
            return jogador

    inimigo = define_personagem_inimigo(None)
    print(batalha_1, inimigo)
    if not decisao_de_fugir():
        batalha(jogador, inimigo, 200*jogador["dificuldade"], "")
        if jogador["vida"] <= 0:
            return jogador

    evento_intermediario(jogador)
    inimigo = define_personagem_inimigo(None)
    print(batalha_2, inimigo)
    if not decisao_de_fugir():
        batalha(jogador, inimigo, 240*jogador["dificuldade"], "")
        if jogador["vida"] <= 0:
            return jogador

    if "viajando_com" not in jogador.keys():
        inimigo = define_personagem_inimigo(jogador["ignorou"])
        print(mensagem_batalha3(inimigo))
        if not decisao_de_fugir():
            resultado_evento = faz_as_pazes(jogador)
            if type(resultado_evento) is bool:
                if not resultado_evento:
                    batalha(jogador, inimigo, 250*jogador["dificuldade"], "")
                    if jogador["vida"] <= 0:
                        return jogador
            else:
                batalha(jogador, inimigo, 250*jogador["dificuldade"]*resultado_evento, "")
                if jogador["vida"] <= 0:
                    return jogador

    if not item_drop_aleatorio(jogador):
        return jogador
    batalha_final(jogador)

    return jogador


def tenta_criar_arquivo_scores():
    try:
        arquivo = open("../resources/scores.txt", "x")
        arquivo.close()
    except FileExistsError:
        pass


def menu():
    tenta_criar_arquivo_scores()
    game_loop = True
    while game_loop:
        print("****Bem vindo ao RPG da Avaliação****")

        print("*********Escolha uma opção!**********")

        print("I - Iniciar\nP - Pontuações\nS - Sair")

        opcao = input_processado(["i", "s", "p"], "Opção: ")

        if opcao == "s":
            game_loop = False
        elif opcao == "p":
            mostra_scores(le_scores_arquivo())
        else:
            nome = input("Digite seu nome: ")
            print("Vamos começar a aventura,", nome + "!")

            jogador = jogo(nome)
            grava_resultado_arquivo(jogador)

            game_loop = (input_processado(["sim", "nao"], "Deseja jogar novamente? sim/nao: ") == "sim")


menu()
