#!/usr/bin/env python3
"""Validador do feed.json do Previsa Market.

Espelha as regras que o site aplica a cada pergunta (index.html: feedMarketOK) e acrescenta
regras editoriais. Se uma pergunta falhar aqui, o site também a descartaria; por isso rode
sempre antes de enviar (commit) qualquer alteração.

Uso:
  python3 validar_feed.py feed.json                      # confere o arquivo todo
  python3 validar_feed.py feed.json --hoje 2026-10-21    # também exige o lote do dia (2 por ícone)
  python3 validar_feed.py feed.json --hoje 2026-10-21 --minimo 1   # aceita lote incompleto (avise o responsável)

Código de saída: 0 = sem erros (avisos podem existir); 1 = há erros, NÃO publique.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from urllib.parse import urlparse

ID_RE = re.compile(r'^d(\d{4})(\d{2})(\d{2})-(eco|fin|tec|neg|esp|pol)-([1-9])$')
CATS = {'eco': 'Economia', 'fin': 'Finanças', 'tec': 'Tecnologia', 'neg': 'Negócios', 'esp': 'Esporte', 'pol': 'Política'}
# mesmos domínios que o site aceita em "news" (FEED_NEWS_HOSTS)
NEWS_HOSTS = {'g1.globo.com', 'www.metropoles.com', 'tntsports.com.br', 'www.tntsports.com.br', 'www.infomoney.com.br'}
BRT = dt.timezone(dt.timedelta(hours=-3))
ISO_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$')
MAX_BYTES = 600000       # limite do site e do servidor
MAX_MARKETS = 600        # limite do site
SOFT_MARKETS = 500       # acima disso, faça a limpeza descrita em REGRAS.md

# Regras editoriais (heurística: ajuda a não esquecer; não substitui o julgamento).
BLOCK_ALL = re.compile(
    r'(?i)\b(candidat[oa]s?|eleiç(?:ão|ões)|eleit[oa]s?|urnas?|segundo turno|intenç(?:ão|ões) de voto|'
    r'datafolha|quaest|ipec|partidos?|impeachment|cassaç(?:ão|ões)|denúncias?|denunciad[oa]s?|investigad[oa]s?|'
    r'condenad[oa]s?|presos?|prisão|indiciad[oa]s?|inquérito|acusad[oa]s?|'
    r'apostas?|apostar|bets?|odds|cassinos?|casas? de apostas?)\b'
)
# ids com exceção ao veto eleitoral: SOMENTE por autorização expressa e individual do responsável (REGRAS.md, seção 5A)
EXCECOES_ELEITORAIS = {
    'd20261024-pol-9',
    # 28/10/2026, 11h21 (Brasília): o responsável aprovou, por escrito no chat, estas 3 perguntas já vistas por ele (REGRAS.md, seção 5B)
    'd20261028-pol-3', 'd20261028-pol-4', 'd20261028-pol-5',
}
BLOCK_POL = re.compile(r'(?i)\b(lula|bolsonaro|tarc[ií]sio|ciro|marçal|boulos|zema|caiado|ratinho|michelle)\b')


def jslen(s):
    """Tamanho como o JavaScript conta (unidades UTF-16)."""
    return len(s.encode('utf-16-le')) // 2


def fstr(v, lo, hi):
    return isinstance(v, str) and len(v.strip()) >= lo and jslen(v) <= hi


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def feed_day(mid):
    m = ID_RE.match(mid or '')
    if not m:
        return None
    try:
        return dt.datetime(int(m[1]), int(m[2]), int(m[3]), 6, 0, tzinfo=BRT)
    except ValueError:
        return None


def parse_iso(s):
    if not isinstance(s, str) or not ISO_RE.match(s):
        return None
    try:
        return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))
    except ValueError:
        return None


def https_url(u):
    try:
        p = urlparse(u)
    except Exception:
        return False
    return p.scheme == 'https' and bool(p.hostname)


def check_structure(x):
    """Regras idênticas às do site. Devolve a lista de erros (vazia = o site aceita)."""
    if not isinstance(x, dict):
        return ['não é um objeto']
    errs = []
    mid = x.get('id') if isinstance(x.get('id'), str) else ''
    m = ID_RE.match(mid)
    if not m or CATS.get(m[4]) != x.get('cat'):
        errs.append('id inválido ou categoria diferente do id')
    if not fstr(x.get('q'), 15, 200):
        errs.append('q (pergunta): 15 a 200 caracteres')
    if not fstr(x.get('crit'), 20, 500):
        errs.append('crit (critério): 20 a 500 caracteres')
    if not fstr(x.get('src'), 3, 120):
        errs.append('src (fonte oficial): 3 a 120 caracteres')
    if x.get('desc') is not None and not fstr(x.get('desc'), 0, 400):
        errs.append('desc: até 400 caracteres')
    outs = x.get('outs')
    outs_ok = isinstance(outs, list) and 2 <= len(outs) <= 6 and all(fstr(o, 1, 40) for o in outs) \
        and len({o.strip().lower() for o in outs}) == len(outs)
    if not outs_ok:
        errs.append('outs: de 2 a 6 opções, 1 a 40 caracteres, sem repetir')
    p = x.get('p')
    if not (outs_ok and isinstance(p, list) and len(p) == len(outs) and all(is_num(v) and 0.03 <= v <= 0.97 for v in p)
            and abs(sum(p) - 1) <= 0.02):
        errs.append('p: um número por opção, cada um entre 0.03 e 0.97, somando 1 (tolerância 0.02)')
    day = feed_day(mid)
    close = parse_iso(x.get('close'))
    if day is None or close is None:
        errs.append('close: data ISO com fuso (ex.: 2026-10-23T18:00:00-03:00) e id com data válida')
    elif close <= day or close > day + dt.timedelta(days=120):
        errs.append('close: precisa ser depois do dia do id e em até 120 dias')
    news = x.get('news')
    if news is not None:
        ok = isinstance(news, list) and len(news) <= 3 and all(
            isinstance(n, dict) and fstr(n.get('name'), 1, 40) and isinstance(n.get('url'), str)
            and len(n['url']) <= 300 and https_url(n['url']) and urlparse(n['url']).hostname in NEWS_HOSTS
            for n in news)
        if not ok:
            errs.append('news: até 3 links https de g1, Metrópoles, TNT Sports ou InfoMoney, com nome')
    return errs


def _avisos_gerais(x):
    warns = []
    if isinstance(x.get('q'), str) and not x['q'].strip().endswith('?'):
        warns.append('a pergunta deveria terminar com "?"')
    p = x.get('p')
    if isinstance(p, list) and p and all(is_num(v) for v in p) and (min(p) < 0.10 or max(p) > 0.90):
        warns.append('probabilidade inicial muito extrema (prefira entre 0.10 e 0.90)')
    day, close = feed_day(x.get('id')), parse_iso(x.get('close'))
    if day and close:
        if close < day + dt.timedelta(hours=24):
            warns.append('encerra em menos de 24 horas')
        if close > day + dt.timedelta(days=90):
            warns.append('encerra em mais de 90 dias (prefira 1 a 45 dias)')
    if not x.get('news'):
        warns.append('sem link de notícia de origem (news)')
    return warns


def check_editorial(x):
    """Regras editoriais. Devolve (erros, avisos)."""
    errs, warns = [], []
    text = ' '.join(str(x.get(k) or '') for k in ('q', 'desc', 'crit', 'src', 'outs')
                    if not isinstance(x.get(k), list)) + ' ' + ' '.join(x.get('outs') or [])
    if x.get('id') in EXCECOES_ELEITORAIS:      # autorização expressa e individual do responsável (ver REGRAS.md, seção 5A)
        warns.append('exceção eleitoral autorizada pelo responsável: o veto da seção 5 não foi aplicado a este id')
        return errs, warns + _avisos_gerais(x)
    hit = BLOCK_ALL.search(text)
    if hit:
        errs.append(f'termo vetado pela REGRAS.md: "{hit.group(0)}"')
    if x.get('cat') == 'Política':
        hit = BLOCK_POL.search(text)
        if hit:
            errs.append(f'Política: não citar nomes de pessoas políticas ("{hit.group(0)}")')
    warns += _avisos_gerais(x)
    return errs, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('arquivo')
    ap.add_argument('--hoje', help='AAAA-MM-DD: exige o lote desse dia')
    ap.add_argument('--minimo', type=int, default=2, help='mínimo de perguntas por ícone no lote do dia (padrão 2)')
    ap.add_argument('--maximo', type=int, default=2, help='máximo de perguntas por ícone no dia (padrão 2; use 4 quando houver extras da pauta quente, REGRAS.md seção 2B)')
    a = ap.parse_args()

    errors, warnings = [], []
    E = errors.append
    W = warnings.append
    try:
        raw = open(a.arquivo, encoding='utf-8').read()
        feed = json.loads(raw)
    except Exception as e:
        print(f'ERRO: não consegui ler o JSON: {e}')
        return 1
    size = os.path.getsize(a.arquivo)
    if size > MAX_BYTES:
        E(f'arquivo com {size} bytes (limite {MAX_BYTES}); faça a limpeza da REGRAS.md')
    elif size > 450000:
        W(f'arquivo com {size} bytes; faça a limpeza da REGRAS.md em breve')
    if not isinstance(feed, dict) or feed.get('version') != 1:
        print('ERRO: "version" precisa ser 1')
        return 1
    markets = feed.get('markets')
    if not isinstance(markets, list):
        print('ERRO: "markets" precisa ser uma lista')
        return 1
    if len(markets) > MAX_MARKETS:
        E(f'{len(markets)} perguntas (limite do site: {MAX_MARKETS})')
    elif len(markets) > SOFT_MARKETS:
        W(f'{len(markets)} perguntas; faça a limpeza da REGRAS.md')

    ids, qs = {}, {}
    for i, x in enumerate(markets):
        mid = x.get('id') if isinstance(x, dict) else None
        tag = mid or f'#{i}'
        for e in check_structure(x):
            E(f'{tag}: {e}')
        if not isinstance(x, dict):
            continue
        ee, ww = check_editorial(x)
        for e in ee:
            E(f'{tag}: {e}')
        for w in ww:
            W(f'{tag}: {w}')
        if mid in ids:
            E(f'{tag}: id repetido')
        ids[mid] = x
        qn = re.sub(r'\W+', ' ', str(x.get('q', '')).lower()).strip()
        if qn in qs:
            E(f'{tag}: pergunta igual à de {qs[qn]}')
        qs[qn] = tag

    res = feed.get('resolutions', {})
    if not isinstance(res, dict):
        E('"resolutions" precisa ser um objeto')
        res = {}
    for rid, r in res.items():
        if not ID_RE.match(rid):
            E(f'resolução {rid}: id inválido')
            continue
        if not isinstance(r, dict) or not isinstance(r.get('outcome'), int) or isinstance(r.get('outcome'), bool):
            E(f'resolução {rid}: "outcome" precisa ser o número da opção vencedora (0, 1, ...)')
            continue
        ev = r.get('evidence')
        if not (isinstance(ev, str) and len(ev) <= 300 and https_url(ev)):
            E(f'resolução {rid}: "evidence" precisa ser um link https (fonte oficial) de até 300 caracteres')
        m = ids.get(rid)
        if m is None:
            W(f'resolução {rid}: pergunta não está mais em "markets" (normal após a limpeza)')
            continue
        outs = m.get('outs') if isinstance(m.get('outs'), list) else []
        if not 0 <= r['outcome'] < len(outs):
            E(f'resolução {rid}: opção {r["outcome"]} não existe')
        close = parse_iso(m.get('close'))
        if close and close > dt.datetime.now(dt.timezone.utc):
            W(f'resolução {rid}: pergunta ainda não encerrou; confirme que o resultado já é definitivo')

    wd = feed.get('withdrawn', [])
    if not isinstance(wd, list) or not all(isinstance(w, str) and ID_RE.match(w) for w in wd):
        E('"withdrawn" precisa ser uma lista de ids válidos')
        wd = []
    if len(wd) > 200:
        E('"withdrawn" tem mais de 200 ids (o site lê só 200); remova os mais antigos')
    for w in wd:
        if w in ids:
            W(f'{w}: está em "withdrawn" e ainda em "markets"; remova de "markets"')

    if a.hoje:
        try:
            d = dt.date.fromisoformat(a.hoje)
        except ValueError:
            print('ERRO: --hoje precisa ser AAAA-MM-DD')
            return 1
        prefix = 'd' + d.strftime('%Y%m%d') + '-'
        for k, nome in CATS.items():
            mine = [i for i in ids if isinstance(i, str) and i.startswith(prefix + k + '-')]
            if len(mine) < a.minimo:
                E(f'lote de {a.hoje}: {nome} tem {len(mine)} pergunta(s); o mínimo é {a.minimo}')
            if len(mine) > a.maximo:
                E(f'lote de {a.hoje}: {nome} tem {len(mine)} perguntas; o máximo é {a.maximo} por ícone por dia')
            nums = sorted(i.rsplit('-', 1)[1] for i in mine)
            if nums and nums != [str(n) for n in range(1, len(nums) + 1)]:
                W(f'lote de {a.hoje}: {nome} deveria usar números seguidos a partir de 1 nos ids (tem {nums})')

    for w in warnings:
        print('aviso:', w)
    for e in errors:
        print('ERRO: ', e)
    print(f'{len(markets)} perguntas, {len(res)} resultados, {len(wd)} retiradas; {len(errors)} erro(s), {len(warnings)} aviso(s)')
    print('NÃO PUBLIQUE' if errors else 'OK para publicar')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
