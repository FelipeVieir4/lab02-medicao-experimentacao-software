def kebabize(st):
	partes = []

	for caractere in st:
		if not caractere.isalpha():
			continue
		if caractere.isupper() and partes:
			partes.append('-')
		partes.append(caractere.lower())

	return ''.join(partes)