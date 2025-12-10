import pandas as pd
import graphviz
import sys
from graphviz import Source

# Pega o arquivo de gramática
try:
    with open('gramatica.txt', 'r', encoding='utf-8') as arquivo:
        gramatica_texto = arquivo.read()
except FileNotFoundError:
    print("Erro: arquivo 'gramatica.txt' não encontrado!")
    sys.exit(1)


# 2. Parser da Gramática (BNF -> NFA)
transitions = {}
# initial_state = 'A'
initial_state = input("Digite o estado inicial da gramática (ex: A): ").strip()
final_states = set()
states = set()
input_symbols = set()

for linha in gramatica_texto.strip().split('\n'):
    esquerda, direita = linha.split('::=')
    estado_origem = esquerda.strip().replace('<', '').replace('>', '')
    states.add(estado_origem)
    
    producoes = [p.strip() for p in direita.split('|')]
    
    if estado_origem not in transitions:
        transitions[estado_origem] = {}
        
    for prod in producoes:
        if prod == 'ε':
            final_states.add(estado_origem)
            continue
            
        # Extrai terminal e não terminal (ex: a<A> -> 'a', 'A')
        simbolo = prod[0]
        prox_estado = prod[1:].replace('<', '').replace('>', '') if len(prod) > 1 else 'FIM'
        
        input_symbols.add(simbolo)
        states.add(prox_estado)
        
        if simbolo not in transitions[estado_origem]:
            transitions[estado_origem][simbolo] = set()
        transitions[estado_origem][simbolo].add(prox_estado)

# 3. Conversão NFA -> AFD (Determinização)
# Algoritmo simplificado de construção de subconjuntos
dfa_transitions = {}
dfa_initial = frozenset([initial_state])
dfa_states = [dfa_initial]
dfa_final_states = set()
queue = [dfa_initial]
processed = set()

while queue:
    current_set = queue.pop(0)
    current_tuple = tuple(sorted(list(current_set)))
    
    if current_tuple in processed:
        continue
    processed.add(current_tuple)
    
    # Verifica se é estado final (se contém algum estado final do NFA)
    if not current_set.isdisjoint(final_states):
        dfa_final_states.add(current_tuple)
    
    dfa_transitions[current_tuple] = {}
    
    for symbol in sorted(list(input_symbols)):
        next_set = set()
        for sub_state in current_set:
            if sub_state in transitions and symbol in transitions[sub_state]:
                next_set.update(transitions[sub_state][symbol])
        
        if next_set:
            next_tuple = tuple(sorted(list(next_set)))
            dfa_transitions[current_tuple][symbol] = next_tuple
            if next_tuple not in [tuple(sorted(list(s))) for s in dfa_states]:
                dfa_states.append(next_set)
                queue.append(next_set)

# 4. Preparar Tabela (DataFrame)
tabela_dados = []
nome_estados = {tuple(sorted(list(s))): f"q{i}" for i, s in enumerate(dfa_states)}

for estado_set in dfa_states:
    estado_tuple = tuple(sorted(list(estado_set)))
    nome = nome_estados[estado_tuple]
    
    # Marcadores
    tipo = []
    if estado_tuple == tuple(sorted(list(dfa_initial))): tipo.append("INICIAL")
    if estado_tuple in dfa_final_states: tipo.append("FINAL")
    tipo_str = " / ".join(tipo) if tipo else "-"
    
    linha = {'Estado': nome, 'Composição Original': str(estado_tuple), 'Tipo': tipo_str}
    
    for symbol in sorted(list(input_symbols)):
        destino = dfa_transitions.get(estado_tuple, {}).get(symbol)
        linha[symbol] = nome_estados.get(destino, "-") if destino else "-"
    
    tabela_dados.append(linha)

df_resultado = pd.DataFrame(tabela_dados)

# 5. Gerar Gráfico (Graphviz)
dot = graphviz.Digraph(comment='AFD Resultante')
dot.attr(rankdir='LR')

for estado_set in dfa_states:
    estado_tuple = tuple(sorted(list(estado_set)))
    nome = nome_estados[estado_tuple]
    
    # Estilo dos nós
    shape = 'doublecircle' if estado_tuple in dfa_final_states else 'circle'
    if estado_tuple == tuple(sorted(list(dfa_initial))):
        dot.node('start', '', shape='none')
        dot.edge('start', nome)
    
    dot.node(nome, nome, shape=shape)

# Arestas
for origem_tuple, trans in dfa_transitions.items():
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