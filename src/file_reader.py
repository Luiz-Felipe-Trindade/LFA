def file_reader(file_name):
    
    try:
        caminho = f'src/inputs/{file_name}'
    except Exception as e:
        print(f'Erro ao construir o caminho do arquivo: {e}')
        return []
    
    with open(caminho, 'r', encoding='utf-8') as file:
       linhas = file.readlines()
       print(f'Linhas lidas do arquivo {file_name}: {linhas}')
       
    return [linha.strip() for linha in linhas] 