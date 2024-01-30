from music21 import *
import time as t
from state import guitar_frets

# 初期コスト
def startCost(st):
    # 初期状態確率
    n = list(set(st))
    if -1 in n or 0 in n:# nから-1,0を消去
        if -1 in n and len(n) != 1:
            n.remove(-1)
        if 0 in n and len(n) != 1:
            n.remove(0)
    if min(n) >= 4:
      return 2.5
    else:
      return 5.0

# 遷移コスト
def transmatCost(now_s, next_s):
    # コードと単音、コードとコードなら弦同士の移動距離を比較
    # 単音同士ならフレット移動距離を比較
    
    # lfFret以上離れていたら大きな値を設定したい
    lf = 4
    def is_monophony(mel, s_mel):
        return len(s_mel) == 1 and mel.count(s_mel[0]) == 1
    
    # 2つの状態のmin, maxを計算
    snow_s = list(set(now_s))
    if -1 in snow_s or 0 in snow_s:# aから-1,0を消去したい
        if -1 in snow_s and len(snow_s) != 1:
            snow_s.remove(-1)
        if 0 in snow_s and len(snow_s) != 1:
            snow_s.remove(0)
    snext_s = list(set(next_s))
    if -1 in snext_s or 0 in snext_s:# bから-1,0を消去したい
        if -1 in snext_s and len(snext_s) != 1:
            snext_s.remove(-1)
        if 0 in snext_s and len(snext_s) != 1:
            snext_s.remove(0)
    
    a_min, a_max = min(snow_s), max(snow_s)
    b_min, b_max = min(snext_s), max(snext_s)
    
    nw_min_ind, nw_max_ind = now_s.index(min(snow_s)), now_s.index(max(snow_s))
    nx_min_ind, nx_max_ind = next_s.index(min(snext_s)), next_s.index(max(snext_s))
    # 単音同士
    if is_monophony(now_s,snow_s) and is_monophony(next_s,snext_s):
        dist = abs(a_min - b_min)
        if a_min == 0 or b_min == 0:
            if b_min <= lf:
                return 0.0
            else:
                return dist
        # return dist
        elif b_min > lf:
            return dist + 5.0
        else:
            return dist
    # 単音->コード or コード->単音
    elif is_monophony(now_s,snow_s) or is_monophony(next_s,snext_s):
        if is_monophony(now_s,snow_s):# aが単音
            if a_max < next_s[nx_min_ind]:# a(単音)がb(コード)の左側
                dist = abs(a_min - next_s[nx_min_ind])
            elif next_s[nx_min_ind] < a_min:# a(単音)がb(コード)の右側
                dist = abs(a_min - next_s[nx_max_ind])
            elif next_s[nx_min_ind] <= a_max and a_max <= next_s[nx_max_ind]:# aがbの内側
                dist = 0
            if a_min == 0:
                if b_min <= lf:
                    return 0.0
                else:
                    return dist
            # return dist
            elif b_min > lf:
                return dist + 5.0
            else:
                return dist
        elif is_monophony(next_s,snext_s):# bが単音
            if b_max < now_s[nw_min_ind]:# a(コード)がb(単音)の右側
                dist = abs(now_s[nw_min_ind] - b_min)
            elif now_s[nw_min_ind] < b_min:# aがbの左側
                dist = abs(now_s[nw_min_ind] - b_min)
            elif now_s[nw_min_ind] <= b_max and b_max <= now_s[nw_max_ind]:# b(単音)がa(コード)の中
                dist = 0
            if b_min == 0:
                if b_min <= lf:
                    return 0.0
                else:
                    return dist
            elif b_min > lf:
                return dist + 5.0
            else:
                return dist
    else:# コード同士
        dist = 1.0 * abs(a_min - b_min)
        return dist

