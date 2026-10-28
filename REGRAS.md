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
- O `close` precisa ser **antes** do fato acontecer ou ser divulgado (jogo, divulgação do índice, resultado da empresa),
  com folga de pelo menos algumas horas, para ninguém responder já sabendo o resultado. Prazos de votação ou de
  decisão (ex.: "até 22/12") podem fechar semanas antes do prazo.
- **As 2 perguntas do mesmo ícone no mesmo dia tratam de assuntos diferentes.** Não publique a mesma pergunta com
  limites ou datas diferentes (ex.: "até 22/12" e "até 18/12" sobre o mesmo orçamento) nem duas perguntas sobre o mesmo
  processo (ex.: duas sobre o mesmo edital). Não repita um tema já publicado nos últimos 7 dias, a menos que haja fato novo.
- O critério (`crit`) diz exatamente o que faz cada opção vencer, em que fonte e em que data. Sem "opinião", sem "parece".
- 2 opções (Sim/Não) na maioria dos casos; até 6 quando fizer sentido (faixas de valores, resultado de jogo).
- A chance inicial (`p`) vem de dados públicos (consenso do Boletim Focus, calendário, histórico, tabela do campeonato),
  entre 0.10 e 0.90 na maioria dos casos. **Nunca copie odds de casas de apostas** e não as cite.
- Escreva com as suas palavras. Não copie títulos nem trechos de matérias.
- Não use linguagem de recomendação de investimento ("compre", "venda", "vale a pena"). É uma pergunta, não um conselho.

## 2A. Tom editorial: assuntos que dividem opinião (orientação do dono, 21/10/2026)

O objetivo é atrair audiência. Entre as perguntas seguras, **prefira as que tratam do que o público está discutindo
e sobre o que há opiniões divididas**. Pelo menos **1 das 2 perguntas de cada ícone** deve ser desse tipo, quando
houver assunto quente; a outra pode ser de calendário (divulgação de índice, jogo, balanço).

- **Assuntos que rendem:** contas públicas e dívida, juros e dólar, preço de combustíveis e alimentos, jornada de
  trabalho, impostos, regulação de big techs e redes sociais, IA e empregos, segurança pública, relação entre
  Congresso e STF, grandes negócios e disputas entre empresas, clássicos e decisões de campeonato.
