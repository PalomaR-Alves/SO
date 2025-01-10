import time

def scan(requests, cabeca, min_bloco, max_bloco, direcao):
    sequencia_blocos = []
    deslocamento_total = 0
    esquerda = []
    direita = []
    request_min = min(requests)
    cabeca_inicial = cabeca

    # separa as requisições nas listas de esquerda e direita da cabeça
    for request in requests:
        if request < cabeca and request >= min_bloco:
            esquerda.append(request)
        elif request > cabeca and request <= max_bloco:
            direita.append(request)

    esquerda.sort()
    direita.sort()

    print('\n')
    print('Blocos a esquerda: ', esquerda)
    print('Blocos a direita: ', direita)
    print('\n')

    # movimentacao da cabeça
    if direcao == "esquerda": # se começar pela esquerda
        # começa do maior index, itera de 1 em 1 de forma descrescente e para quando chega no index 0
        for i in range(len(esquerda) - 1, -1, -1):
            destino = esquerda[i]
            deslocamento = abs(destino - cabeca)
            sequencia_blocos.append(destino)
            print(f"Movendo de {cabeca} para {destino}, tempo de seek parcial: {deslocamento} u.t.")
            time.sleep(3)
            cabeca = destino

        for i in range(len(direita)):
            destino = direita[i]
            deslocamento = abs(destino - cabeca)
            sequencia_blocos.append(destino)
            print(f"Movendo de {cabeca} para {destino}, tempo de seek parcial: {deslocamento} u.t.")
            time.sleep(3)
            cabeca = destino

    elif direcao == "direita": # se começar pela direita
        for i in range(len(direita)):
            destino = direita[i]
            deslocamento = abs(destino - cabeca)
            sequencia_blocos.append(destino)
            print(f"Movendo de {cabeca} para {destino}, tempo de seek parcial: {deslocamento} u.t.")
            time.sleep(3)
            cabeca = destino

        # percorre a esquerda
        for i in range(len(esquerda) - 1, -1, -1):
            destino = esquerda[i]
            deslocamento = abs(destino - cabeca)
            sequencia_blocos.append(destino)
            print(f"Movendo de {cabeca} para {destino}, tempo de seek parcial: {deslocamento} u.t.")
            time.sleep(3)
            cabeca = destino

    print('\n')
    print(f"Tempo de seek total: {(max_bloco-cabeca_inicial) + (max_bloco-request_min)} u.t.")
    return deslocamento_total, sequencia_blocos

# exemplo de entrada por usuário
min_bloco = int(input("Informe o bloco mínimo do disco: "))
max_bloco = int(input("Informe o bloco máximo do disco: "))
cabeca = int(input("Informe a posição inicial da cabeça de leitura/gravação: "))
requests_input = input("Informe a ordem dos blocos a serem visitados (separados por vírgula): ")
direcao = input("Informe a direção inicial (esquerda/direita): ").strip().lower()

requests = [int(x.strip()) for x in requests_input.split(',')]

deslocamento_total, sequencia_blocos = scan(requests, cabeca, min_bloco, max_bloco, direcao)

print("Sequência de blocos:", sequencia_blocos)
