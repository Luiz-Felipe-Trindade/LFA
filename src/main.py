import file_reader as fr 

print("Iniciando a leitura do arquivo...")
linhas = fr.file_reader('exemplo1.txt')
print("Linhas do arquivo lidas com sucesso:")
for linha in linhas:
    print(linha)