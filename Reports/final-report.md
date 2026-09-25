# Assistentes de IA versus codificação manual

## 1. Objetivo e questões de pesquisa

Este trabalho realizou um experimento controlado para comparar o uso do GitHub Copilot com a codificação manual na resolução de seis katas Python de nível 6 kyu.

- **RQ1:** o uso de IA reduz o tempo até todos os testes passarem?
- **RQ2:** o uso de IA reduz os defeitos remanescentes?
- **RQ3:** o uso de IA altera complexidade, tamanho, manutenibilidade ou duplicação?

## 2. Metodologia

Foi utilizado um desenho crossover contrabalanceado com dois participantes e seis katas. Cada kata aparece uma vez com IA e uma vez manualmente. O time-box foi de 35 minutos, ou 2100 segundos. Trials sem solução completa foram censurados em 2100 segundos.

O ambiente foi Visual Studio Code, Python 3.14.3 e GitHub Copilot (licença GitHub Student Developer Pack), extensão GitHub Copilot Chat `github.copilot-chat` versão 0.48.1. Os testes de aceitação foram executados pelo runner local do projeto. Os testes ficaram visíveis no workspace, condição mantida para os tratamentos.

### Katas utilizados

Todos são katas 6 kyu do Codewars, resolvidos em Python. Foram escolhidos entre os de menor número de conclusões na plataforma, para reduzir o risco de memorização pelo assistente os clássicos mais populares, com centenas de milhares de conclusões, foram descartados por esse motivo.

| Id | Kata | Testes de aceitação | Link |
|---|---|---:|---|
| k1 | Connect Four - placing tokens | 2 | https://www.codewars.com/kata/connect-four-placing-tokens |
| k2 | Exclamation marks series #17 | 5 | https://www.codewars.com/kata/57fb44a12b53146fe1000136 |
| k3 | If you can read this... | 3 | https://www.codewars.com/kata/586538146b56991861000293 |
| k4 | Kebabize | 5 | https://www.codewars.com/kata/57f8ff867a28db569e000c4a |
| k5 | Buying a car | 5 | https://www.codewars.com/kata/554a44516729e4d80b000012 |
| k6 | The Vowel Code | 4 | https://www.codewars.com/kata/53697be005f803751e0015aa |

A alocação de tratamento foi cruzada: cada kata foi resolvido com IA por um participante e manualmente pelo outro.

Os códigos finais foram arquivados em `data/raw/<participante>` e os resultados foram consolidados em `data/processed/trials.csv`. As métricas estruturais foram coletadas com Radon e jscpd, usando `--min-tokens 20` para duplicação.

### Limitação do procedimento com IA

Tentou-se isolar o ambiente por meio de um ambiente virtual e restringir a interação ao prompt, evitando consultas externas e tentando impedir que a IA simplesmente reproduzisse código pronto ou reconhecesse uma solução conhecida. Entretanto, neste contexto, usar a IA diretamente dentro da IDE não foi uma boa escolha metodológica: os trials `AI` do Felipe foram implementados e medidos como interações assistidas, e não conduzidos integralmente pelo fluxo `run` com a mesma separação operacional dos trials manuais. Por isso, os tempos de IA do Felipe devem ser interpretados como evidência exploratória, não como uma comparação perfeitamente controlada.

## 3. Resultados

Os 12 trials foram consolidados. Houve um trial censurado: `k5` manual do Felipe, com 0 de 5 testes passando ao fim do time-box.

### RQ1: tempo

| Tratamento | Q1 | Mediana | Q3 |
|---|---:|---:|---:|
| Com IA | 10,0 s | 22,5 s | 39,0 s |
| Manual | 777,0 s | 782,0 s | 1380,0 s |

O Wilcoxon pareado por kata produziu `W = 0`, `p = 0,0312`, com 6 pares. Descritivamente, os tempos registrados com IA foram menores. Contudo, o resultado é limitado pela amostra muito pequena e pela diferença de procedimento na medição dos trials de IA do Felipe.

### RQ2: defeitos

A taxa mediana de sucesso foi de 100% nos dois tratamentos. Apenas o par do `k5` apresentou diferença: IA obteve 100% e manual 0%. Cinco diferenças foram zero e apenas um par foi usado no teste de Wilcoxon, que produziu `p = 1,0000`.

Assim, não há evidência estatística suficiente para afirmar que a IA reduziu defeitos nesta amostra. A conclusão descritiva é que a falha observada ocorreu no `k5` manual.

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

## 4. Discussão

O resultado de RQ1 favorece a condição com IA no conjunto observado, mas não permite generalização. O desenho contrabalanceado reduz o efeito de ordem e pessoa, porém o pareamento analítico é por kata: cada participante resolve cada kata em apenas uma condição. Portanto, ele não é um within-subject puro para cada objeto experimental.

Para RQ2, a quantidade reduzida de testes e o fato de quase todos os trials terminarem com 100% de sucesso tornam o teste pouco informativo. Para RQ3, os códigos são curtos e a duplicação não apareceu; LOC é a diferença estrutural mais visível, mas não foi acompanhada por diferença relevante de complexidade ou MI.

## 5. Ameaças e limitações

- Amostra de apenas dois participantes e seis katas.
- Katas com dificuldade não necessariamente equivalente apesar de todos serem 6 kyu.
- Familiaridade prévia diferente com o Copilot.
- Possível memorização dos katas pelo assistente.
- Testes visíveis no workspace.
- Medição dos trials de IA do Felipe não reproduziu integralmente o fluxo operacional dos trials manuais.
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
