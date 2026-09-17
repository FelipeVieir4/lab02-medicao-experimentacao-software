# Katas do experimento

Uma pasta por kata, com o id usado no `trial_protocol.py` (`k1` a `k6`):

```
katas/k2/base.py              enunciado em comentario + assinatura da funcao vazia
katas/k2/testes.py            Sample Tests colados do Codewars, sem adaptacao
katas/k2/solucao_<nome>.py    copia do base.py, criada pela CLI no inicio do trial
```

Os moldes de `base.py` e `testes.py` estao em `data/template/`.

Quem prepara cada kata é quem vai resolvê-lo no tratamento MANUAL - montar o arquivo
exige ler o enunciado antes da hora, e dessa forma essa vantagem nunca cai no trial com
IA. `python -m src.presentation.cli plano --participante <nome>` mostra quais são os seus.

Os arquivos `solucao_*.py` ficam versionados: são o código final de cada trial e é sobre
a cópia em `data/raw/<participante>/` que o Radon e o jscpd rodam depois.
