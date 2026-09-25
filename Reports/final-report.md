# Assistentes de IA versus codificação manual

## 1. Objetivo e questões de pesquisa

Este trabalho realizou um experimento controlado para comparar o uso do GitHub Copilot com a codificação manual na resolução de seis katas Python de nível 6 kyu.

- **RQ1:** o uso de IA reduz o tempo até todos os testes passarem?
- **RQ2:** o uso de IA reduz os defeitos remanescentes?
- **RQ3:** o uso de IA altera complexidade, tamanho, manutenibilidade ou duplicação?

### Hipóteses

Para cada questão, a hipótese nula afirma que não há diferença entre os tratamentos, e é contra ela que os testes foram aplicados.

| | Hipótese nula (H₀) | Hipótese alternativa (H₁) |
|---|---|---|
| RQ1 | Não há diferença na mediana do tempo até passar em todos os testes entre os trials com IA e sem IA. | Os trials com IA apresentam mediana de tempo menor. |
| RQ2 | Não há diferença na taxa de sucesso mediana ao final do time-box entre os dois tratamentos. | Os trials com IA apresentam taxa de sucesso mediana maior, ou seja, menos defeitos remanescentes. |
| RQ3 | Não há diferença na complexidade ciclomática média entre o código produzido com e sem IA. | A complexidade ciclomática média difere entre os tratamentos, em qualquer direção. |

A hipótese de RQ3 é não direcional de propósito: a literatura não é conclusiva sobre o sentido do efeito do uso de assistentes na estrutura do código, então o experimento se limita a verificar se existe diferença.

## 2. Metodologia

Foi utilizado um desenho crossover contrabalanceado com dois participantes e seis katas. Cada kata aparece uma vez com IA e uma vez manualmente, mas cada participante resolve cada kata em apenas uma condição. Assim, a comparação é pareada por kata e não constitui um desenho within-subject puro para cada kata. O time-box foi de 35 minutos, ou 2100 segundos. Trials sem solução completa foram censurados em 2100 segundos.

O ambiente foi Visual Studio Code, Python 3.14.3 e GitHub Copilot (licença GitHub Student Developer Pack), extensão GitHub Copilot Chat `github.copilot-chat` versão 0.48.1. Os testes de aceitação foram executados pelo runner local do projeto. Os testes ficaram visíveis no workspace, condição mantida para os tratamentos.

### Katas utilizados

Todos são katas 6 kyu do Codewars, resolvidos em Python. Foram escolhidos entre os de menor número de conclusões na plataforma, para reduzir o risco de memorização pelo assistente; os clássicos mais populares, com centenas de milhares de conclusões, foram descartados por esse motivo.

| Id | Kata | Testes de aceitação | Link |
|---|---|---:|---|
| k1 | Connect Four - placing tokens | 2 | https://www.codewars.com/kata/connect-four-placing-tokens |
| k2 | Exclamation marks series #17 | 5 | https://www.codewars.com/kata/57fb44a12b53146fe1000136 |
| k3 | If you can read this... | 3 | https://www.codewars.com/kata/586538146b56991861000293 |
| k4 | Kebabize | 5 | https://www.codewars.com/kata/57f8ff867a28db569e000c4a |
| k5 | Buying a car | 5 | https://www.codewars.com/kata/554a44516729e4d80b000012 |
| k6 | The Vowel Code | 4 | https://www.codewars.com/kata/53697be005f803751e0015aa |

- **k1:** posicionar fichas em uma coluna válida do Connect Four.
- **k2:** comparar o peso de duas frases: cada `!` vale 2 e cada `?` vale 3.
- **k3:** transformar letras em seus nomes do alfabeto fonético da OTAN, mantendo a pontuação.
- **k4:** separar palavras escritas juntas usando hífens, deixando tudo em letras minúsculas e removendo os números.
- **k5:** calcular em quantos meses é possível trocar de carro.
- **k6:** codificar e decodificar vogais por posições numéricas.

A alocação de tratamento foi cruzada: cada kata foi resolvido com IA por um participante e manualmente pelo outro.

Os códigos finais foram arquivados em `data/raw/<participante>` e os resultados foram consolidados em `data/processed/trials.csv`. As métricas estruturais foram coletadas com Radon e jscpd, usando `--min-tokens 20` para duplicação.

