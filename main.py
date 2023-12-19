def ler_arquivo_ppm(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

        # Verifica se o arquivo é do tipo P2
        if linhas[0].strip() != 'P2':
            print("Formato de arquivo inválido. Deve ser do tipo P2.")
            return None

        # Obtém largura, altura e valor máximo do pixel
        largura, altura = map(int, linhas[1].split())
        valor_maximo = int(linhas[2])

        # Lê os valores dos pixels
        matriz = []
        for linha in linhas[3:]:
            valores = linha.split()
            matriz.append([int(valor) for valor in valores])
            
        print(matriz)
        return largura, altura, valor_maximo, matriz


def salvar_arquivo_ppm(nome_arquivo, largura, altura, valor_maximo, matriz):
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write("P2\n")
        arquivo.write(f"{largura} {altura}\n")
        arquivo.write(f"{valor_maximo}\n")

        for linha in matriz:
            linha_str = ' '.join(str(valor) for valor in linha)
            arquivo.write(f"{linha_str}\n")


# Lê o arquivo .ppm P2
largura, altura, valor_maximo, matriz = ler_arquivo_ppm('exemplo.ppm')

# Realiza operações na matriz se necessário

# Salva a matriz em um novo arquivo .ppm P2
salvar_arquivo_ppm('nova_imagem.ppm', largura, altura, valor_maximo, matriz)
