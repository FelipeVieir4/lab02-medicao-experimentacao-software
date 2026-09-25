def encode(st):
	vogais = {'a': '1', 'e': '2', 'i': '3', 'o': '4', 'u': '5'}
	return ''.join(vogais.get(caractere, caractere) for caractere in st)


def decode(st):
	vogais = {'1': 'a', '2': 'e', '3': 'i', '4': 'o', '5': 'u'}
	return ''.join(vogais.get(caractere, caractere) for caractere in st)
