# Análise das RQ1 e RQ2

Pareamento por kata: o trial com IA de um integrante contra o trial manual do outro, no mesmo kata. Teste de Wilcoxon exato para amostras pareadas, com descritivas em mediana e IQR.

Trials censurados no time-box: 0 com IA, 1 manuais.

## RQ1 — tempo ate passar nos testes (time-to-green)

Com IA (segundos): Q1 10.00 | mediana 22.50 | Q3 39.00
Manual (segundos): Q1 777.00 | mediana 782.00 | Q3 1380.00

| Kata | Com IA | Manual | Diferença (IA − manual) |
|---|---:|---:|---:|
| k1 | 33.00 | 1380.00 | -1347.00 |
| k2 | 12.00 | 680.00 | -668.00 |
| k3 | 41.00 | 780.00 | -739.00 |
| k4 | 10.00 | 784.00 | -774.00 |
| k5 | 39.00 | 2100.00 | -2061.00 |
| k6 | 6.00 | 777.00 | -771.00 |

Wilcoxon pareado: W = 0, p = 0.0312 (6 de 6 pares; 0 descartado(s) por diferença zero).
Com 6 pares, o menor p-valor que este teste pode produzir é 0.0312 — o limite vem do tamanho amostral, não dos dados.
Ao nível de 5%, rejeita a hipótese nula.

## RQ2 — taxa de sucesso ao fim do time-box

Com IA (proporcao de testes passando): Q1 1.00 | mediana 1.00 | Q3 1.00
Manual (proporcao de testes passando): Q1 1.00 | mediana 1.00 | Q3 1.00

| Kata | Com IA | Manual | Diferença (IA − manual) |
|---|---:|---:|---:|
| k1 | 1.00 | 1.00 | +0.00 |
| k2 | 1.00 | 1.00 | +0.00 |
| k3 | 1.00 | 1.00 | +0.00 |
| k4 | 1.00 | 1.00 | +0.00 |
| k5 | 1.00 | 0.00 | +1.00 |
| k6 | 1.00 | 1.00 | +0.00 |

Wilcoxon pareado: W = 0, p = 1.0000 (1 de 6 pares; 5 descartado(s) por diferença zero).
Com 1 pares, o menor p-valor que este teste pode produzir é 1.0000 — o limite vem do tamanho amostral, não dos dados.
Ao nível de 5%, não rejeita a hipótese nula.