- **Como escrever:** pergunta direta, com um número ou fato que chame atenção no próprio texto (ex.: "dívida de
  R$ 11,1 trilhões") e uma tensão clara (governo x mercado, empregadores x trabalhadores, Congresso x STF).
  Sem jargão. Perguntas que dão vontade de ir **contra a maioria** são bem-vindas (opção improvável, mas possível,
  com `p` entre 0.15 e 0.35).
- **A polêmica vem do assunto, nunca do tom:** sem ironia, sem adjetivos, sem sugerir quem está certo ou errado,
  sem provocar. O critério continua sendo fato objetivo, fonte oficial e data.
- **Continua proibido, mesmo sendo "quente":** candidatos, partidos, eleições, pesquisas, nomes de políticos,
  acusações, crimes, saúde e vida pessoal, menores de idade, apostas e odds. Evite também disputas de identidade
  (religião, raça, gênero, orientação sexual). Na dúvida, escolha outro assunto quente.
- Os limites dos itens 4 e 5 não mudam. O validador também não.

## 2B. Pauta quente do Google Notícias: "da notícia à previsão" (orientação do dono, 28/10/2026)

O dono aprovou e mandou manter, para todas as perguntas daqui em diante, esta dinâmica: **notícia em alta -> previsão**.

- **Pauta.** Leia o Google Notícias Brasil (RSS `https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419`, mais as seções
  Brasil, Negócios, Esportes e Tecnologia, trocando `/rss?` por `/rss/headlines/section/topic/NATION?` etc.). Se o endereço
  não abrir, use as manchetes dos 4 portais. O Google Notícias serve para **descobrir o assunto do dia**: o link das
  perguntas (`news`) continua sendo direto para g1, Metrópoles, InfoMoney ou TNT Sports (os links do Google são
  redirecionamentos e o site os recusa).
- **Quantidade.** Cada pauta quente permitida pode virar 1 ou 2 perguntas. Elas entram como **extras**: até **2 por ícone
  por dia** (ids `-3` e `-4`), além das 2 do lote normal. Rode o validador com `--maximo 4`.
- **Cuidados de sempre.** Fato objetivo, fonte oficial, `close` antes do fato, critério "Sim, se... / Não, se...", sem
  tragédias, sem crimes contra pessoas comuns, sem jogo de azar (loterias) e sem repetir tema dos últimos 7 dias.
- **Pauta vetada nunca vai ao ar sozinha.** Se a notícia mais quente do dia for vetada pelas seções 4 e 5 (nome de político,
  candidato, partido, eleição, acusação, investigação, prisão), **não publique**: deixe a pergunta pronta no relatório final,
  na lista "AGUARDANDO AUTORIZAÇÃO INDIVIDUAL DO DONO" (pergunta, opções, critério, fonte, data de encerramento e links), para
  ele autorizar no chat, id a id, como nas seções 5A e 5B.

## 2C. Procuração do dono: notícias e previsões 24 horas, sem aprovação item a item (28/10/2026, 11h33)

O dono escreveu no chat: "voce tem a procuração para postar noticiais e previsões livremente 24h por dia ... em real time do
google noticiais". Isto vale como autorização permanente para **publicar sem pedir aprovação a cada pergunta**, com estes limites:

- **Rodadas ao longo do dia.** Além do lote das 6h, a rotina de pauta quente roda várias vezes por dia (ROTINA.md, seção 6).
  Cada rodada lê o Google Notícias, escolhe as pautas novas e publica de 1 a 3 perguntas. Ids seguem a numeração do dia
  (`-3` em diante, no máximo `-9` por ícone). Rode o validador com `--procuracao`.
- **Continua valendo tudo das seções 1, 2, 2A, 2B, 3 e 6**: fato objetivo, fonte oficial, `close` antes do fato, critério
  "Sim, se... / Não, se...", `news` direto para g1, Metrópoles, InfoMoney ou TNT Sports, probabilidade inicial entre 0.10 e 0.90
  e nada repetido nos últimos 7 dias.
- **Tema político e eleitoral passa a ser permitido** (notícia em alta com data e fato verificável: candidato, partido,
  eleição, nome de pessoa pública no exercício da função), em tom neutro, sem opinar. O validador só avisa; **todo item político
  publicado vai listado no relatório**, com o id para retirar rápido (`withdrawn`).
- **Seguem vetados mesmo com a procuração** (o validador dá erro): crimes, denúncias, acusações, investigações, prisões,
  condenações; tragédias, mortes, saúde e vida pessoal; menores de idade; conteúdo sexual ou de ódio; apostas e jogo de azar.
  Perguntas sobre esses temas só saem com autorização expressa do dono para aquele id (seção 5B é o modelo).
- **Notícias do módulo de redação** (`/noticias/`): a matéria **normal** segue o fluxo automático. A matéria **sensível**
  (política, crime, saúde) exige segunda aprovação de pessoa; sob esta procuração Claude só a publica se o dono tiver
  autorizado aquele assunto no chat, e registra a autorização na trilha de auditoria.
- **Fila de notícias (28/10/2026, dono: "agora").** O robô de Notícias coleta 4 vezes por dia (0h, 6h, 12h e 18h de Brasília) e o
  banco trava o limite em 20 notícias por dia, 5 por janela (gatilho `limite_nao_aumenta`; só sobe com migração). Para dar
  prioridade ao que está em alta no Google Notícias **sem mexer no código** (mexer apaga os agendamentos), Claude, numa sessão
  com o painel aberto, sobe a pauta quente para o topo da tabela `pauta` do D1 `previsamarket-redacao`: `INSERT OR IGNORE`
  com o link **direto do portal** (nunca o do Google) e `UPDATE pauta SET coletada_em = <agora> WHERE hash_dup = <sha256 do
  título normalizado>`. A fila lê `coletada_em DESC`; o texto continua sendo escrito pelo robô, com todas as travas dele.
- **Nunca** use esta procuração para gasto, para mexer em dados do site (KV, D1 `previsa-stats`, LMSR, PTS) ou para mudar
  regras do jogo. Em dúvida, não publique e liste em "AGUARDANDO AUTORIZAÇÃO DO DONO".

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

### 5A. Exceção autorizada (24/10/2026)

O responsável autorizou, por escrito no chat (24/10/2026, 02:17 de Brasília: "autorizo, assumo o risco, pode ajustar a trava"),
UMA pergunta eleitoral: `d20261024-pol-9` ("Quem venceu o debate da Globo?"), assumindo o risco legal (a regra do TSE sobre
enquetes durante a campanha foi explicada a ele antes). A exceção vale **somente para esse id** (`EXCECOES_ELEITORAIS` em
`validar_feed.py`). Continua proibido criar qualquer outra pergunta eleitoral sem nova autorização individual. A rotina
diária **não** deve copiar este caso.

### 5B. Exceções autorizadas (28/10/2026)

O responsável aprovou, por escrito no chat (28/10/2026, 11h21, Brasília: "aprovado, pode publicar"), depois de ver o texto
completo de cada uma no exemplo "Da notícia à previsão", TRÊS perguntas de Política: `d20261028-pol-3` (Flávio Bolsonaro
voltará ao Brasil até 12/12/2026?), `d20261028-pol-4` (prisão preventiva decretada pelo STF até 12/12/2026?) e
`d20261028-pol-5` (maioria republicana na Câmara dos EUA em 3/11/2026). A exceção vale **somente para esses ids**
(`EXCECOES_ELEITORAIS` em `validar_feed.py`). As perguntas citam pessoa pública e tema de investigação/prisão, que a seção 4
veta; por isso o risco é do responsável e a saída é rápida: colocar o id em `withdrawn` (o site devolve os PTS). O encerramento
da `pol-5` é 3/11 às 6h (antes da votação), e não em 27/11 como no exemplo, porque a seção 2 exige fechar antes do fato.
A rotina diária **não** deve copiar estes casos (veja a seção 2B).

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
