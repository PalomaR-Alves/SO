# Definindo tamanhos e blocos
tam_mem = 100  # Tamanho total da memória em MB
tam_bloco = 2  # Tamanho de cada bloco em MB
num_blocos = tam_mem // tam_bloco  # Número total de blocos

class Diretorio:
    def __init__(self, nome):
        self.nome = nome
        self.filhos = []  # Lista de filhos (arquivos e subdiretórios)

class Arquivo:
    def __init__(self, nome, tamanho):
        self.nome = nome
        self.tamanho = tamanho

class Particao:
    def __init__(self, nome, tam_particao, bloco):
        self.nome = nome
        self.tam_particao = tam_particao
        self.bloco = bloco
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.primeiro = None

    def alocarArquivo(self, nome, tam_particao, bloco):
        nova_particao = Particao(nome, tam_particao, bloco)
        if self.primeiro is None:
            self.primeiro = nova_particao
        else:
            atual = self.primeiro
            while atual.proximo is not None:
                atual = atual.proximo
            atual.proximo = nova_particao

    def imprimir(self):
        atual = self.primeiro
        while atual is not None:
            print(f"Nome: {atual.nome}, Tamanho: {atual.tam_particao}MB, Bloco: {atual.bloco}")
            atual = atual.proximo

class SistemaArquivos:
    def __init__(self):
        self.diretórios = {"raiz": Diretorio("raiz")}
        self.blocos_ocupados = [False] * num_blocos
        self.lista_encadeada = ListaEncadeada()

    def criar_diretorio(self, nome):
        if nome in self.diretórios:
            return f"Diretório {nome} já existe."
        self.diretórios[nome] = Diretorio(nome)
        print(f"Diretório {nome} criado.")

    def excluir_diretorio(self, nome):
        if nome not in self.diretórios:
            return f"Diretório {nome} não existe."
        if nome == "raiz":
            return "Não é possível excluir o diretório raiz."
        del self.diretórios[nome]
        print(f"Diretório {nome} excluído.")

    def criar_arquivo(self, dir_nome, nome_arquivo, tamanho):
        if dir_nome not in self.diretórios:
            return f"Diretório {dir_nome} não existe."
        if any(arq.nome == nome_arquivo for arq in self.diretórios[dir_nome].filhos):
            return f"Arquivo {nome_arquivo} já existe no diretório {dir_nome}."

        if tamanho > tam_mem:
            return "Erro: Tamanho do arquivo maior que a memória disponível (fragmentação externa)."

        partes = []
        restante = tamanho
        # bloco = -1

        while restante > 0:
            bloco = self.procurar_bloco_livre()
            if bloco == -1:
                return "Erro: Não há blocos livres disponíveis."
            
            tam_particao = min(tam_bloco, restante) # para caso o tamanho restante seja < tam_bloco, frag interna
            partes.append((nome_arquivo, tam_particao, bloco))
            restante -= tam_particao # o tamanho restante do arquivo a ser alocado é decrementado

            nome, tam_particao, bloco = partes[-1]  # Acessa a última parte adicionada
            self.lista_encadeada.alocarArquivo(nome, tam_particao, bloco)
            self.blocos_ocupados[bloco] = True

        self.diretórios[dir_nome].filhos.append(Arquivo(nome_arquivo, tamanho))
        print(f"Arquivo {nome_arquivo} criado no diretório {dir_nome}.")

    def excluir_arquivo(self, dir_nome, nome_arquivo):
        if dir_nome not in self.diretórios:
            print(f"Diretório {dir_nome} não existe.")
            return
        arquivo = next((arq for arq in self.diretórios[dir_nome].filhos if arq.nome == nome_arquivo), None)
        if not arquivo:
            print(f"Arquivo {nome_arquivo} não encontrado no diretório {dir_nome}.")
            return

        self.diretórios[dir_nome].filhos.remove(arquivo)
        self.desalocar_arquivo(nome_arquivo)
        print(f"Arquivo {nome_arquivo} excluído do diretório {dir_nome}.")

    def procurar_bloco_livre(self):
        for i in range(num_blocos):
            if not self.blocos_ocupados[i]: # se false = livre, retorna o índice
                return i
        return -1 # nenhum bloco livre

    def desalocar_arquivo(self, nome_arquivo):
        atual = self.lista_encadeada.primeiro
        while atual is not None:
            if atual.nome == nome_arquivo:
                self.blocos_ocupados[atual.bloco] = False
            atual = atual.proximo

    def listar_diretorio(self, nome):
        if nome not in self.diretórios:
            print(f"Diretório {nome} não existe.")
            return
        diretorio = self.diretórios[nome]
        print(f"Conteúdo do diretório {nome}:")
        for filho in diretorio.filhos:
            print(f"- {filho.nome} ({filho.tamanho}MB)")

    def mostrar_alocacao(self):
        print("Alocação atual:")
        self.lista_encadeada.imprimir()

    def verificar_fragmentacao(self):
        fragmentacao_interna = 0
        bloco_atual = None
        bloco_livre = False

        atual = self.lista_encadeada.primeiro
        while atual is not None:
            if bloco_atual is None or bloco_atual != atual.bloco:
                bloco_atual = atual.bloco
                bloco_livre = False
            if bloco_livre:
                fragmentacao_interna += tam_bloco - atual.tam_particao
            bloco_livre = True
            atual = atual.proximo

        print(f"Fragmentação interna: {fragmentacao_interna}MB")

# Exemplo de uso
sistema = SistemaArquivos()
sistema.criar_diretorio("docs")
sistema.criar_arquivo("docs", "file1.txt", 5)
sistema.criar_arquivo("docs", "file2.txt", 8)
sistema.listar_diretorio("docs")
sistema.mostrar_alocacao()
sistema.verificar_fragmentacao()
# sistema.excluir_arquivo("docs", "file1.txt")
# sistema.listar_diretorio("docs")
# sistema.mostrar_alocacao()
# sistema.verificar_fragmentacao()
# sistema.excluir_diretorio("docs")