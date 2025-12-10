import file_reader as fr 
import bnf as b

print("Iniciando a leitura do arquivo...")
lista_producoes = fr.file_reader('exemplo1.txt')

if lista_producoes == None:
    print("Nenhuma linha foi lida do arquivo.")

print(f"{len(lista_producoes)} linhas lidas do arquivo.")
print("Construindo a BNF...")
bnf = b.constructor(lista_producoes)
print(bnf)

afn = b.bnf_to_afn(bnf)
print("BNF convertida para AFN:")
print(afn)