### Limitação do procedimento com IA

O projeto oferece uma CLI (`run`) que cronometra o trial, executa os testes de aceitação ao final, arquiva o código e grava o registro automaticamente.

Tentou-se isolar o ambiente por meio de um ambiente virtual e restringir a interação ao prompt, evitando consultas externas e reduzindo a possibilidade de a IA simplesmente reproduzir código pronto ou reconhecer uma solução conhecida. Também, o Felipe tentou deliberadamente empregar um refinamento de um prompt com instruções como: “você não pode usar seus conhecimentos prévios; deve processar a informação do zero”. Essa estratégia buscou tornar a assistência mais controlada e evitar a geração direta de uma solução previamente conhecida, mas não houve uma mudança significativa nos resultados.

## 3. Resultados

Os 12 trials foram consolidados. Houve um trial censurado: `k5` manual do Felipe, com 0 de 5 testes passando ao fim do time-box.

### Revisão dos dados e outliers

Os dados foram revisados pelo critério de 1,5 × IQR aplicado dentro de cada tratamento, separadamente para tempo e taxa de sucesso.

| Métrica | Tratamento | Q1 | Q3 | IQR | Limites | Fora dos limites |
|---|---|---:|---:|---:|---|---|
| Tempo (s) | Com IA | 10,0 | 39,0 | 29,0 | até 82,5 | nenhum |
| Tempo (s) | Manual | 777,0 | 1380,0 | 603,0 | até 2284,5 | nenhum |
| Taxa de sucesso | Com IA | 1,00 | 1,00 | 0,00 | - | nenhum |
| Taxa de sucesso | Manual | 1,00 | 1,00 | 0,00 | - | o 0% do `k5` |

Nenhum outlier de tempo foi identificado. O trial censurado de 2100 s permanece dentro dos limites do grupo manual, porque a dispersão desse grupo é alta o bastante para acomodá-lo.

Na taxa de sucesso, o único ponto sinalizado é o 0% do `k5` manual. Trata-se de artefato do critério: como cinco dos seis valores do grupo são idênticos a 100%, o IQR é zero e qualquer valor diferente é marcado. O ponto não é erro de medição, é o trial censurado, e o protocolo do experimento determina que trials censurados sejam mantidos e nunca descartados, sob pena de enviesar a comparação a favor do tratamento que falha mais.


### RQ1: tempo

| Tratamento | Q1 | Mediana | Q3 |
|---|---:|---:|---:|
| Com IA | 10,0 s | 22,5 s | 39,0 s |
| Manual | 777,0 s | 782,0 s | 1380,0 s |

O teste de Wilcoxon pareado por kata produziu `W = 0` e `p = 0,0312`, com 6 pares. O valor `W = 0` indica que todas as diferenças de tempo apontaram para o mesmo lado: os trials com IA foram mais rápidos que os trials manuais. O valor `p = 0,0312` indica que haveria aproximadamente 3,12% de chance de observar um resultado tão extremo caso não existisse diferença real entre os tratamentos. Como `p < 0,05`, o resultado sugere uma diferença estatisticamente significativa nesta amostra. Contudo, a conclusão é limitada pelo número reduzido de pares e pelo tempo adicional gasto pelo Felipe na formulação de prompts restritivos para impedir que a IA reproduzisse soluções prontas.

![Tempo por kata: com IA versus manual](../data/charts/Tempo%20por%20kata-com%20IA%20versus%20manual.png)

*Figura 1 — Tempo registrado por kata. Cada segmento liga os dois tratamentos do mesmo kata; a escala logarítmica permite visualizar tanto os trials concluídos em segundos quanto os trials próximos do time-box. Os pontos com IA aparecem concentrados em tempos menores.*

### RQ2: defeitos

A taxa mediana de sucesso foi de 100% nos dois tratamentos. Apenas o par do `k5` apresentou diferença: IA obteve 100% e manual 0%. Cinco diferenças foram zero e apenas um par foi usado no teste de Wilcoxon, que produziu `p = 1,0000`.

Assim, não há evidência estatística suficiente para afirmar que a IA reduziu defeitos nesta amostra. A conclusão descritiva é que a falha observada ocorreu no `k5` manual.

