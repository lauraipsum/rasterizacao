def ler_arquivo_ppm(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

        # verifica se é P2
        if linhas[0].strip() != 'P2':
            print("Formato de arquivo inválido. Deve ser do tipo P2.")
            return None

        # Obtém largura, altura e valor máximo do pixel
        largura, altura = map(int, linhas[1].split())
        valor_maximo = int(linhas[2])

        # le o valor de cada pixel da img
        matriz = []
        for linha in linhas[3:]:
            valores = linha.split()
            matriz.append([int(valor) for valor in valores])
            
        #print(matriz)
        return largura, altura, valor_maximo, matriz

def salvar_arquivo_ppm(nome_arquivo, largura, altura, valor_maximo, matriz):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write("P2\n")
        arquivo.write(f"{largura} {altura}\n")
        arquivo.write(f"{valor_maximo}\n")

        for linha in matriz:
            linha_str = ' '.join(str(valor) for valor in linha)
            arquivo.write(f"{linha_str}\n")

def negativo(nome_arquivo):
    largura, altura, valor_maximo, matriz = ler_arquivo_ppm('exemplo.ppm') 
    matriz_negativo = [ 
                       [valor_maximo - pixel # s = (L-1) - r , transformacao negativa
                        for pixel in linha] 
                       for linha in matriz  
                       ]       
    
    # Salva a matriz negativa em um novo arquivo .ppm
    novo_nome_arquivo = nome_arquivo.replace('.ppm', '_negativo.ppm')
    salvar_arquivo_ppm(novo_nome_arquivo, largura, altura, valor_maximo, matriz_negativo)
    
def threshold(nome_arquivo, limite):
    largura, altura, valor_maximo, matriz = ler_arquivo_ppm('exemplo.ppm') 
    
    matriz_threshold = [
                        [0 if pixel <= limite else valor_maximo 
                         for pixel in linha] 
                        for linha in matriz
                        ]

    novo_nome_arquivo = nome_arquivo.replace('.ppm', f'_threshold_{limite}.ppm')
    salvar_arquivo_ppm(novo_nome_arquivo, largura, altura, valor_maximo, matriz_threshold)



negativo('exemplo.ppm')
threshold('exemplo.ppm', limite=125)