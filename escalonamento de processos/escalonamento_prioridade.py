# Algoritmo de escalonamento por prioridade
# A prioridade será considerada como Arrival time

def priority_scheduling(processos, quantum_time):
    tempo_total = 0  # Tempo total desde o início do escalonamento até o fim da execução de todos os processos
    gantt = []  # Lista para ordem de execução
    completo = {}  # Dicionário para conter os valores de turnaround e de espera de cada processo

    while processos:
        processos_prontos = [processo for processo in processos if processo[2] <= tempo_total]  # Filtra os processos prontos
        if not processos_prontos:
            gantt.append("Inativo")
            tempo_total += 1
            continue

        # Seleciona o processo com a maior prioridade
        processo_atual = max(processos_prontos, key=lambda x: x[2])

        gantt.append(processo_atual[0])  # Adiciona o processo ao Gantt chart

        if processo_atual[4] <= quantum_time:
            tempo_total += processo_atual[4]
            completion_time = tempo_total
            arrival_time = processo_atual[2]
            turnaround_time = completion_time - arrival_time
            waiting_time = turnaround_time - processo_atual[4]
            completo[processo_atual[0]] = [completion_time, turnaround_time, waiting_time]
            processos.remove(processo_atual)
        else:
            tempo_total += quantum_time
            processo_atual[4] -= quantum_time
            processos.remove(processo_atual)
            processos.append(processo_atual)

    # Exibição dos resultados
    print('Tempo de completude, turnaround e waiting time dos processos (em ms) respectivamente: ')
    print(completo)

    valores_espera = [v[2] for v in completo.values()]
    media_espera = sum(valores_espera) / len(valores_espera)
    print('Tempo médio de espera:', round(media_espera, 2))

    valores_turnaround = [v[1] for v in completo.values()]
    media_turnaround = sum(valores_turnaround) / len(valores_turnaround)
    print('Tempo médio de turnaround:', round(media_turnaround, 2))


# Entrada dos processos e quantum time
processos = []
while True:
    processo = []
    campos = ["ID: ", "Nome: ", "Prioridade: ", "Tipo (I/O ou CPU bound): ", "Burst time: "]
    for i, texto in enumerate(campos):
        entrada = input(texto)
        if i == 2 or i == 4:
            entrada = int(entrada)
        processo.append(entrada)

    processos.append(processo)

    continuar = input("Deseja inserir outro processo? (s/n): ")
    if continuar.lower() == 'n':
        quantum_time = int(input("Insira o quantum time: "))
        break

print('\n')
priority_scheduling(processos, quantum_time)