import csv

def analisar_tipos():
    tipos_unicos = set()
    with open('Banco/pontos_turisticos_traduzido.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tipos = [t.strip() for t in row['Tipos'].split(',')]
            tipos_unicos.update(tipos)
    
    print("Total de tipos únicos:", len(tipos_unicos))
    print("\nTipos encontrados:")
    for tipo in sorted(tipos_unicos):
        print(f"- {tipo}")

if __name__ == "__main__":
    analisar_tipos() 