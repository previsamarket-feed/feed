#!/usr/bin/env python3
"""Publica no feed.json as previsões automáticas ligadas às matérias do Previsa Market (monitor da CNN Brasil).

O Worker editorial grava, para cada matéria publicada que permite uma pergunta objetiva e verificável, um item no formato do feed
(probabilidade inicial NEUTRA, ids -7 a -9 do ícone e do dia). Este script lê esses itens, confere cada um com as MESMAS regras do
validador (`validar_feed.py`, modo normal, sem procuração) e acrescenta ao `feed.json` só os que passam. Nada é inventado aqui.

Segurança: nunca altera nem apaga item existente; ignora id já usado, id retirado/resolvido, pergunta parecida com outra dos últimos
7 dias, ícone fora de eco/fin/tec/neg/esp, número fora de 7 a 9 e encerramento a menos de 2 horas. Se o resultado não passar no
validador do arquivo inteiro, não grava nada.

Uso:  python3 publicar_auto.py [--feed feed.json] [--fonte URL | --arquivo itens.json] [--agora 2026-10-28T20:00:00-03:00] [--simular]
Código de saída: 0 = ok (publicou ou não havia nada); 2 = fonte indisponível (não é erro do feed); 1 = erro.
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import urllib.request

import validar_feed as V

FONTE_PADRAO = 'https://previsamarket-redacao.hads14.workers.dev/public/v1/previsoes-feed.json'
CATS_AUTO = {'eco', 'fin', 'tec', 'neg', 'esp'}
NUMS_AUTO = {7, 8, 9}
MAX_ITENS_POR_RODADA = 6


def palavras(s):
    return set(re.findall(r'[a-zà-ú0-9]{4,}', str(s).lower()))


def parecida(a, b):
    pa, pb = palavras(a), palavras(b)
    if not pa or not pb:
        return False
    return len(pa & pb) / min(len(pa), len(pb)) >= 0.7


def baixar(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'PrevisaMarketFeedAuto/1.0', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as r:
        if r.status != 200:
            raise RuntimeError(f'HTTP {r.status}')
        corpo = r.read(500_000)
    return json.loads(corpo.decode('utf-8'))


def aceitar(item, feed, agora, motivo):
    """Devolve o item limpo (apenas campos conhecidos) ou None, registrando o motivo."""
    if not isinstance(item, dict):
        motivo.append('item não é objeto'); return None
    mid = item.get('id') if isinstance(item.get('id'), str) else ''
    m = V.ID_RE.match(mid)
    if not m:
        motivo.append(f'{mid or "?"}: id inválido'); return None
    if m[4] not in CATS_AUTO or int(m[5]) not in NUMS_AUTO:
        motivo.append(f'{mid}: id fora da faixa reservada (-7 a -9 de eco/fin/tec/neg/esp)'); return None
    limpo = {k: item[k] for k in ('id', 'cat', 'q', 'outs', 'p', 'close', 'crit', 'src', 'desc', 'news') if k in item}
    for e in V.check_structure(limpo):
        motivo.append(f'{mid}: {e}'); return None
    ee, _ = V.check_editorial(limpo)
    if ee:
        motivo.append(f'{mid}: {ee[0]}'); return None
    fecha = V.parse_iso(limpo['close'])
    if fecha is None or fecha < agora + dt.timedelta(hours=2):
        motivo.append(f'{mid}: encerra em menos de 2 horas'); return None
    if len(set(round(v, 4) for v in limpo['p'])) != 1:
        motivo.append(f'{mid}: probabilidade inicial precisa ser neutra'); return None
    ids = {x.get('id') for x in feed['markets'] if isinstance(x, dict)}
    if mid in ids or mid in feed.get('withdrawn', []) or mid in feed.get('resolutions', {}):
        motivo.append(f'{mid}: id já existe'); return None
    limite = agora - dt.timedelta(days=7)
    for x in feed['markets']:
        if not isinstance(x, dict):
            continue
        dia = V.feed_day(x.get('id'))
        if dia and dia >= limite and parecida(x.get('q'), limpo['q']):
            motivo.append(f'{mid}: pergunta parecida com {x.get("id")}'); return None
    return limpo


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--feed', default='feed.json')
    ap.add_argument('--fonte', default=FONTE_PADRAO)
    ap.add_argument('--arquivo', help='lê os itens deste arquivo em vez de baixar (testes)')
    ap.add_argument('--agora', help='ISO 8601 (testes)')
    ap.add_argument('--simular', action='store_true', help='não grava nada')
    a = ap.parse_args()
    agora = V.parse_iso(a.agora) if a.agora else dt.datetime.now(dt.timezone.utc)
    try:
        dados = json.load(open(a.arquivo, encoding='utf-8')) if a.arquivo else baixar(a.fonte)
    except Exception as e:
        print(f'fonte indisponível: {e}')
        return 2
    if not isinstance(dados, dict) or dados.get('ok') is not True or not isinstance(dados.get('itens'), list):
        print('fonte devolveu formato inesperado; nada feito')
        return 2
    feed = json.load(open(a.feed, encoding='utf-8'))
    novos, motivos = [], []
    for item in dados['itens'][:40]:
        if len(novos) >= MAX_ITENS_POR_RODADA:
            break
        ok = aceitar(item, feed, agora, motivos)
        if ok:
            novos.append(ok)
            feed['markets'].append(ok)      # já conta para a checagem de parecidas do próximo item
    for m in motivos:
        print('ignorado:', m)
    if not novos:
        print('nada novo para publicar')
        return 0
    if a.simular:
        print(f'{len(novos)} previsão(ões) seriam publicadas:', ', '.join(n['id'] for n in novos))
        return 0
    texto = json.dumps(feed, ensure_ascii=False, indent=2)
    tmp = a.feed + '.novo'
    open(tmp, 'w', encoding='utf-8').write(texto)
    r = subprocess.run([sys.executable, 'validar_feed.py', tmp], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-1500:])
        print('o arquivo inteiro NÃO passou no validador; nada foi gravado')
        import os
        os.remove(tmp)
        return 1
    import os
    os.replace(tmp, a.feed)
    print(f'{len(novos)} previsão(ões) publicadas:', ', '.join(n['id'] for n in novos))
    return 0


if __name__ == '__main__':
    sys.exit(main())
