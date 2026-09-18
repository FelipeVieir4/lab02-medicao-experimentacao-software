# Laboratório 02 - Medição e Experimentação de Software

Experimento controlado para comparar o uso de um assistente de IA com a codificação manual na resolução de katas de programação.

## 1. Objetivo do experimento

O experimento compara duas condições:

- `AI`: GitHub Copilot habilitado.
- `MANUAL`: GitHub Copilot desabilitado e sem consultas externas.

Cada integrante resolve os mesmos seis katas. Como o tratamento é alternado entre os integrantes, cada kata é resolvido uma vez com IA e uma vez sem IA.

O experimento procura responder três questões:

- **RQ1 - Tempo:** o uso de IA reduz o tempo necessário para passar em todos os testes?
- **RQ2 - Defeitos:** o uso de IA reduz a quantidade de testes que falham?
- **RQ3 - Estrutura:** o uso de IA altera a complexidade, o tamanho ou a duplicação do código?

Cada trial possui um limite máximo de **35 minutos**, ou **2100 segundos**.

## 2. Desenho experimental

O desenho utilizado é um **crossover within-subject contrabalanceado**.

Isso significa que:

- os dois integrantes resolvem os mesmos katas;
- cada integrante realiza metade dos katas com IA e metade sem IA;
- a ordem dos tratamentos é invertida entre os integrantes;
- cada kata aparece nas duas condições experimentais.

A escala está definida em `src/domain/services/trial_protocol.py`:

| Kata | Yan | Felipe |
|---|---|---|
| `k1` | IA | Manual |
| `k2` | Manual | IA |
| `k3` | IA | Manual |
| `k4` | Manual | IA |
| `k5` | IA | Manual |
| `k6` | Manual | IA |

Essa organização reduz a influência de diferenças individuais, aprendizado e cansaço ao longo dos trials.

## 3. Katas utilizados

Os seis katas são de nível 6 kyu e possuem testes de aceitação:

1. `k1` - Connect Four - placing tokens
2. `k2` - Exclamation marks series #17
3. `k3` - If you can read this...
4. `k4` - Kebabize
5. `k5` - Buying a car
6. `k6` - The Vowel Code

A documentação específica dos arquivos dos katas está em [katas/README.md](katas/README.md).

Cada kata possui:

- `base.py`: enunciado e assinatura da função;
- `testes.py`: testes de aceitação;
- `solucao_<participante>.py`: arquivo usado pelo participante.

## 4. O que já foi implementado

### 4.1 Definição automática do tratamento

O sistema identifica automaticamente se o trial deve ser realizado com IA ou manualmente, usando o participante e o código do kata.

O participante não escolhe o tratamento na hora da execução. Isso evita que um kata seja executado acidentalmente na condição errada.

### 4.2 Cronômetro

O comando `run` inicia o cronômetro depois que o participante pressiona ENTER. O tempo é medido com um relógio monotônico.

O trial é encerrado quando:

- todos os testes passam; ou
- o limite de 35 minutos é atingido.

O tempo e o resultado dos testes são registrados mesmo quando a solução não está completa. Nesse caso, o trial é considerado censurado em 2100 segundos.

### 4.3 Execução dos testes

Os testes são executados em uma pasta temporária. A solução do participante é copiada para essa pasta com o nome `solution.py`, que é o nome esperado pelos testes adaptados do Codewars.

O código original do participante não é alterado durante a execução dos testes.

### 4.4 Registro dos trials

Cada trial gera uma linha em um arquivo CSV específico do participante:

```text
data/raw/trials_yan.csv
data/raw/trials_felipe.csv
```

O registro contém:

- participante;
- ordem do trial;
- kata;
- tratamento (`AI` ou `MANUAL`);
- horário de início;
- tempo em segundos;
- indicação de censura;
- quantidade total de testes;
- quantidade de testes aprovados;
- observações;
- caminho do código final arquivado.

O código final de cada trial é salvo em:

```text
data/raw/<participante>/<ordem>_<kata>_<tratamento>.py
```

