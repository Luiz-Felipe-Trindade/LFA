import pandas as pd
import graphviz
import sys
from graphviz import Source


gramatica_texto= """
<A> ::= a<A> | a<B> | b<A>
<B> ::= a<C>
<C> ::= b<D>
<D> ::= a<D> | b<D> | ε
"""

# Pega o arquivo de gramática
#FILE_PATH = 'src\inputs\exemplo1.txt'
#try:
#    with open(FILE_PATH, 'r', encoding='utf-8') as arquivo:
#        gramatica_texto = arquivo.read()
#except FileNotFoundError:
#    print(f"Erro: arquivo '{FILE_PATH}' não encontrado!")
#    sys.exit(1)

# 2. (BNF -> AFN)
transitions = {}
# initial_state = 'A'
initial_state = input("Digite o estado inicial da gramática (ex: A): ").strip()
final_states = set()
states = set()
input_symbols = set()

# Para cada linha da gramática
for linha in gramatica_texto.strip().split('\n'):
    # Divide a linha de produção em esquerda e direita do simbolo '::='
    esquerda, direita = linha.split('::=')
    # Remove caracteres desnecessários
    estado_origem = esquerda.strip().replace('<', '').replace('>', '')
    states.add(estado_origem)  
    # Divide as produções em uma lista
    producoes = [p.strip() for p in direita.split('|')]
    
    # Se o estado de origem não estiver no dicionário de transições, inicializa.
    if estado_origem not in transitions:
        transitions[estado_origem] = {}
        
    # Para cada produção, cria as transições
    for prod in producoes:   
        # Verifica se a produção é ε (episolon)
        if prod == 'ε':
            final_states.add(estado_origem)
            continue          
        # Extrai terminal e não terminal removendo os caractéres inuteis (ex: a<A> -> 'a', 'A')
        simbolo = prod[0]
        prox_estado = prod[1:].replace('<', '').replace('>', '') if len(prod) > 1 else 'FIM' 
        # Adiciona o terminal a lista de simbolos de entrada
        input_symbols.add(simbolo)
        # Adiciona o nao terminal aos estados conhecidos
        states.add(prox_estado)
        # se o terminal não estiver no dicionário de transições do estado de origem, inicializa-o.
        if simbolo not in transitions[estado_origem]:
            transitions[estado_origem][simbolo] = set()
        transitions[estado_origem][simbolo].add(prox_estado)
        print(f"Transição: {estado_origem} --{simbolo}--> {prox_estado}")        
print("\n--- Transições do AFN ---")
print(transitions)

# 3. Conversão AFN -> AFD (Determinização)

# Inicializa estruturas para o autômato determinístico (AFD): 
#transições, estado inicial, lista de estados, estados finais, fila de processamento e estados já processados.
afd_transitions = {}
afd_initial = frozenset([initial_state])
afd_states = [afd_initial]
afd_final_states = set()
queue = [afd_initial]
processed = set()

# Processa cada conjunto de estados na fila até que a fila esteja vazia.
while queue:
    # Pega o próximo conjunto de estados da fila
    current_set = queue.pop(0)
    # Converte o conjunto atual para uma tupla ordenada (para uso como chave)
    current_tuple = tuple(sorted(list(current_set)))
    # Se já foi processado, pula para o próximo loop
    if current_tuple in processed:
        continue
    # Sinaliza como processado e continua o loop atual
    processed.add(current_tuple)
    # Verifica se é estado final (se contém algum estado final do AFN) e adiciona aos estados finais do AFD
    if not current_set.isdisjoint(final_states):
        afd_final_states.add(current_tuple)
    # Inicializa o dicionário de transições para o estado atual
    afd_transitions[current_tuple] = {}
    # Para cada símbolo de entrada
    for simbolo in sorted(list(input_symbols)):
        # define o próximo conjunto de estados como vazio
        next_set = set()
        # Para cada estado no conjunto atual
        for sub_state in current_set:
            # Verifica se há transições para o símbolo atual
            if sub_state in transitions and simbolo in transitions[sub_state]:
                # Adiciona os estados de destino ao próximo conjunto
                next_set.update(transitions[sub_state][simbolo])
        # Se houver estados de destino
        if next_set:
            # Converte o próximo conjunto para uma tupla ordenada
            next_tuple = tuple(sorted(list(next_set)))
            # Adiciona a transição ao dicionário de transições do AFD
            afd_transitions[current_tuple][simbolo] = next_tuple
            # Se o próximo conjunto ainda não foi adicionado à lista de estados do AFD, adiciona-o e enfileira para processamento
            if next_tuple not in [tuple(sorted(list(s))) for s in afd_states]:
                afd_states.append(next_set)
                queue.append(next_set)

# 4. Preparar Tabela (DataFrame)
tabela_dados = []
nome_estados = {tuple(sorted(list(s))): f"q{i}" for i, s in enumerate(afd_states)}

for estado_set in afd_states:
    estado_tuple = tuple(sorted(list(estado_set)))
    nome = nome_estados[estado_tuple]
    
    # Marcadores
    tipo = []
    if estado_tuple == tuple(sorted(list(afd_initial))): tipo.append("INICIAL")
    if estado_tuple in afd_final_states: tipo.append("FINAL")
    tipo_str = " / ".join(tipo) if tipo else "-"
    
    linha = {'Estado': nome, 'Composição Original': str(estado_tuple), 'Tipo': tipo_str}
    
    for simbolo in sorted(list(input_symbols)):
        destino = afd_transitions.get(estado_tuple, {}).get(simbolo)
        linha[simbolo] = nome_estados.get(destino, "-") if destino else "-"
    
    tabela_dados.append(linha)

df_resultado = pd.DataFrame(tabela_dados)

# 5. Gerar Gráfico (Graphviz)
dot = graphviz.Digraph(comment='AFD Resultante')
dot.attr(rankdir='LR')

for estado_set in afd_states:
    estado_tuple = tuple(sorted(list(estado_set)))
    nome = nome_estados[estado_tuple]
    
    # Estilo dos nós
    shape = 'doublecircle' if estado_tuple in afd_final_states else 'circle'
    if estado_tuple == tuple(sorted(list(afd_initial))):
        dot.node('start', '', shape='none')
        dot.edge('start', nome)
    
    dot.node(nome, nome, shape=shape)

# Arestas
for origem_tuple, trans in afd_transitions.items():
    origem_nome = nome_estados[origem_tuple]
    for simbolo, destino_tuple in trans.items():
        destino_nome = nome_estados[destino_tuple]
        dot.edge(origem_nome, destino_nome, label=simbolo)

# Exibindo resultados
print("\n--- Tabela de Transições do AFD ---")
# Primeira parte: Estado e Composição Original
print("Estado  Composição Original")
for linha in tabela_dados:
    print(f"{linha['Estado']:>6} {linha['Composição Original']:>20}")

print("\n  Tipo  a  b")
for linha in tabela_dados:
    print(f"{linha['Tipo']:>7} {linha['a']:>2} {linha['b']:>2}")

print("\n--- CÓDIGO DO GRÁFICO (Copie o texto abaixo) ---")
# Em vez de dot.render, usamos print(dot.source) para evitar o erro do executável
print(dot.source)
Source(dot.source) # Isso exibirá o gráfico diretamente no Jupyter Notebook ou ambiente compatível