![Taxa de sucesso por kata](../data/charts/Taxa%20de%20sucesso%20por%20kata.png)

*Figura 2 — Taxa de testes aprovados por kata e tratamento. Quase todos os trials alcançaram 100%; a única diferença visível está no `k5`, em que o trial manual terminou com 0% de sucesso.*

### RQ3: estrutura

As métricas foram coletadas para todos os 12 códigos finais.

| Métrica mediana | Com IA | Manual |
|---|---:|---:|
| Complexidade média | 4,50 | 4,50 |
| LOC | 13 | 19 |
| SLOC | 10 | 15 |
| Manutenibilidade | 70,80 | 70,67 |
| Duplicação | 0,00% | 0,00% |

As medianas indicam complexidade semelhante, código manual um pouco maior e índice de manutenibilidade praticamente igual. A duplicação foi zero em todos os arquivos segundo o jscpd com limiar de 20 tokens. Como os katas são pequenos, essa métrica tem baixa capacidade de discriminar tratamentos.

![Estrutura do código por kata](../data/charts/Estrutura%20do%20c%C3%B3digo.png)

*Figura 3 — Complexidade ciclomática média e LOC por kata. A complexidade varia entre os katas, mas não apresenta separação consistente entre os tratamentos; a diferença mais recorrente é o maior número de linhas nos códigos manuais.*

![Complexidade média versus LOC](../data/charts/Estrutura%20do%20c%C3%B3digo%202.png)

*Figura 4 — Relação entre tamanho e complexidade. Os pontos permanecem concentrados em códigos pequenos, sem um padrão claro que associe o tratamento a maior complexidade.*

![Efeito do tratamento por participante](../data/charts/O%20efeito%20do%20tratamento%20muda%20de%20dire%C3%A7%C3%A3o%20entre%20os%20participantes.png)

*Figura 5 — Mediana de LOC por participante e tratamento. As linhas apontam em direções opostas: o código do Felipe foi menor com IA, enquanto o do Yan foi maior com IA. Isso recomenda cautela ao interpretar apenas a mediana agregada.*

## 4. Discussão

O resultado de RQ1 favorece a condição com IA no conjunto observado, mas não permite generalização. O desenho contrabalanceado reduz o efeito de ordem e pessoa, porém o pareamento analítico é por kata: cada participante resolve cada kata em apenas uma condição.

Para RQ2, a quantidade reduzida de testes e o fato de quase todos os trials terminarem com 100% de sucesso tornam o teste pouco informativo. Para RQ3, os códigos são curtos e a duplicação não apareceu; LOC é a diferença estrutural mais visível, mas não foi acompanhada por diferença relevante de complexidade.

## 5. Ameaças e limitações

- Amostra de apenas dois participantes e seis katas.
- Katas com dificuldade não necessariamente equivalente apesar de todos serem 6 kyu.
- Familiaridade prévia diferente com o Copilot.
- Possível memorização dos katas pelo assistente.
- Testes visíveis no workspace.
- Pareamento por kata, e não repetição do mesmo kata pelo mesmo participante nos dois tratamentos.
- O jscpd não encontrou duplicação em códigos muito pequenos.

## 6. Conclusão

Neste conjunto de dados, a condição com IA apresentou menor tempo mediano, enquanto não houve diferença estatística observável na taxa de sucesso e não houve duplicação detectada. O resultado de tempo é promissor, mas exploratório e condicionado às limitações de coleta. O experimento não sustenta uma afirmação geral de superioridade da IA; sustenta apenas que, nesta execução, a assistência esteve associada a soluções mais rápidas nos katas observados.

## 7. Reprodutibilidade

Para regenerar os artefatos:

```powershell
python -m src.presentation.cli export
python -m src.presentation.cli metricas
python -m src.presentation.cli analise
streamlit run src/presentation/dashboard.py
```

O dashboard apresenta filtros por participante e tratamento, gráficos de tempo, taxa de sucesso, falhas, LOC e complexidade, além da tabela de métricas estáticas.

**Repositório e GitHub Projects:** https://github.com/FelipeVieir4/lab02-medicao-experimentacao-software

O código, os dados brutos e os artefatos gerados estão nesse repositório. O rastreamento dos trials está nas Issues `#14` a `#24`, e a análise da sprint 3 nas Issues `#25` a `#32`.
