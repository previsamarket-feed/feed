# feed (perguntas diárias do Previsa Market)

Arquivo público que alimenta as **perguntas diárias** do [Previsa Market](https://www.previsamarket.com.br),
um simulador de previsões com PTS virtuais (sem apostas e sem dinheiro real).

Este repositório contém **apenas perguntas baseadas em notícias públicas**. Não guarda nenhum dado de usuário.

## Como funciona

1. Todos os dias, às 6h (Brasília), uma rotina automática do Claude lê as notícias de g1, Metrópoles, TNT Sports e InfoMoney,
   escreve 2 perguntas novas para cada ícone, confere os resultados das perguntas que encerraram e atualiza o `feed.json`.
2. O servidor do site (Cloudflare) lê o `feed.json` pelo endereço `/api/feed`, com cache de poucos minutos.
3. O navegador de cada pessoa confere cada pergunta (formato, tamanhos, datas, links permitidos) antes de mostrá-la.
   Pergunta fora das regras é descartada sem afetar as demais.

## Arquivos

| Arquivo | Para quê |
| --- | --- |
| `feed.json` | As perguntas, os resultados e as retiradas (é o que o site lê). |
| `REGRAS.md` | Regras editoriais. Leia antes de editar. |
| `validar_feed.py` | Validador: mesmas regras do site + regras editoriais. Rode antes de cada commit. |
| `ROTINA.md` | Roteiro que a rotina diária segue. |

## Formato do `feed.json`

```json
{
  "version": 1,
  "markets": [
    {
      "id": "d20261021-eco-1",
      "cat": "Economia",
      "q": "O IPCA-15 de outubro ficará acima de 0,5%?",
      "outs": ["Sim", "Não"],
      "p": [0.45, 0.55],
      "close": "2026-10-28T12:00:00-03:00",
      "crit": "Sim, se o IBGE divulgar IPCA-15 de outubro de 2026 acima de 0,50%.",
      "src": "IBGE (SIDRA)",
      "desc": "Texto curto opcional com o contexto.",
      "news": [{ "name": "InfoMoney", "url": "https://www.infomoney.com.br/..." }]
    }
  ],
  "resolutions": {
    "d20261015-eco-2": { "outcome": 0, "evidence": "https://www.ibge.gov.br/..." }
  },
  "withdrawn": []
}
```

- `p`: chance inicial de cada opção (uma por opção, entre 0.03 e 0.97, somando 1).
- `outcome`: número da opção vencedora (0 = primeira).
- `evidence`: link `https` da fonte oficial que comprova o resultado.

## Conferir antes de publicar

```bash
python3 validar_feed.py feed.json --hoje 2026-10-21
```

Termina com `OK para publicar` (código 0) ou `NÃO PUBLIQUE` (código 1).
