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