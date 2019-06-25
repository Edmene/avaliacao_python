#escrever em arquivos

with open('arquivo.txt', 'a') as arquivo:
    arquivo.write('Hello\n') # escreve 'Hello' e quebra a linha
    arquivo.write('World\n') # escreve 'World' e quebra a linha

#dicionários: memórias/arrays associativos
empresa = {'nome': 'Compasso Tecnologia', 'setor': 'Software', 'funcionarios': 500}
print(empresa['nome']) # Compasso Tecnologia
empresa['funcionarios'] = 550
print(empresa['funcionarios']) # 550
print(empresa.keys()) # ['nome', 'setor', 'funcionarios']
del empresa['setor']
print(empresa.keys()) # ['nome', 'funcionarios']