# 出力コスト
def emmisionCost(st, ob, sc, frets, tf):
    # print("in emmision_prob")
    st_name = states2noteName(st, sc, frets)
    if ob[-1] == "chord":
        if ob[1] >= 2.0:# 音価が2以上
            if sum(1 for i in st if i > -1) >= 3:# 3音以上
                if st in tf:# 典型フォームに含まれれば
                    if sum(1 for i in st if i > -1) >= 5:
                        emmision = 0.0
                    elif sum(1 for i in st if i > -1) == 4:
                        emmision = 2.0
                    elif sum(1 for i in st if i > -1) == 3:
                        emmision = 4.0
                    else:
                        emmision = 100.0
                else:# 典型フォームにない
                    if sum(1 for i in st if i > -1) >= 5:
                        emmision = 2.0
                    elif sum(1 for i in st if i > -1) == 4:
                        emmision = 4.0
                    elif sum(1 for i in st if i > -1) == 3:
                        emmision = 6.0
                    else:
                        emmision = 100.0
            else:# 3音未満は高コスト
                emmision = 100.0
        else:# 音価が2未満
            if sum(1 for i in st if i > -1) <= 4:# 5音以下
                if st in tf:# 典型フォームに含まれれば
                    if sum(1 for i in st if i > -1) == 4:
                        emmision = 2.0
                    elif sum(1 for i in st if i > -1) == 3:
                        emmision = 4.0
                    elif sum(1 for i in st if i > -1) == 2:
                        emmision = 6.0
                    elif sum(1 for i in st if i > -1) == 1:
                        emmision = 8.0
                    else:
                        emmision = 100.0
                else:# 典型フォームにない
                    if sum(1 for i in st if i > -1) == 4:
                        emmision = 4.0
                    elif sum(1 for i in st if i > -1) == 3:
                        emmision = 6.0
                    elif sum(1 for i in st if i > -1) == 2:
                        emmision = 8.0
                    elif sum(1 for i in st if i > -1) == 1:
                        emmision = 10.0
                    else:
                        emmision = 100.0
            else:# どれにも当てはまらない
                emmision = 100.0
    elif ob[-1] == "rest":
        if ob[0].name == "rest": # 音名が休符かつ合致すれば
            emmision = 0.0
    elif ob[-1] == "note":
        if ob[0].nameWithOctave == st_name[0]:# 音名が合致すれば
            emmision = 0.0
        else:
            emmision = 100.0
    return emmision


# 主旋律が入っている状態を見つける
def findState(ob, states, sc, frets):
    li = []
    if type(ob) == note.Note:
        n = ob.nameWithOctave
    else:
        n = ob.name
    for st in states:
        if len(list(set(st))) <= 2:
            oct_name = states2noteName(st, sc, frets)
            if [n] == oct_name:
                li.append(st)
    return li

# 主旋律とコード構成音が入っている状態を探索し、格納する
def findChord(ob, states, sc, frets):
    li = []
    for item in states:
        n = states2noteName(item, sc, frets) # 押弦状態itemを音名の配列に変換
        C = [x[:-1] for x in n]
        if set(C).issubset(set(ob[1:])) and ob[0].nameWithOctave == n[0]:
            n_ = [note.Note(x) for x in n]# 状態をnote型で扱えるように変換
            if ob[0] == n_[0] and max(n_) == ob[0] and len(list(set(n))) == len(n):
                if n[-1][:-1] == ob[1]:
                    li.append(item)
    return li

# 主旋律がない場合の状態を探索し、格納
def rest2Chord(ob, states, sc, frets, tf):
    li = []
    for item in states:
        n = states2noteName(item, sc, frets) # 押弦状態itemを音名の配列に変換
        if len(n) <= 1:
            continue
        C = [x[:-1] for x in n]
        if set(C).issubset(set(ob)):
            # n_ = [note.Note(x) for x in n]# 状態をnote型で扱えるように変換
            # if ob[0] == n_[0] and max(n_) == ob[0] and n[-1][:-1] == ob[1]:
            if item in tf and len(list(set(n))) == len(n):
                li.append(item)
    return li

# 状態が発音する音名を配列で返す
def states2noteName(l, sc, frets):
    ans = []
    # print("st: {}".format(l))
    for i in range(len(l)):
        if l[i] == -1:
            continue
        else:
            string, fret = i, l[i]
            n = [k[0] for k in frets[string] if k[2] == fret]
            # print(n)
            if len(n) == 2:
                n_ = [item for item in n if item[:-1] in sc]
                # print(" ",n_)
                if n_: ans.append(n_[0])
                else: ans.append(n[0])
            else: ans.append(n[0])
    if not ans:
        ans.append("rest")
    return ans