Esses arquivos devem ser preservados, pois são a versão usada posteriormente para calcular as métricas estáticas.

## 5. Preparação do ambiente

O projeto utiliza:

- Visual Studio Code;
- Python 3.14.3;
- GitHub Copilot na versão estudante;
- Radon para métricas estáticas;
- jscpd para duplicação de código.

Confira a versão do Python:

```powershell
python --version
```

Instale o Radon:

```powershell
pip install radon
```

Para instalar o jscpd, caso ainda não esteja disponível:

```powershell
npm install -g jscpd
```

## 6. Fluxo de execução dos trials

Todos os comandos devem ser executados no terminal, a partir da raiz do projeto.

### 6.1 Conferir a escala do participante

Para Yan:

```powershell
python -m src.presentation.cli plano --participante yan
```

Para Felipe:

```powershell
python -m src.presentation.cli plano --participante felipe
```

Esse comando mostra:

- a ordem dos seis katas;
- o tratamento de cada kata;
- quais katas precisam ser preparados pelo participante.

Cada participante prepara os arquivos dos katas que resolverá na condição `MANUAL`. Dessa forma, ninguém precisa ler o enunciado do kata da condição com IA antes do início do trial.

### 6.2 Iniciar um trial

Exemplo para Yan no kata `k1`:

```powershell
python -m src.presentation.cli run --participante yan --kata k1
```

Exemplo para Felipe:

```powershell
python -m src.presentation.cli run --participante felipe --kata k1
```

O comando informa se o Copilot deve estar ligado ou desligado.

Quando aparecer a mensagem para pressionar ENTER:

1. deixe o ambiente pronto;
2. pressione ENTER;
3. comece a resolver o kata;
4. use ou não use o Copilot conforme o tratamento informado;
5. execute os testes durante o trial;
6. pressione ENTER quando todos os testes passarem ou quando o tempo acabar.

Não é permitido utilizar outra consulta externa durante os trials.

### 6.3 Executar os testes

Os testes podem ser executados em outro terminal:

```powershell
python -m src.presentation.cli test --participante yan --kata k1
```

Ou:

```powershell
python -m src.presentation.cli test --participante felipe --kata k1
```

O comando mostra quantos testes passaram e quantos testes existem no total.

Quando todos os testes passarem, volte ao terminal em que o comando `run` está aguardando e pressione ENTER para encerrar o trial.

Se os 35 minutos acabarem, pare de programar, execute os testes uma última vez e pressione ENTER. O resultado será registrado como censurado caso nem todos os testes tenham passado.

### 6.4 Executar todos os katas

Yan deve executar:

```powershell
python -m src.presentation.cli run --participante yan --kata k1
python -m src.presentation.cli run --participante yan --kata k2
python -m src.presentation.cli run --participante yan --kata k3
python -m src.presentation.cli run --participante yan --kata k4
python -m src.presentation.cli run --participante yan --kata k5
python -m src.presentation.cli run --participante yan --kata k6
```

Felipe deve executar os mesmos comandos substituindo o participante:

```powershell
python -m src.presentation.cli run --participante felipe --kata k1
python -m src.presentation.cli run --participante felipe --kata k2
python -m src.presentation.cli run --participante felipe --kata k3
python -m src.presentation.cli run --participante felipe --kata k4
python -m src.presentation.cli run --participante felipe --kata k5
python -m src.presentation.cli run --participante felipe --kata k6
```

O sistema impede registrar duas vezes o mesmo kata para o mesmo participante. O parâmetro `--refazer` só deve ser usado quando houver um erro real no trial:

```powershell
python -m src.presentation.cli run --participante yan --kata k1 --refazer
```

## 7. Consolidação dos dados

Depois de concluir os 12 trials, consolide os arquivos CSV dos participantes:

```powershell
python -m src.presentation.cli export
```

Esse comando gera:

```text
data/processed/trials.csv
```

O arquivo consolidado contém os dados dos dois participantes e calcula as métricas derivadas:

- taxa de sucesso dos testes;
- quantidade de testes falhando.

## 8. Coleta das métricas estáticas

