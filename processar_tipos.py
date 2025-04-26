import csv

# Nome do arquivo de entrada e saída
arquivo_entrada = 'Banco/pontos_turisticos_traduzido.csv'
arquivo_saida = 'Banco/pontos_turisticos_atualizado.csv'

# Lista de palavras-chave e seus respectivos tipos
palavras_chave = {
    'Cachoeira': 'cachoeira',
    'Rafting': 'rafting',
    'Tirolesa': 'tirolesa'
}

# Função para verificar se o nome contém alguma das palavras-chave
def verificar_palavras_chave(nome):
    tipos_adicionais = []
    for palavra, tipo in palavras_chave.items():
        if palavra.lower() in nome.lower():
            tipos_adicionais.append(tipo)
    return tipos_adicionais

# Ler o arquivo CSV e processar
with open(arquivo_entrada, 'r', encoding='utf-8') as entrada, \
     open(arquivo_saida, 'w', newline='', encoding='utf-8') as saida:
    
    leitor = csv.DictReader(entrada)
    campos = leitor.fieldnames
    
    escritor = csv.DictWriter(saida, fieldnames=campos)
    escritor.writeheader()
    
    for linha in leitor:
        # Verificar se o nome contém alguma das palavras-chave
        tipos_adicionais = verificar_palavras_chave(linha['Nome'])
        
        if tipos_adicionais:
            # Adicionar os novos tipos à lista existente
            tipos_existentes = [t.strip() for t in linha['Tipos'].split(',')]
            tipos_existentes.extend(tipos_adicionais)
            # Remover duplicatas e ordenar
            tipos_existentes = sorted(set(tipos_existentes))
            linha['Tipos'] = ', '.join(tipos_existentes)
        
        escritor.writerow(linha)

print("Processamento concluído. Arquivo atualizado salvo em:", arquivo_saida) 