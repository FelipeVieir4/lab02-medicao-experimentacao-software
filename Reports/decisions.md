# Decisões do projeto

- **Agente de IA:** GitHub Copilot, versão estudante.
- **Linguagem:** Python 3.14.3.
- **Métricas estáticas:** Radon para complexidade e linhas de código; jscpd
	para duplicação (com `--min-tokens 20`, igual em todos os trials).
- **Desenho:** crossover within-subject, com tratamentos `AI` e `MANUAL`.
- **Time-box:** 35 min (2100s) por trial. Trial que estoura entra censurado
	nesse valor, nunca descartado.
- **Análise:** Wilcoxon pareado para RQ1 e RQ2; mediana e IQR nas descritivas.
- **Arquitetura:** camadas `domain`, `application`, `infrastructure` e
	`presentation`.
- **Dados:** arquivos brutos em `data/raw`, processados em `data/processed` e
	relatórios em `data/reports`.
- **Configuração:** `config/experiment.yaml`, `.env` e `.env.example`.
- **Familiaridade prévia com o Copilot:** Yan — _(preencher)_; Felipe — _(preencher)_.
	Registrar antes do primeiro trial, é ameaça à validade prevista no desenho.
