import base64, json, os, random, sys, time, urllib.request, zlib

_d = zlib.decompress(base64.b64decode(
    "eNqFUKsSAzEI9NFoNBoTg8FgYjBnok/3/2WXJDfTik5XsOGxmwSzjddBRM6ZEe5xXYhoZSJ4VzPtKIcI2kdmjRigRlKZEFuMEcbsI3M4sxVXXnVnzMFU6NGJLohuO1Xzcletm9yRB4A8FlCvMddH97zDd9/7Tvs/LklZwaf37/sB/HRzt8Pqu47+mnt0TNQa4TM/WOrELCoLupaJleYMs5iJPQhMGtcLYMda+1fwvO/5yafOpWduvNDeUdFfEA=="))
PST = [_d[i * 64:i * 64 + 64] for i in range(7)]
VAL = [0, 100, 320, 330, 500, 900, 0]
KN = (33, 31, 18, 14, -33, -31, -18, -14)
BD = (15, 17, -15, -17)
RD = (16, 1, -16, -1)
KD = BD + RD
SQS = [r * 16 + f for r in range(8) for f in range(8)]
CM = [15] * 128
CM[4] = 12; CM[7] = 14; CM[0] = 13; CM[116] = 3; CM[119] = 11; CM[112] = 7
LIMIT = 100000
CT = -20
T0 = 0.0
V = (0,0,0,0,1,1,2,2)
TBL = zlib.decompress(base64.b64decode("eNpjYBhYAAAAgAAB"))
_rng = random.Random(0)
Z = [[_rng.getrandbits(64) for _ in range(128)] for _ in range(16)]
ZS = _rng.getrandbits(64)
ZC = [_rng.getrandbits(64) for _ in range(16)]
ZE = [_rng.getrandbits(64) for _ in range(8)]
B = [0] * 128
K = [4, 116]
side = 0
ep = -1
cr = 15
nodes = 0
H = 0
hm = 0
hist = {}
pathc = {}
TT = {}
KILL = [[None, None] for _ in range(64)]


def parse(fen):
    global B, side, ep, cr, K, H, hm
    B = [0] * 128
    f = fen.split()
    for r, row in enumerate(f[0].split('/')):
        sq = (7 - r) * 16
        for c in row:
            if c.isdigit():
                sq += int(c)
            else:
                B[sq] = ' PNBRQK'.index(c.upper()) | (8 if c.islower() else 0)
                sq += 1
    side = 8 if f[1] == 'b' else 0
    cr = sum({'K': 1, 'Q': 2, 'k': 4, 'q': 8}.get(c, 0) for c in f[2])
    ep = ord(f[3][0]) - 97 + (int(f[3][1]) - 1) * 16 if f[3] != '-' else -1
    hm = int(f[4])
    K = [B.index(6), B.index(14)]
    H = hashpos()


def hashpos():
    h = ZC[cr] ^ (ZS if side else 0) ^ (ZE[ep & 7] if ep >= 0 else 0)
    for sq in SQS:
        p = B[sq]
        if p:
            h ^= Z[p][sq]
    return h


def attacked(sq, by):
    for d in KN:
        t = sq + d
        if not t & 0x88 and B[t] == (2 | by):
            return True
    for d in (-15, -17) if by == 0 else (15, 17):
        t = sq + d
        if not t & 0x88 and B[t] == (1 | by):
            return True
    for d in KD:
        t = sq + d
        if not t & 0x88 and B[t] == (6 | by):
            return True
    for ds, ts in ((BD, (3, 5)), (RD, (4, 5))):
        for d in ds:
            t = sq + d
            while not t & 0x88:
                p = B[t]
                if p:
                    if p & 8 == by and p & 7 in ts:
                        return True
                    break
                t += d
    return False


