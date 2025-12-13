import json
nb = json.load(open('notebooks/50_optimization_or/OR-09-network_optimization.ipynb'))
for i, cell in enumerate(nb['cells']):
    if cell.get('id') == '7f01ade1':
        print("Encontrada celda 7f01ade1 en índice:", i)
        print("Primeros 300 caracteres:")
        src = ''.join(cell.get('source', []))
        print(src[:300])
        print("\n....\n")
        print("Línea del solver:")
        for line in src.split('\n'):
            if 'solve' in line:
                print(repr(line))
        break
