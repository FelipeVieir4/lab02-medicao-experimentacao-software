def balance(left, right):
	pesos = {'!': 2, '?': 3}
	
	peso_esquerdo = sum(pesos[caractere] for caractere in left)
	peso_direito = sum(pesos[caractere] for caractere in right)

	if peso_esquerdo > peso_direito:
		return "Left"
	if peso_direito > peso_esquerdo:
		return "Right"
	return "Balance"
