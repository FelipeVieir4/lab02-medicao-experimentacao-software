# Decisões do projeto

- **Agente de IA:** GitHub Copilot, versão estudante.
- **Linguagem:** Python 3.14.3.
- **Métricas estáticas:** Radon para complexidade e linhas de código; jscpd
	para duplicação.
- **Desenho:** crossover within-subject, com tratamentos `AI` e `MANUAL`.
- **Time-box:** 
- **Análise:**
- **Arquitetura:** camadas `domain`, `application`, `infrastructure` e
	`presentation`.
- **Dados:** arquivos brutos em `data/raw`, processados em `data/processed` e
	relatórios em `data/reports`.
- **Configuração:** `config/experiment.yaml`, `.env` e `.env.example`.
