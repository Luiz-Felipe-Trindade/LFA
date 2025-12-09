import file_reader as fr 
import bnf

print("Iniciando a leitura do arquivo...")
lista_producoes = fr.file_reader('exemplo1.txt')

if lista_producoes == None:
    print("Nenhuma linha foi lida do arquivo.")
else:
    print(f"{len(lista_producoes)} linhas lidas do arquivo.")
    print("Construindo a BNF...")
    bnf = bnf.constructor(lista_producoes)
    print(bnf)