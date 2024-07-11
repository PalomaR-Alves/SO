# Alocação de memória com partições fixas
# Looping de duração de processos não foi incluído, considerando que a duração é infinita
# Código foi feito considerando que nunca serão criados processos grandes o suficiente para não caber em nenhuma partição
import time

lista_processos = [] # lista de processos a serem alocados
lista_partições = [] # lista para tamanhos das partições
lista_alocação_processos = []
partições_alocadas = []
memoria_virtual = [] # lista para processos em memoria virtual
algoritmo = ""
not_frag_externa = False
soma_partições = 0
frag_interna = 0
melhor_partição = 0
menor_frag_interna = float("inf")
indice = 0

def print_state():
    print("Processos: " + str(lista_processos))
    print("Alocação de processos: " + str(lista_alocação_processos))
    print("Partições alocadas: " + str(partições_alocadas))
    print("Memória virtual: " + str(memoria_virtual))
    print("\n")

def valor_presente(lista, chave, valor):
    for dic in lista:
        if dic.get(chave) == valor:
            return True
    return False

def obter_indice(lista, chave, valor):
    for indice, dic in lista:
        if dic.get(chave) == valor:
            return indice

def mem_allocation(lista_processos):
    global algoritmo, lista_partições, lista_alocação_processos, partições_alocadas, memoria_virtual, menor_frag_interna
  # os processos serão alocados em ordem FIFO usando o algoritmo escolhido
    if algoritmo == "first-fit":
        for i in range(len(lista_processos)):
            not_frag_externa = False # variável setada para que frag externa possa ser registrada
            for j in range(len(lista_partições)): # percorrer lista de partições até achar uma que encaixe
                # se o tamanho do processo for <= ao tam da partição e ela estiver livre ele é alocado
                if lista_processos[i][2] <= lista_partições[j] and (j not in partições_alocadas):
                    lista_alocação_processos.append({"Partição": j,
                                                "PID": lista_processos[i][0], 
                                                "Tamanho": lista_processos[i][2], 
                                                "Frag. Interna": False if (lista_processos[i][2] - lista_partições[j]) == 0 else True,
                                                })
                        
                    partições_alocadas.append(j) # adiciona a partição na lista
                    not_frag_externa = True
                    break
            
            print_state() # printar estados das listas

            # se o processo não foi alocado depois de percorrida a lista de partições houve frag externa
            if not not_frag_externa:
                print("Frag. Externa: " + str(lista_processos[i]))
                # realizar swap in de um processo alocado para alocar no lugar o que sofreu frag externa
                for n in range(len(lista_alocação_processos)):
                    # se o processo couber na partição (já ocupada pois tá na lista_alocação_processos) na
                    # posição n da lista_partições, ele vai pra lá

                    if lista_partições[(lista_alocação_processos[n]["Partição"])] >= lista_processos[i][2]:
                        # swap in no processo anterior
                        memoria_virtual.append(lista_alocação_processos[n].copy())

                        # mudar informações para a do processo novo alocado
                        lista_alocação_processos[n]["PID"] = lista_processos[i][0]
                        lista_alocação_processos[n]["Tamanho"] = lista_processos[i][2]
                        lista_alocação_processos[n]["Frag. Interna"] = False if (lista_processos[i][2] - lista_partições[(lista_alocação_processos[n]["Partição"]) - 1]) == 0 else True
                        print_state() # printar estados das listas
                        break
                        
            time.sleep(5)

    elif algoritmo == "best-fit":
        for i in range(len(lista_processos)):
            menor_frag_interna = float('inf')
            melhor_partição = -1
            for j in range(len(lista_partições)):  # para fazer comparações quanto à fragmentação interna para achar a melhor partição
                if lista_processos[i][2] <= lista_partições[j] and (j not in partições_alocadas):
                    frag_interna = lista_partições[j] - lista_processos[i][2] # essa subtração não pode ser invertida
                    if frag_interna < menor_frag_interna:
                        menor_frag_interna = frag_interna
                        melhor_partição = j

            if melhor_partição != -1:  # encontrou uma partição adequada
                lista_alocação_processos.append({"Partição": melhor_partição,
                                                 "PID": lista_processos[i][0],
                                                 "Tamanho": lista_processos[i][2],
                                                 "Frag. Interna": False if menor_frag_interna == 0 else True,
                                                 })
                partições_alocadas.append(melhor_partição)
            else:
                print("Frag. Externa: " + str(lista_processos[i]))
                for n in range(len(lista_alocação_processos)):
                    if lista_partições[lista_alocação_processos[n]["Partição"]] >= lista_processos[i][2]:
                        memoria_virtual.append(lista_alocação_processos[n].copy())

                        lista_alocação_processos[n]["PID"] = lista_processos[i][0]
                        lista_alocação_processos[n]["Tamanho"] = lista_processos[i][2]
                        lista_alocação_processos[n]["Frag. Interna"] = False if (lista_partições[lista_alocação_processos[n]["Partição"]] - lista_processos[i][2]) == 0 else True
                        print_state()
                        break

                    if (n + 1 == len(lista_alocação_processos)):  # ao chegar no fim da lista_alocação_processos o processo é incluído na melhor posição
                        indice = obter_indice(lista_alocação_processos, "Partição", melhor_partição)
                        memoria_virtual.append(lista_alocação_processos[indice].copy())

                        lista_alocação_processos[indice]["PID"] = lista_processos[i][0]
                        lista_alocação_processos[indice]["Tamanho"] = lista_processos[i][2]
                        lista_alocação_processos[indice]["Frag. Interna"] = False if menor_frag_interna == 0 else True
                        print("\n")
                        print_state()

            print_state()
            time.sleep(5)


    else:
        print("O algoritmo inserido não é válido!")


while True:
    processo = []
    campos = ["PID: ", "Nome: ", "Tamanho (em MB): "]
    print("Insira processos para execução ")

    for i, texto in enumerate(campos):
        entrada = input(texto)
        if i == 2: 
            entrada = int(entrada)  # converte para inteiro
        processo.append(entrada)
    
    lista_processos.append(processo)
    
    continuar = input("Deseja inserir outro processo? (s/n): ")
    if continuar.lower() == 'n':
        entrada = input("\nInsira o tamanho da memória: ")
        entrada = int(entrada)
        tam_mem = entrada

        for i in range(len(lista_processos)):
            entrada = input("\ninsira o tamanho da partição %.0f: " % (i+1))
            entrada = int(entrada)
            lista_partições.append(entrada)
            soma_partições = soma_partições + entrada
            print('Soma total de partições: %.0f de %.0f' % (soma_partições, tam_mem))

        algoritmo = input("\nInsira o algoritmo de alocação (best-fit/first-fit): ")
        break


print('\n')
mem_allocation(lista_processos)