# Regras editoriais das perguntas diárias do Previsa Market

O Previsa Market é um **simulador**: os PTS são moeda virtual, sem apostas e sem dinheiro real. As perguntas do
`feed.json` entram no site automaticamente; por isso estas regras valem mais do que qualquer pressa.
**Na dúvida, não publique a pergunta.**

## 1. Quantidade e identificação

- **2 perguntas novas por ícone, por dia** (Economia, Finanças, Tecnologia, Negócios, Esporte, Política) = 12 por dia.
- O dia é o de Brasília (America/Sao_Paulo) em que a rotina roda.
- Formato do `id`: `dAAAAMMDD-<cat>-<n>`, com `<cat>` em `eco`, `fin`, `tec`, `neg`, `esp`, `pol` e `<n>` = 1 ou 2.
  Exemplo: `d20261021-eco-1`. Nunca reutilize nem altere um `id` já publicado.

## 2. Como é uma boa pergunta

- Pode ser respondida com **fato objetivo e verificável** numa **fonte oficial** (IBGE, Banco Central, B3, CBF, FIFA,
  Diário Oficial, Câmara, Senado, STF, agências reguladoras, comunicados das empresas etc.).
- Tem **data e hora de encerramento** (`close`, com fuso: `2026-10-23T18:00:00-03:00`). Prefira de 1 a 45 dias; o site
  aceita até 120.
- O critério (`crit`) diz exatamente o que faz cada opção vencer, em que fonte e em que data. Sem "opinião", sem "parece".
- 2 opções (Sim/Não) na maioria dos casos; até 6 quando fizer sentido (faixas de valores, resultado de jogo).
- A chance inicial (`p`) vem de dados públicos (consenso do Boletim Focus, calendário, histórico, tabela do campeonato),
  entre 0.10 e 0.90 na maioria dos casos. **Nunca copie odds de casas de apostas** e não as cite.
- Escreva com as suas palavras. Não copie títulos nem trechos de matérias.
- Não use linguagem de recomendação de investimento ("compre", "venda", "vale a pena"). É uma pergunta, não um conselho.

## 3. Notícias de origem (`news`)

- Até 3 links `https` de **g1.globo.com, www.metropoles.com, tntsports.com.br (ou www.) e www.infomoney.com.br**. O site
  recusa qualquer outro domínio e a pergunta inteira é descartada.
- InfoMoney: Economia, Finanças, Negócios. TNT Sports: Esporte. g1 e Metrópoles: todos os ícones.
- Se um portal bloquear a leitura, **não contorne**: use outro portal ou outra matéria.
- Cada pergunta deve ter pelo menos um link de notícia que a inspirou, quando houver.

## 4. O que nunca entra

- Pessoas que não sejam figuras públicas no exercício da função, saúde ou vida pessoal de qualquer pessoa, menores de idade.
- Crimes, acusações, investigações, prisões, condenações de pessoas; tragédias, mortes, violência; conteúdo sexual; ódio.
- Qualquer referência a apostas, casas de apostas, odds, cassinos.
- Perguntas ambíguas, que dependam de interpretação ou cujo resultado possa ser contestado.

## 5. Política (regra extra, até a revisão do advogado)

- **Somente institucional**: pauta e votações do Congresso, calendário e julgamentos do STF, regulamentação, prazos legais,
  atos do Diário Oficial, indicadores de governo divulgados por órgãos oficiais.
- **Proibido**: candidatos, partidos, pesquisas eleitorais, resultados de eleição (inclusive o segundo turno de 25/10/2026),
  intenção de voto, denúncias e acusações, nomes de políticos. O validador barra essas palavras.

## 6. Esporte

- Somente resultados oficiais (jogo, classificação, ranking, calendário divulgados por CBF, FIFA, ligas e federações).
- Sem lesões, sem vida pessoal de atletas, sem jogadores menores de idade, sem odds nem apostas.

## 7. Resolução das perguntas encerradas

- Só resolva depois do `close`, e **somente com evidência oficial**: coloque o link `https` da fonte em `evidence`
  e o número da opção vencedora em `outcome` (0 = primeira opção, 1 = segunda...).
- Se o resultado não estiver claro, ou só existir em notícia/boato: **deixe aberta** e diga isso no relatório final.
- Nunca altere uma resolução já publicada. Se houve erro, o caminho é corrigir com cuidado e avisar o responsável.

## 8. Retirar uma pergunta

- Pergunta com erro, ambiguidade ou risco: coloque o `id` em `withdrawn`. O site devolve os PTS usados nela.
- Retire também de `markets`.

## 9. Limpeza (para o arquivo não crescer)

- Limite do site: 600 perguntas e 600 mil caracteres. Meta: **até 500 perguntas** e **menos de 450 mil bytes**.
- Remova de `markets` as perguntas resolvidas há mais de 14 dias. **Mantenha o item em `resolutions` por 90 dias**
  (quem ficou dias sem abrir o site ainda precisa receber o resultado).
- Mantenha em `withdrawn` só os 150 ids mais recentes.

## 10. Antes de publicar

1. `python3 validar_feed.py feed.json --hoje AAAA-MM-DD`
2. Só envie se terminar com **OK para publicar**.
3. Faça um único commit: `Perguntas de AAAA-MM-DD`. Altere somente o `feed.json`.