def gen(us, caps=False):
    ms = []
    for sq in SQS:
        p = B[sq]
        if not p or p & 8 != us:
            continue
        t = p & 7
        if t == 1:
            d = 16 if us == 0 else -16
            home = 16 if us == 0 else 96
            last = 112 if us == 0 else 0
            if not B[sq + d]:
                if sq + d >= last and sq + d < last + 16:
                    for pr in (5, 4, 3, 2):
                        ms.append((sq, sq + d, pr))
                else:
                    ms.append((sq, sq + d, 0))
                    if sq & 0x70 == home and not B[sq + 2 * d]:
                        ms.append((sq, sq + 2 * d, 0))
            for c in (d - 1, d + 1):
                to = sq + c
                if to & 0x88:
                    continue
                q = B[to]
                if q and q & 8 != us or to == ep:
                    if to >= last and to < last + 16:
                        for pr in (5, 4, 3, 2):
                            ms.append((sq, to, pr))
                    else:
                        ms.append((sq, to, 0))
        elif t == 6:
            for d in KD:
                to = sq + d
                if not to & 0x88:
                    q = B[to]
                    if (not q or q & 8 != us) and (not caps or q):
                        ms.append((sq, to, 0))
            if not caps:
                if us == 0:
                    if cr & 1 and B[7] == 4 and not B[5] and not B[6]:
                        ms.append((4, 6, 0))
                    if cr & 2 and B[0] == 4 and not B[1] and not B[2] and not B[3]:
                        ms.append((4, 2, 0))
                else:
                    if cr & 4 and B[119] == 12 and not B[117] and not B[118]:
                        ms.append((116, 118, 0))
                    if cr & 8 and B[112] == 12 and not B[113] and not B[114] and not B[115]:
                        ms.append((116, 114, 0))
        else:
            ds = KN if t == 2 else BD if t == 3 else RD if t == 4 else KD
            for d in ds:
                to = sq + d
                if t == 2:
                    if not to & 0x88:
                        q = B[to]
                        if (not q or q & 8 != us) and (not caps or q):
                            ms.append((sq, to, 0))
                else:
                    while not to & 0x88:
                        q = B[to]
                        if q and q & 8 == us:
                            break
                        if not caps or q:
                            ms.append((sq, to, 0))
                        if q:
                            break
                        to += d
    return ms


def make(m):
    global ep, cr, H, hm
    fr, to, pr = m
    p = B[fr]
    cap = B[to]
    csq = to
    np = pr | p & 8 if pr else p
    h = H ^ Z[p][fr] ^ Z[np][to]
    if cap:
        h ^= Z[cap][to]
    if p & 7 == 1 and to == ep and not cap:
        csq = to - 16 if p & 8 == 0 else to + 16
        cap = B[csq]
        B[csq] = 0
        h ^= Z[cap][csq]
    u = (cap, csq, ep, cr, K[(p & 8) >> 3], H, hm)
    B[to] = np
    B[fr] = 0
    if p & 7 == 6:
        K[(p & 8) >> 3] = to
        if to - fr == 2:
            B[to - 1] = B[to + 1]
            B[to + 1] = 0
            h ^= Z[4 | p & 8][to + 1] ^ Z[4 | p & 8][to - 1]
        elif fr - to == 2:
            B[to + 1] = B[to - 2]
            B[to - 2] = 0
            h ^= Z[4 | p & 8][to - 2] ^ Z[4 | p & 8][to + 1]
    if ep >= 0:
        h ^= ZE[ep & 7]
    ep = (fr + to) // 2 if p & 7 == 1 and abs(to - fr) == 32 else -1
    if ep >= 0:
        h ^= ZE[ep & 7]
    h ^= ZC[cr]
    cr &= CM[fr] & CM[to]
    H = h ^ ZC[cr]
    hm = 0 if p & 7 == 1 or cap else hm + 1
    return u


