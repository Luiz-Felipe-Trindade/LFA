# Função que constrói uma gramática BNF a partir de uma lista de produções
def constructor(lista_producoes): 
    bnf = {}

    try:
        for linha_producoes in lista_producoes:
            partes = linha_producoes.split("::=")
            bnf[partes[0].strip()] = [p.strip() for p in partes[1].split("|")]
        return bnf
    except Exception as e:
        return (f"Erro ao construir a BNF: {e}")

def bnf_to_afn(bnf):
    afn={}
    estados_finais = set()
    
    try:
        for simbolo, producoes in bnf.items():
            if simbolo not in afn:
                afn[simbolo] = {}
                
            for p in producoes:
                
                # Tratamento para produção vazia (ε)
                if p == "ε":
                    estados_finais.add(simbolo)
                    continue
                
                # Tratamento para transições com terminal + não terminal (aB)
                if len(p) == 2:
                    estado_atual = p[0]
                    proximo_estado = p[1]
                    
                    afn[simbolo].setdefault(estado_atual, set()).add(proximo_estado)
                 
                    
                    
                estados = p.split()
                afn[simbolo].append(estados)
        return afn
    except Exception as e:
        return (f"Erro ao converter BNF para AFN: {e}")
    