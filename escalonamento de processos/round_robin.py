# Algoritmo de escalonamento Round Robin
# Input: ID, nome, arrival time, i/o ou cpu bound, burst time
# Informações de um processo: [todas as listadas acima]

lista_processos = []

def round_robin(lista_processos, quantum_time):
    t = 0 # Tempo total desde o início do escalonamento até o fim da execução de todos os processos
    gantt = [] # Lista para exibição da ordem de execução dos processos
    completo = {} # Dicionário para conter os valores de turnaround e de espera de cada processo

    # Ordenando a lista de processos com base no arrival de cada processo
    lista_processos = sorted(lista_processos, key=lambda x: x[2])

    burst_times = {} # Dicionário para guardar os burst times de um processo
    for p in lista_processos:
        id = p[0]
        burst_time = p[4]
        burst_times[id] = burst_time

    while lista_processos != []: # Loop vai rodar até que a lista esteja vazia
        pronto = [] # Lista de processos prontos
        for p in lista_processos:
             at = p[2] # Arrival time
             if p[2] <= t:
                pronto.append(p) # Quer dizer que ele ainda não teve vez na execução, ou seja, vai pra lista de pronto
        # Caso não tenha nenhum processo na fila de pronto
        if pronto == []:
            gantt.append("Inativo")
            t += 1 # Tempo (ms) é iterado
            continue
        else:
            print('Lista de processos prontos: ')
            print(pronto)
            print('\n')
            processo = pronto[0] # Sempre pegando o primeiro processo da lista de pronto por causa da rotatividade
            # Vez de execução desse processo, pegando seu ID
            gantt.append(processo[0])
            print('Em execução: ')
            print(gantt) # Mostra qual processo está executando atualmente
            print('\n')
            # Remoção dele da lista de processos em espera
            lista_processos.remove(processo)
            print('Processos em espera: ')
            print(lista_processos) # Lista de processos em espera
            print('\n')
            # Atualização do seu burst time
            burst_rest = processo[4]
            
            if burst_rest <= quantum_time: # Isso significa que nessa execução o processo já pode finalizar
                t += burst_rest # Então o t é incrementado com o burst time restante

                completion_time = t # Completion time = t
                id = processo[0] # ID do processo
                arrival_time = processo[2] # arrival time
                burst_time = burst_times[id]
                turnaround_time = completion_time - arrival_time
                waiting_time = turnaround_time - burst_time
                completo[processo[0]] = [completion_time, turnaround_time, waiting_time] # Completion time é t no

                continue
            else: 
                t += quantum_time
                processo[4] -= quantum_time # O burst time é decrementado pelo quantum time
                lista_processos.append(processo) # E o processo retorna à lista de processos 

        
    print('Tempo de completude, turnaround e waiting time dos processos (em ms) respectivamente: ')
    print(completo)
    print('\n')
    # Calculando tempo médio de espera
    valores = [v[2] for v in completo.values()]
    media_waiting = sum(valores) / len(valores)

    # Calculando tempo médio de turnaround
    valores = [v[1] for v in completo.values()]
    media_turnaround = sum(valores) / len(valores)

    print('Tempo médio de espera:')
    print(round(media_waiting, 2))
    print('\n')
    print('Tempo médio de turnaround:')
    print(round(media_turnaround, 2))


while True:
    processo = []
    campos = ["ID: ", "Nome: ", "Arrival time: ", "I/O ou CPU bound (io/cpu): ", "Burst time: "]
    
    for i, texto in enumerate(campos):
        entrada = input(texto)
        if i == 2 or i == 4:  # Verifica se é a terceira ou última entrada
            entrada = int(entrada)  # Converte para inteiro
        processo.append(entrada)
    
    lista_processos.append(processo)
    
    continuar = input("Deseja inserir outro processo? (s/n): ")
    if continuar.lower() == 'n':
        quantum_time = int(input("Insira o quantum time: "))
        break


print('\n')
round_robin(lista_processos, quantum_time)