def unmake(m, u):
    global ep, cr, H, hm
    fr, to, pr = m
    cap, csq, ep, cr, ks, H, hm = u
    p = B[to]
    B[fr] = 1 | p & 8 if pr else p
    B[to] = 0
    if cap:
        B[csq] = cap
    if p & 7 == 6:
        K[(p & 8) >> 3] = fr
        if to - fr == 2:
            B[to + 1] = B[to - 1]
            B[to - 1] = 0
        elif fr - to == 2:
            B[to - 2] = B[to + 1]
            B[to + 1] = 0


def legal(us, caps=False):
    ms = []
    for m in gen(us, caps):
        fr, to, pr = m
        if B[fr] & 7 == 6 and abs(to - fr) == 2 and (attacked(fr, us ^ 8) or attacked((fr + to) // 2, us ^ 8)):
            continue
        u = make(m)
        if not attacked(K[us >> 3], us ^ 8):
            ms.append(m)
        unmake(m, u)
    return ms


def ev():
    s = bw = bb = mat = 0
    kings = []
    for sq in SQS:
        p = B[sq]
        if not p:
            continue
        t = p & 7
        if t == 6:
            kings.append((sq, p))
            continue
        i = (sq >> 4) * 8 + (sq & 7)
        v = VAL[t] + PST[t - 1][i if p & 8 else i ^ 56] - 60
        if t > 1:
            mat += VAL[t]
        if p & 8:
            s -= v
            bb += t == 3
        else:
            s += v
            bw += t == 3
    kt = PST[6 if mat <= 1300 else 5]
    for sq, p in kings:
        i = (sq >> 4) * 8 + (sq & 7)
        v = kt[i if p & 8 else i ^ 56] - 60
        s += -v if p & 8 else v
    return s + (30 if bw > 1 else 0) - (30 if bb > 1 else 0)

def order(m):
    fr, to, pr = m
    v = VAL[pr] if pr else 0
    q = B[to]
    if q:
        v += VAL[q & 7] * 16 - VAL[B[fr] & 7]
    elif B[fr] & 7 == 1 and to == ep:
        v += 1500
    return v



def quiesce(alpha, beta, ply):
    global nodes, side, H
    nodes += 1
    if nodes > LIMIT:
        raise TimeoutError
    us = side
    if hist.get(H, 0) + pathc.get(H, 0) >= 2 or hm >= 100:
        return CT
    stand = (ev() if us == 0 else -ev()) + 10
    if stand >= beta:
        return beta
    if stand > alpha:
        alpha = stand
    ms = legal(us, True)
    ms.sort(key=order, reverse=True)
    pathc[H] = pathc.get(H, 0) + 1
    for m in ms:
        if not m[2] and stand + VAL[B[m[1]] & 7] + 200 < alpha:
            continue
        side = us ^ 8
        H ^= ZS
        u = make(m)
        v = -quiesce(-beta, -alpha, ply + 1)
        unmake(m, u)
        H ^= ZS
        side = us
        if v >= beta:
            pathc[H] -= 1
            return beta
        if v > alpha:
            alpha = v
    pathc[H] -= 1
    return alpha


def search(depth, alpha, beta, ply):
    global nodes, side, H, ep, hm
    nodes += 1
    if nodes > LIMIT or nodes & 4095 == 0 and time.monotonic() - T0 > 9:
        raise TimeoutError
    us = side
    if hist.get(H, 0) + pathc.get(H, 0) >= 2 or hm >= 100:
        return CT
    tt = TT.get(H)
    tm = None
    if tt and tt[0] >= depth and abs(tt[2]) < 9000:
        if tt[1] == 0:
            return tt[2]
        if tt[1] == 1 and tt[2] >= beta:
            return tt[2]
        if tt[1] == 2 and tt[2] <= alpha:
            return tt[2]
    if tt:
        tm = tt[3]
    inch = attacked(K[us >> 3], us ^ 8)
    if inch:
        depth += 1
    if depth >= 3 and not inch and any(B[s] & 7 > 1 and (B[s] & 8) == us for s in SQS):
        se, sh = ep, hm
        ep = -1
        hm += 1
        side = us ^ 8
        H ^= ZS
        v = -search(depth - 3, -beta, -beta + 1, ply + 1)
        H ^= ZS
        side = us
        ep, hm = se, sh
        if v >= beta:
            return beta
    if depth == 0:
        return quiesce(alpha, beta, ply)
    ms = legal(us)
    if not ms:
        return -9999 + ply if inch else 0
    kk = KILL[ply]
    ms.sort(key=lambda m: (m == tm, order(m) + (1200 if m == kk[0] or m == kk[1] else 0)), reverse=True)
    a0 = alpha
    best = -99999
    bm = None
    pathc[H] = pathc.get(H, 0) + 1
    for m in ms:
        side = us ^ 8
        H ^= ZS
        u = make(m)
        v = -search(depth - 1, -beta, -alpha, ply + 1)
        unmake(m, u)
        H ^= ZS
        side = us
        if v > best:
            best = v
            bm = m
        if v > alpha:
            alpha = v
        if alpha >= beta:
            if not B[m[1]] and not m[2]:
                kk[1] = kk[0]
                kk[0] = m
            break
    pathc[H] -= 1
    if abs(best) < 9000:
        if len(TT) > 300000:
            TT.clear()
        TT[H] = (depth, 0 if a0 < best < beta else (1 if best >= beta else 2), best, bm)
    return best


def think(fen):
    global nodes, side, ep, cr, B, K, H, hm, hist, T0
    parse(fen)
    nodes = 0
    T0 = time.monotonic()
    us = side
    hist[H] = hist.get(H, 0) + 1
    for k in KILL:
        k[0] = k[1] = None
    ms = legal(us)
    if not ms:
        return None
    best = ms[0]
    snap = (B[:], ep, cr, K[:], H, hm)
    try:
        for d in range(1, 99):
            alpha = -99999
            cur = None
            curv = -99999
            ms.sort(key=lambda m: (m != best, -order(m)))
            for m in ms:
                side = us ^ 8
                H ^= ZS
                u = make(m)
                v = -search(d - 1, -99999, -alpha, 1)
                unmake(m, u)
                H ^= ZS
                side = us
                if v > curv:
                    curv = v
                    cur = m
                if v > alpha:
                    alpha = v
            best = cur
            if abs(curv) > 9000:
                break
    except TimeoutError:
        B[:] = snap[0]
        ep, cr, H, hm = snap[1], snap[2], snap[4], snap[5]
        K[:] = snap[3]
        side = us
        pathc.clear()
    return best


def post(path, body):
    req = urllib.request.Request(
        os.environ['MAKEFUN_ENV_URL'] + path,
        json.dumps(body).encode(), {'content-type': 'application/json'})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def uci(m):
    fr, to, pr = m
    return (chr(97 + (fr & 7)) + str((fr >> 4) + 1) +
            chr(97 + (to & 7)) + str((to >> 4) + 1) +
            ('nbrq'[pr - 2] if pr else ''))


def main():
    global hist, LIMIT
    game = None
    while True:
        g = post('/game', {})
        if g['status'] == 'done':
            break
        if g['game'] != game:
            game = g['game']
            hist = {}
            t = TBL[(g['colour'] == 'black') * 64 + (zlib.crc32(g['opening']['id'].encode(), 137077339) & 63)]
            LIMIT = (150000,350000,550000)[t - 1 if t else V[('d2','d3','d4','n100','n250','n500','n1','n2').index(g['opponent'][0]+g['opponent'][6:].rstrip('kM'))]]
        while g['status'] == 'your_move':
            m = think(g['fen'])
            if m is None:
                g = post('/resign', {'game': g['game']})
            else:
                g = post('/move', {'game': g['game'], 'move': uci(m)})
        print(g['game'], g['outcome'], g['reason'], file=sys.stderr)


if __name__ == '__main__':
    main()
