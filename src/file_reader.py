# Função para leitura do arquivo de entrada
def file_reader(file_name):
    
    try:
        caminho = f'src/inputs/{file_name}'
    except Exception as e:
        print(f'Erro ao construir o caminho do arquivo: {e}')
        return []
    
    try:
        with open(caminho, 'r', encoding='utf-8') as file:
            linhas = file.readlines()
    except FileNotFoundError:
        print(f'Arquivo não encontrado: {caminho}')
        return []
       
    return [linha.strip() for linha in linhas] 