Depois que todos os trials forem concluídos e os códigos finais estiverem arquivados, execute:

```powershell
python -m src.presentation.cli metricas
```

Esse comando analisa os arquivos em `data/raw` e gera:

```text
data/processed/metrics.csv
```

As métricas coletadas são:

- complexidade ciclomática média por função;
- complexidade ciclomática máxima;
- quantidade de funções;
- LOC;
- SLOC;
- quantidade de comentários;
- índice de manutenibilidade;
- percentual de duplicação, quando o jscpd estiver instalado.

O Radon é utilizado por meio de sua API Python, com as operações equivalentes a:

- `cc`: complexidade ciclomática;
- `mi`: índice de manutenibilidade;
- `raw`: linhas e informações brutas do código.

## 9. Análise dos resultados

Os resultados devem ser analisados separando os tratamentos `AI` e `MANUAL`.

### RQ1 - Tempo

Usar:

- tempo até passar em todos os testes;
- valor de 2100 segundos para trials censurados;
- mediana;
- intervalo interquartil (IQR);
- teste de Wilcoxon pareado.

### RQ2 - Defeitos

Usar:

- taxa de sucesso dos testes;
- quantidade absoluta de testes falhando;
- mediana e IQR;
- teste de Wilcoxon pareado quando aplicável.

### RQ3 - Estrutura

Comparar entre os tratamentos:

- complexidade ciclomática média;
- LOC e SLOC;
- índice de manutenibilidade;
- duplicação de código.

A complexidade e a duplicação devem ser interpretadas junto com LOC, porque um código maior pode apresentar valores diferentes simplesmente por ter mais linhas.

## 10. O que ainda falta concluir

A coleta automatizada já está estruturada, mas o trabalho ainda precisa de:

1. executar os 12 trials;
2. registrar a familiaridade prévia de Yan e Felipe com o Copilot em `Reports/decisions.md`;
3. manter a mesma regra sobre visibilidade dos testes em todos os trials;
4. revisar os arquivos gerados em `data/raw`;
5. executar `export` e `metricas`;
6. gerar tabelas e gráficos com Pandas, Matplotlib e Seaborn;
7. aplicar as análises estatísticas;
8. preencher os resultados por RQ em `Reports/final-report.md`;
9. escrever a discussão final;
10. inserir o link do repositório e do GitHub Projects, conforme solicitado pelo enunciado.

## 11. Comandos resumidos

Fluxo completo depois de preparar o ambiente:

```powershell
# Conferir o planejamento
python -m src.presentation.cli plano --participante yan
python -m src.presentation.cli plano --participante felipe

# Executar os 6 trials de cada participante
python -m src.presentation.cli run --participante yan --kata k1
python -m src.presentation.cli run --participante yan --kata k2
python -m src.presentation.cli run --participante yan --kata k3
python -m src.presentation.cli run --participante yan --kata k4
python -m src.presentation.cli run --participante yan --kata k5
python -m src.presentation.cli run --participante yan --kata k6

python -m src.presentation.cli run --participante felipe --kata k1
python -m src.presentation.cli run --participante felipe --kata k2
python -m src.presentation.cli run --participante felipe --kata k3
python -m src.presentation.cli run --participante felipe --kata k4
python -m src.presentation.cli run --participante felipe --kata k5
python -m src.presentation.cli run --participante felipe --kata k6

# Consolidar os dados
python -m src.presentation.cli export

# Calcular métricas estáticas
python -m src.presentation.cli metricas
```

## 12. Estrutura principal de dados

```text
data/
├── raw/
│   ├── trials_yan.csv
│   ├── trials_felipe.csv
│   └── <participante>/
│       └── códigos finais dos trials
├── processed/
│   ├── trials.csv
│   └── metrics.csv
└── template/

Reports/
├── decisions.md
└── final-report.md
```

O arquivo `Reports/decisions.md` registra as decisões metodológicas do experimento. O arquivo `Reports/final-report.md` apresenta o desenho do experimento e deverá receber os resultados finais após a execução e análise dos trials.