# ビタビアルゴリズム本体
def viterbi(observes, states, frets, tf):
    """viterbi algorithm
    Output : labels estimated"""
    scale_name = observes[0][1]
    # print("SCALE: {}".format(sc))
    # print("first: {}".format(observes[1]))
    T = {} # present state
    for st in states:
        T[states.index(st)] = (startCost(st) + emmisionCost(st, observes[1], scale_name, frets, tf), [st])
    # print("T: {}\n".format(T))
    i, j = 1, 2
    now_ob = observes[i]
    while i <= len(observes) and j <= len(observes[1:]):
        next_ob = observes[j]
        if now_ob[-1] == "scale":
            scale_name = now_ob[1]
            i += 1
            now_ob = observes[i]
            T = next_state(now_ob, next_ob, states, scale_name, T, frets, tf)
        elif next_ob[-1] == "scale":
            scale_name = next_ob[1]
            j += 1
            next_ob = observes[j]
            T = next_state(now_ob, next_ob, states, scale_name, T, frets, tf)
        else:
            T = next_state(now_ob, next_ob, states, scale_name, T, frets, tf)
        i += 1
        j += 1
        now_ob = observes[i]
    
    prob, labels = min([T[st] for st in T])
    
    # print("T(result):{}\n".format(T))
    return prob,labels

# ビタビアルゴリズムの途中部分
def next_state(now_ob, next_ob, states, sc, T, frets, tf):
    """calculate a next state"s probability, and get a next path"""
    U = {} # next state
    if now_ob[-1] == "chord":
        if type(now_ob[0][0]) == note.Note:
            l1 = findChord(now_ob[0], states, sc, frets)
        else:
            l1 = rest2Chord(now_ob[0], states, sc, frets, tf)
    else:
        l1 = findState(now_ob[0], states, sc, frets)
    if next_ob[-1] == "chord":
        if type(next_ob[0][0]) == note.Note:
            l2 = findChord(next_ob[0], states, sc, frets)
        else:
            l2 = rest2Chord(next_ob[0], states, sc, frets, tf)
    else:
        l2 = findState(next_ob[0], states, sc, frets)
    for next_s in l2:
        U[states.index(next_s)] = (float("inf"),[])
        for now_s in l1:
            p = T[states.index(now_s)][0] + transmatCost(now_s, next_s) + emmisionCost(next_s, next_ob, sc, frets, tf)
            if p < U[states.index(next_s)][0]:
                U[states.index(next_s)] = (p,T[states.index(now_s)][1]+[next_s])
    # print("U: {}\n".format(U))
    return U

# データ成形
def vec2num(l):
    res = []
    if l.count(-1) == 6:
        return ["rest"]
    for i in range(len(l)):
        if l[i] == -1:
            continue
        res.append((i+1, l[i]))
    return res

# メイン
def Viterbi_guitar(Input):
    print(">>make states...")
    st_states = t.perf_counter()
    frets, sf_state, tf = guitar_frets()
    observe_states = sf_state # 押弦状態集合
    print("size: {}".format(len(observe_states)))
    en_states = t.perf_counter()
    print(">>done: {:.2f}s\n".format(en_states - st_states))
    
    print(">>start viterbi...")
    st_viterbi = t.perf_counter()
    prob, labels = viterbi(Input, observe_states, frets, tf)
    en_viterbi = t.perf_counter()
    print(">>done: {:.2f}s\n".format(en_viterbi - st_viterbi))

    res = []
    inp ,lab = 0,0
    sc = Input[inp][1]
    while inp < len(Input) and lab < len(labels):
        if Input[inp][-1] == "scale":
            sc = Input[inp][1]
            res.append([Input[inp][0], Input[inp][1], Input[inp][-1]])
        else:
            it = states2noteName(labels[lab], sc, frets)
            ar = vec2num(labels[lab])
            res.append([it, ar, Input[inp][1], Input[inp][-1]])
            lab += 1
        inp += 1
    
    return res
            